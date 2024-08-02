from mnist_data_set import get_data
from nn import neuralNetwork
import numpy

if __name__ == "__main__":
    input_nodes = 784
    hidden_nodes = 200
    output_nodes = 10

    learning_rate = 0.1

    n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    training_data_list = get_data("mnist_dataset/mnist_train_100.csv")

    epochs = 5

    for e in range(epochs):
        print(f"Epoch: {e}")
        for record in training_data_list:
            all_values = record.split(",")
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            targets = numpy.zeros(output_nodes) + 0.01
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)

    test_data_list = get_data(path="mnist_dataset/mnist_test_10.csv")

    scorecard = []
    for record in test_data_list:
        all_values = record.split(",")
        correct_label = int(all_values[0])
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        outputs = n.query(inputs)
        label = numpy.argmax(outputs) # index of max value
        if label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)

    scorecard_array = numpy.asarray(scorecard)
    print(f"Performace= {scorecard_array.sum() / scorecard_array.size}")