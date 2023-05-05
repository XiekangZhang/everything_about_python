from typing import Union
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

def get_data():
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labes) = fashion_mnist.load_data()
    if train_images[0].any() >= 1:
        print("the image's pixel need to be rescaled.") 
        train_images = train_images / 255.0
        test_images = test_images / 255.0
    return train_images, train_labels, test_images, test_labes

def show_image(images: list) -> None:
    plt.figure(figsize=(10, 10))

if __name__ == "__main__":
    x_train, _, _, _ = get_data()
    print(x_train[0])