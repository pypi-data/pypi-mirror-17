
Denoising Autoencoder
=====
You can try the Denoising Autoencoder [Example](../example/mnist_dae.py) running on Mnist. Here we build two hidden layer encoding and decoding layers
```python
from mozi.model import Sequential
from mozi.layers.linear import Linear
from mozi.layers.activation import *
from mozi.layers.noise import Gaussian
import theano.tensor as T

# build model
model = Sequential(input_var=T.matrix(), output_var=T.matrix())
# build encoder
model.add(Gaussian())
encode_layer1 = Linear(prev_dim=28*28, this_dim=200)
model.add(encode_layer1)
model.add(RELU())
encode_layer2 = Linear(prev_dim=200, this_dim=50)
model.add(encode_layer2)
model.add(Tanh())

# build decoder
decode_layer1 = Linear(prev_dim=50, this_dim=200, W=encode_layer2.W.T)
model.add(decode_layer1)
model.add(RELU())
decode_layer2 = Linear(prev_dim=200, this_dim=28*28, W=encode_layer1.W.T)
model.add(decode_layer2)
model.add(Sigmoid())
```
Next we prepare the mnist dataset such that the input X and output y is the same
```python
from mozi.datasets.mnist import Mnist

# build dataset
data = Mnist(batch_size=64, train_valid_test_ratio=[5,1,1])
# for autoencoder, the output will be equal to input
data.set_train(X=data.get_train().X, y=data.get_train().X)
data.set_valid(X=data.get_valid().X, y=data.get_valid().X)

```


Finally build learning method and put everything in train object and run
```python
from mozi.train_object import TrainObject
from mozi.cost import entropy
from mozi.learning_method import AdaGrad

learning_method = AdaGrad(learning_rate=0.01, momentum=0.9,
                          lr_decay_factor=0.9, decay_batch=10000)

train_object = TrainObject(model = model,
                           log = None,
                           dataset = data,
                           train_cost = entropy,
                           valid_cost = entropy,
                           learning_method = learning_method,
                           stop_criteria = {'max_epoch' : 10,
                                            'epoch_look_back' : 5,
                                            'percent_decrease' : 0.01}
                           )
# finally run the code
train_object.setup()
train_object.run()
```
