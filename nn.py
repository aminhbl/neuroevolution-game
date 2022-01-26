import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        self.weights = {}
        for layer in range(1, len(layer_sizes)):
            self.weights['W' + '{}'.format(layer)] = np.random.randn(layer_sizes[layer], layer_sizes[layer - 1])
            self.weights['b' + '{}'.format(layer)] = np.zeros((layer_sizes[layer], 1))

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        last_layer = x
        num_of_layers = len(self.weights) // 2
        for l in range(num_of_layers):
            next_layer = np.matmul(self.weights['W' + '{}'.format(l + 1)], last_layer)
            next_layer += self.weights['b' + '{}'.format(l + 1)]
            last_layer = self.activation(next_layer)
        return last_layer

    def reconstruct_weights(self, flat_weights):
        cut_index = 0
        for w in self.weights:
            cut = flat_weights[cut_index:cut_index + self.weights[w].shape[1] * self.weights[w].shape[0]]
            cut_array = np.array(cut)
            self.weights[w] = cut_array.reshape(self.weights[w].shape)
            cut_index += self.weights[w].shape[1] * self.weights[w].shape[0]
