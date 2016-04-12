import random
import math


class Node:
    def __init__(self, connections):
        self.weights = []
        self.bias = random.random() - 0.5
        self.output = 0.0
        self.error = 0.0
        self.diff = 0.0

        for i in range(connections):
            self.weights.append((random.random() - 0.5) / 10)


class Layer:
    def __init__(self, number_nodes, number_inputs):
        self.nodes = []
        self.inputs = number_inputs

        for i in range(number_nodes):
            self.nodes.append(Node(number_inputs))

    def feedforward(self, inputs):
        for node in self.nodes:
            total = node.bias
            for i, j in zip(inputs, node.weights):
                total += i * j
            node.output = self.sigmoid(total)

    def output(self):
        out = []
        for node in self.nodes:
            out.append(node.output)
        return out

    def sigmoid(self, val):
        if val == 0:
            return val
        return 1.0/(1.0 + math.exp(-val))


class Network:
    def __init__(self, layers, learning_rate):
        self.input = []
        self.layers = []
        for i in range(len(layers))[1:]:
            self.layers.append(Layer(layers[i], layers[i-1]))

        self.learning_rate = learning_rate

    def feedforward(self, inputs):
        self.layers[0].feedforward(inputs)
        for i in range(len(self.layers))[1:]:
            self.layers[i].feedforward(self.layers[i-1].output())

    def assign_error(self, expected):
        # output layer
        for i in range(len(self.layers[-1].nodes)):
            actual = self.layers[-1].nodes[i].output
            self.layers[-1].nodes[i].error = (expected[i] - actual) * actual * (1-actual)

        # the rest (hopefully works....)
        for i in reversed(range(len(self.layers))[:-1]):
            for j in range(len(self.layers[i].nodes)):
                total = 0.0
                for k in range(len(self.layers[i+1].nodes)):
                    total += self.layers[i+1].nodes[k].weights[j] * \
                             self.layers[i+1].nodes[k].error

                self.layers[i].nodes[j].error = self.layers[i].nodes[j].output * total

    def backpropagate(self):
        for i in reversed(range(len(self.layers))[1:]):
            for j in range(len(self.layers[i].nodes)):
                #bias weights
                self.layers[i].nodes[j].diff = self.learning_rate * self.layers[i].nodes[j].error

                #update bias weight
                self.layers[i].nodes[j].bias = self.layers[i].nodes[j].diff

                #update weights
                for k in range(self.layers[i].inputs):
                    diff = self.learning_rate * self.layers[i].nodes[j].error * self.layers[i-1].nodes[k].output

                    self.layers[i].nodes[j].weights[k] += diff

    def cycle(self, inputs, expected_outputs):
        self.feedforward(inputs)
        self.assign_error(expected_outputs)
        self.backpropagate()

    def getoutput(self,inputs):
        self.feedforward(inputs)
        return self.layers[-1].output()



