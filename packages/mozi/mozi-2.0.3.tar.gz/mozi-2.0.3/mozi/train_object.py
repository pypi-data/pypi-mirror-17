

import theano
import theano.tensor as T
floatX = theano.config.floatX

import numpy as np

import time, datetime
import sys

import logging
internal_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from mozi.log import Log
from mozi.utils.theano_utils import shared_zeros
from mozi.utils.train_object_utils import split_list, generate_shared_list, merge_lists, \
                             get_shared_values, is_shared_var, merge_var

from mozi.utils.check_memory import get_mem_usage
from mozi.utils.progbar import Progbar


class TrainObject():

    def __init__(self, model, dataset, train_cost, valid_cost, learning_method, stop_criteria, log=None, verbose=True):
        self.model = model
        self.dataset = dataset
        self.train_cost = train_cost
        self.valid_cost = valid_cost
        self.learning_method = learning_method
        self.stop_criteria = stop_criteria
        self.log = log
        self.verbose = verbose


        if self.log is None:
            # use default Log setting
            self.log = Log(logger=internal_logger)

        elif self.log.save_to_database:
            self.log.print_records()
            self.log.info('\n')


    def setup(self):

        self.log.info( '..begin setting up train object')

        #===================[ build params and deltas list ]==================#

        params = []
        deltas = []

        for i, layer in enumerate(self.model.layers):
            layer_name = "{}_{}".format(layer.__class__.__name__, i)
            if hasattr(layer, 'params'):
                for param in layer.params:
                    # checked that the param to be updated is shared variable
                    if is_shared_var(param):
                        param.name = str(i) + '_' + str(param.name)
                        param.name += '_' + layer.__class__.__name__
                        params += [param]
                        deltas += [shared_zeros(shape=param.shape.eval())]

        #=====================[ training params updates ]=====================#

        self.log.info("..update params: " + str(params))
        train_y_pred, train_layers_stats = self.model.train_fprop(self.model.input_var)
        train_cost = self.train_cost(self.model.output_var, train_y_pred).astype(floatX)
        gparams = T.grad(train_cost, params)
        train_updates = self.learning_method.update(deltas, params, gparams)

        #=================[ append updates from each layer ]==================#

        for i, layer in enumerate(self.model.layers):
            layer_name = "{}_{}".format(layer.__class__.__name__, i)
            if hasattr(layer, 'updates') and len(layer.updates) > 0:
                self.log.info("..{}: has shared variable updates".format(layer_name))
                train_updates += layer.updates

        #----[ append updates of stats from each layer to train updates ]-----#

        self.train_stats_names, train_stats_vars = split_list(train_layers_stats)
        train_stats_vars = [var.astype(floatX) for var in train_stats_vars]
        self.train_stats_shared = generate_shared_list(train_stats_vars)
        train_stats_updates = merge_lists(self.train_stats_shared, train_stats_vars)
        if self.verbose:
            train_updates += train_stats_updates

        #-------------------------[ train functions ]-------------------------#

        self.log.info('..begin compiling functions')
        self.training = theano.function(inputs=merge_var(self.model.input_var, self.model.output_var),
                                        outputs=train_cost,
                                        updates=train_updates,
                                        on_unused_input='warn',
                                        allow_input_downcast=True)

        self.log.info('..training function compiled')

        #=============================[ testing ]=============================#

        test_y_pred, test_layers_stats = self.model.test_fprop(self.model.input_var)

        #-----[ append updates of stats from each layer to test updates ]-----#

        self.test_stats_names, test_stats_vars = split_list(test_layers_stats)
        test_stats_vars = [var.astype(floatX) for var in test_stats_vars]
        self.test_stats_shared = generate_shared_list(test_stats_vars)
        test_stats_updates = []
        if self.verbose:
            test_stats_updates = merge_lists(self.test_stats_shared, test_stats_vars)

        #-------------------------[ test functions ]--------------------------#

        test_stopping_error = self.valid_cost(self.model.output_var, test_y_pred).astype(floatX)
        test_cost = self.train_cost(self.model.output_var, test_y_pred).astype(floatX)

        self.testing = theano.function(inputs=merge_var(self.model.input_var, self.model.output_var),
                                       outputs=(test_stopping_error, test_cost),
                                       updates=test_stats_updates,
                                       on_unused_input='warn',
                                       allow_input_downcast=True)

        self.log.info('..testing function compiled')


    def run(self):

        best_valid_error = float(sys.maxint)
        valid_error = float(sys.maxint)

        train_cost = float(sys.maxint)
        valid_cost = float(sys.maxint)

        train_stats_values = []
        valid_stats_values = []

        epoch = 0
        error_dcr = 0
        self.best_epoch_last_update = 0
        self.best_valid_last_update = float(sys.maxint)

        train_stats_names = ['train_' + name for name in self.train_stats_names]
        valid_stats_names = ['valid_' + name for name in self.test_stats_names]

        job_start = time.time()

        while (self.continue_learning(epoch, error_dcr, best_valid_error)):

            if epoch > 0:
                self.log.info("best_epoch_last_update: %d"%self.best_epoch_last_update)
                self.log.info("valid_error_decrease: %f"%error_dcr)
                self.log.info("best_valid_last_update: %f"%self.best_valid_last_update)
                self.log.info("========[ End of Epoch ]========\n\n")

            epoch += 1

            start_time = time.time()

            num_train_examples = 0
            total_train_cost = 0.
            train_stats_values = np.zeros(len(train_stats_names), dtype=floatX)

            num_valid_examples = 0
            total_valid_cost = 0.
            total_valid_stopping_cost = 0.
            valid_stats_values = np.zeros(len(valid_stats_names), dtype=floatX)

            blk = 0

            for block in self.dataset:
                block_time = time.time()
                blk += 1

                train_set = block.get_train()
                valid_set = block.get_valid()

                #====================[ Training Progress ]====================#
                if train_set.dataset_size > 0:
                    self.log.info('..training '+ self.dataset.__class__.__name__
                                + ' block %s/%s'%(blk, self.dataset.nblocks))

                    progbar = Progbar(target=train_set.dataset_size)
                    blk_sz = 0
                    for idx in train_set:
                        cost = self.training(*train_set[idx])
                        total_train_cost += cost * len(idx)
                        num_train_examples += len(idx)
                        train_stats_values += len(idx) * get_shared_values(self.train_stats_shared)
                        blk_sz += len(idx)
                        progbar.update(blk_sz)
                    print

                #===================[ Validating Progress ]===================#
                if valid_set.dataset_size > 0:

                    self.log.info('..validating ' + self.dataset.__class__.__name__
                                + ' block %s/%s'%(blk, self.dataset.nblocks))

                    progbar = Progbar(target=valid_set.dataset_size)
                    blk_sz = 0
                    for idx in valid_set:
                        stopping_cost, cost = self.testing(*valid_set[idx])
                        total_valid_cost += cost * len(idx)
                        total_valid_stopping_cost += stopping_cost * len(idx)
                        num_valid_examples += len(idx)
                        valid_stats_values += len(idx) * get_shared_values(self.test_stats_shared)
                        blk_sz += len(idx)
                        progbar.update(blk_sz)
                    print

                self.log.info('block time: %0.2fs'%(time.time()-block_time))
                self.log.info(get_mem_usage())

            #-------[ Update train best cost and error values ]-------#
            if num_train_examples > 0:
                train_cost = total_train_cost / num_train_examples
                train_stats_values /= num_train_examples

            #-------[ Update valid best cost and error values ]-------#
            if num_valid_examples > 0:
                valid_error = total_valid_stopping_cost / num_valid_examples
                valid_cost = total_valid_cost / num_valid_examples
                valid_stats_values /= num_valid_examples

                if valid_error < best_valid_error:
                    best_valid_error = valid_error
                    self.log.info('..best validation error so far')
                    if self.log.save_model:
                        self.log._save_model(self.model)
                        self.log.info('..model saved')

                if valid_error < self.best_valid_last_update:
                    error_dcr = self.best_valid_last_update - valid_error
                else:
                    error_dcr = 0

            #==============[ save to database, save epoch error]==============#
            if self.log.save_to_database:
                self.log._save_to_database(epoch, train_cost, valid_error, best_valid_error)
                self.log.info('..sent to database: %s:%s' % (self.log.save_to_database['name'],
                                                             self.log.experiment_name))

            if self.log.save_epoch_error:
                self.log._save_epoch_error(epoch, train_cost, valid_cost, valid_error)
                self.log.info('..epoch error saved')

            end_time = time.time()

            #=====================[ log outputs to file ]=====================#
            merged_train = merge_lists(train_stats_names, train_stats_values)
            merged_valid = merge_lists(valid_stats_names, valid_stats_values)

            outputs = [('epoch', epoch),
                        ('runtime(s)', int(end_time-start_time)),
                        ('train_' + self.train_cost.func_name, train_cost),
                        ('valid_' + self.train_cost.func_name, valid_cost),
                        ('valid_' + self.valid_cost.func_name, valid_error),
                        ('best_valid_' + self.valid_cost.func_name, best_valid_error)]

            outputs += merged_train + merged_valid
            self.log._log_outputs(outputs)


        job_end = time.time()
        self.log.info('Job Completed on %s'%time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(job_end)))
        ttl_time = int(job_end - job_start)
        dt = datetime.timedelta(seconds=ttl_time)
        self.log.info('Total Time Taken: %s'%str(dt))
        self.log.info("========[ End of Job ]========\n\n")


    def continue_learning(self, epoch, error_dcr, best_valid_error):

        if epoch > self.stop_criteria['max_epoch']:
            return False

        elif self.stop_criteria['percent_decrease'] is None or \
            self.stop_criteria['epoch_look_back'] is None:
            return True

        elif np.abs(float(error_dcr) / self.best_valid_last_update) \
            >= self.stop_criteria['percent_decrease']:
            self.best_valid_last_update = best_valid_error
            self.best_epoch_last_update = epoch
            return True

        elif epoch - self.best_epoch_last_update > \
            self.stop_criteria['epoch_look_back']:
            return False

        else:
            return True
