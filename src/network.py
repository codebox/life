from random import random
import numpy as np


class Network:
    def __init__(self, input_size, hidden_layer_size, output_size):
        self.input_size = input_size
        self.hidden_layer_size = hidden_layer_size
        self.output_size = output_size
        self.w1 = np.random.randn(input_size, hidden_layer_size)
        self.w2 = np.random.randn(hidden_layer_size, output_size)
        self.b1 = np.random.randn(self.w1.shape[1], )
        self.b2 = np.random.randn(self.w2.shape[1], )

    def _relu(self, x):
        return np.maximum(0, x)

    def _softmax(self, x, axis=None):
        x = x - x.max(axis=axis, keepdims=True)
        y = np.exp(x)
        return y / y.sum(axis=axis, keepdims=True)

    def calc(self, input_values):
        x = np.array(input_values)
        r1 = x.dot(self.w1) + self.b1
        r2 = self._relu(r1)

        r3 = r2.dot(self.w2) + self.b2
        return self._softmax(r3,1).tolist()

    def copy(self, delta=0.1):
        copy_network = Network(self.input_size, self.hidden_layer_size, self.output_size)
        copy_network.w1 = self.w1 + np.random.randn(self.input_size, self.hidden_layer_size) * delta
        copy_network.w2 = self.w2 + np.random.randn(self.hidden_layer_size, self.output_size) * delta
        copy_network.b1 = self.b1 + np.random.randn(self.w1.shape[1]) * delta
        copy_network.b2 = self.b2 + np.random.randn(self.w2.shape[1]) * delta
        return copy_network
