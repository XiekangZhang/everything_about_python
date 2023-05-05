 # ! delta_weight = learning_rate * E_k * O_k * (1 - O_k) * O_j

import numpy
# for sigmoid
import scipy.special

class neuralNetwork:
    def __init__(self, inputnodes: int, hiddennodes: int, outputnodes: int, learningrate: float) -> None:
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # weights
        # * loc: mean of the distribution
        # * scale: standard deviation
        # * size: number of random to create
        self.wih = numpy.random.normal(loc=0.0, scale=pow(self.inodes, -0.5), size=(self.hnodes, self.inodes))
        self.who = numpy.random.normal(loc=0.0, scale=pow(self.hnodes, -0.5), size=(self.onodes, self.hnodes))

        self.lr = learningrate

        # sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hiden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1 - final_outputs)), numpy.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1 - hidden_outputs)), numpy.transpose(inputs))

    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_input = numpy.dot(self.who, hidden_outputs)
        # calculate the singals emerging from final output layer
        final_outputs = self.activation_function(final_input)

        return final_outputs
    
if __name__ == "__main__":
    input_nodes = 3
    hidden_nodes = 3
    output_nodes = 3
    learning_rate = 0.3
    n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    print(n.query([1.0, 0.5, -1.5]))