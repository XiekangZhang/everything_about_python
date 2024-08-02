import logging
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


def get_data(use_own_model: bool = False):
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labes) = fashion_mnist.load_data()
    if train_images[0].any() >= 1:
        print("the image's pixel need to be rescaled.")
        # * according to NN from scratch, you should add a small number to the dataset to avoid 0.
        train_images = (train_images / 255.0 * 0.99) + 0.01
        test_images = (test_images / 255.0 * 0.99) + 0.01
    if use_own_model:
        train_images = train_images[..., tf.newaxis].astype("float32")
        test_images = test_images[..., tf.newaxis].astype("float32")
        train_ds = tf.data.Dataset.from_tensor_slices((train_images, train_labels)).shuffle(10000).batch(32)
        test_ds = tf.data.Dataset.from_tensor_slices((test_images, test_labes)).batch(32)
        #for data, label in test_ds.take(1):
        #    print(data, label)
        return train_ds, test_ds
    else:
        return train_images, train_labels, test_images, test_labes


def show_image(images: list, labels: list, predictions: list) -> None:
    num_rows = 5
    num_cols = 3
    num_images = num_rows * num_cols
    plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
        plot_image(i, predictions[i], labels, images)
        plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
        plot_value_array(i, predictions[i], labels)
    plt.tight_layout()
    plt.show()


def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap="gray")
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = "blue"
    else:
        color = "red"

    plt.xlabel(
        f"{class_names[predicted_label]} {100*np.max(predictions_array):2.0f}% ({class_names[true_label]})",
        color=color,
    )


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)
    thisplot[predicted_label].set_color("red")
    thisplot[true_label].set_color("blue")


def create_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10),
        ]
    )

    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    # model compiler
    probability_model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return probability_model


# ! Variantion to create a model
class MyModel(tf.keras.Model):
    def __init__(self, input_shape, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_layer = tf.keras.layers.Flatten(input_shape=input_shape)
        self.layer_1st = tf.keras.layers.Dense(128, activation="relu")
        self.output_layer = tf.keras.layers.Dense(10)

    def call(self, inputs, training=None, mask=None):
        inputs = self.input_layer(inputs)
        inputs = self.layer_1st(inputs)
        inputs = self.output_layer(inputs)
        return inputs


class MyTrainingSteps:
    def __init__(
        self,
        train: tf.data.Dataset,
        test: tf.data.Dataset,
        epochs,
        model: tf.keras.Model,
        objective: tf.keras.losses.SparseCategoricalCrossentropy,
        train_loss: tf.keras.metrics.Mean,
        train_accuracy: tf.keras.metrics.SparseCategoricalAccuracy,
        test_loss: tf.keras.metrics.Mean,
        test_accuracy: tf.keras.metrics.SparseCategoricalAccuracy,
        optimizer: tf.keras.optimizers.Adam,
    ) -> None:
        self.train= train
        self.test: tf.data.Dataset = test
        self.epochs = epochs
        self.model = model
        self.objective = objective
        self.train_loss = train_loss
        self.train_accuracy = train_accuracy
        self.test_loss = test_loss
        self.test_accuracy = test_accuracy
        self.optimizer = optimizer
        self.logger = logging.getLogger(__name__)

    @tf.function
    def train_step(self, x, y):
        with tf.GradientTape() as tape:
            predictions = self.model(x, training=True)
            loss = self.objective(y, predictions)
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(
            grads_and_vars=zip(gradients, self.model.trainable_variables)
        )
        self.train_loss(loss)
        self.train_accuracy(y, predictions)
        

    @tf.function
    def test_step(self, x, y):
        predictions = self.model(x, training=False)
        loss = self.objective(y, predictions)
        self.test_loss(loss)
        self.test_accuracy(y, predictions)
        

    def training(self):
        for epoch in range(self.epochs):
            self.train_loss.reset_states()
            self.train_accuracy.reset_states()
            self.test_loss.reset_states()
            self.test_accuracy.reset_states()
            for x, y in self.train:
                self.train_step(x, y)
            for test_data, test_label in self.test:
                self.test_step(test_data, test_label)

            print(
            f"Epoch {epoch + 1}, "
            f"Loss: {self.train_loss.result()}, "
            f"Accuracy: {self.train_accuracy.result() * 100}, "
            f"Test Loss: {self.test_loss.result()}, "
            f"Test Accuracy: {self.test_accuracy.result() * 100}"
        )


if __name__ == "__main__":
    # * easy way
    """x_train, y_train, x_test, y_test = get_data() # type: ignore

    model = create_model()
    model.fit(x_train, y_train, epochs=10)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print("\nTest accuracy: ", test_acc)"""

    # predictions = model.predict(x_test)
    # print(np.argmax(predictions[0]), y_test[0], sep=" versus ")

    # show_image(x_test, y_test, predictions)

    # * exp way
    train_ds, test_ds = get_data(True) # type: ignore
    model = MyModel(input_shape=(28, 28))
    training = MyTrainingSteps(
        train=train_ds,
        test=test_ds,
        epochs=10,
        model=model,
        objective=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=tf.keras.optimizers.Adam(),
        train_loss=tf.keras.metrics.Mean(name="train_loss"),
        train_accuracy=tf.keras.metrics.SparseCategoricalAccuracy(name="train_accuracy"),
        test_loss=tf.keras.metrics.Mean(name="test_loss"),
        test_accuracy=tf.keras.metrics.SparseCategoricalAccuracy(name="test_accuracy")
    )
    training.training()
