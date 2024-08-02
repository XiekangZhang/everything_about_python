import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

if __name__ == "__main__":
    data_file = open("mnist_dataset/mnist_train_100.csv", "r")
    data_list = data_file.readlines()
    data_file.close()
    record = 6
    all_values = data_list[record].split(",")
    scaled_input = ((np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01).reshape(28, 28)
    # plt.imshow(scaled_input, cmap="Greys", interpolation="None")
    # plt.show()
    # * rotated anticlockwise by 10 degrees
    inputs_plus10_img = scipy.ndimage.rotate(scaled_input, 10.0, cval=0.01, order=1, reshape=False)
    # * rotated clockwise by 10 degrees
    inputs_minus10_img = scipy.ndimage.rotate(scaled_input, -10.0, cval=0.01, order=1, reshape=False)
    plt.imshow(inputs_minus10_img, cmap="Greys", interpolation="None")
    plt.show()