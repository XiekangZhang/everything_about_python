import numpy
import matplotlib.pyplot as plt

def get_data(path:str = "mnist_dataset/mnist_train_100.csv"):
    data_file = open(path, "r")
    data_list = data_file.readlines()
    data_file.close()
    return data_list

if __name__ == "__main__":
    data_list = get_data()
    print(f"number of images: {len(data_list)}") # , and 1st image looks like: {data_list[1]}")

    # rearrange to 28*28 
    all_values = data_list[1].split(",")
    # image_array = numpy.asfarray(all_values[1:]).reshape((28, 28)) # return an float array
    # plt.imshow(image_array, cmap="Greys", interpolation="None")
    # plt.show()

    # scale to 0.01 - 1
    scaled_input = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    
    # output nodes is 10
    onodes = 10
    targets = numpy.zeros(onodes) + 0.01
    targets[int(all_values[0])] = 0.99
    print(targets)