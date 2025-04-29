# To be rewritten from scratch
# This code is a simplified version of a deep learning engine that includes basic components
# Not to be used or exposed

from abc import ABC, abstractmethod
import numpy as np 

class Module(ABC):
    """
    Base class for all neural network modules.
    """
    def __init__(self):
        self.params = {}
    
    @abstractmethod
    def forward(self, x):
        pass
    
    def _init_parameter(self, name, shape, init_method='xavier'):
        if init_method == 'xavier':
            std = np.sqrt(2.0 / sum(shape))
            return np.random.randn(*shape) * std
        elif init_method == 'zeros':
            return np.zeros(shape)
        elif init_method == 'ones':
            return np.ones(shape)
        else:
            raise ValueError(f"Unknown initialization method: {init_method}")

class Linear(Module):
    def __init__(self, in_features, out_features, bias=True, init_method='xavier'):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
        
        # Initialize weights
        self.params['weight'] = self._init_parameter(
            'weight', 
            (in_features, out_features), 
            init_method
        )
        
        if bias:
            self.params['bias'] = self._init_parameter(
                'bias', 
                (1, out_features), 
                'zeros'
            )
    
    def forward(self, x):
        output = np.dot(x, self.params['weight'])
        if self.bias:
            output += self.params['bias']
        return output

class ReLU(Module):
    def forward(self, x):
        return np.maximum(0, x)

class Softmax(Module):
    def forward(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        self.layers = layers
    
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

class SGD:
    def __init__(self, parameters, learning_rate=0.01):
        self.params = parameters
        self.lr = learning_rate
    
    def step(self, grads):
        for param_name, param in self.params.items():
            if param_name in grads:
                self.params[param_name] -= self.lr * grads[param_name]

class CrossEntropyLoss:
    def __call__(self, predictions, targets):
        m = predictions.shape[0]
        log_probs = -np.log(predictions[range(m), targets])
        loss = np.sum(log_probs) / m
        
        # Compute gradients
        dx = predictions.copy()
        dx[range(m), targets] -= 1
        dx /= m
        return loss, dx

def train_step(model, optimizer, criterion, x_batch, y_batch):
    # Forward pass
    outputs = model.forward(x_batch)
    loss, grad = criterion(outputs, y_batch)
    
    # Backward pass (simplified for now)
    optimizer.step({'weight': grad})
    
    return loss



