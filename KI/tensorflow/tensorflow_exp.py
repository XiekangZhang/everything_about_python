# a full customized model
from typing import Union
import tensorflow as tf


def get_data():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # * add a chaneels dimension
    x_train = x_train[..., tf.newaxis].astype("float32")
    x_test = x_test[..., tf.newaxis].astype("float32")

    train_ds = (
        tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
    )
    test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

    return train_ds, test_ds


class MyModel(tf.keras.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv1 = tf.keras.layers.Conv2D(32, 3, activation="relu")
        self.flatten = tf.keras.layers.Flatten()
        self.d1 = tf.keras.layers.Dense(128, activation="relu")
        self.d2 = tf.keras.layers.Dense(10)

    def call(self, inputs, training=None, mask=None):
        inputs = self.conv1(inputs)
        inputs = self.flatten(inputs)
        inputs = self.d1(inputs)
        return self.d2(inputs)


@tf.function
def train_step(model, images, labels, objective, losses, accuracy, optimizer):
    with tf.GradientTape() as tape:
        # ! training=True is only needed if there are layers with different behavior during training vs inference
        predictions = model(images, training=True)
        loss = objective(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    losses(loss)
    accuracy(labels, predictions)


@tf.function
def test_step(model, images, labels, objective, losses, accuracy):
    predictions = model(images, training=False)
    t_loss = objective(labels, predictions)
    losses(t_loss)
    accuracy(labels, predictions)


if __name__ == "__main__":
    model = MyModel()

    train_ds, test_ds = get_data()

    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    optimizer = tf.keras.optimizers.Adam()
    train_loss = tf.keras.metrics.Mean(name="train_loss")
    train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="train_accuracy")

    test_loss = tf.keras.metrics.Mean(name="test_loss")
    test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="test_accuracy")

    EPOCHS = 5
    for epoch in range(EPOCHS):
        train_loss.reset_states()
        train_accuracy.reset_states()
        test_loss.reset_states()
        test_accuracy.reset_states()

        for images, labels in train_ds:
            train_step(
                model,
                images,
                labels,
                loss_object,
                train_loss,
                train_accuracy,
                optimizer,
            )

        for test_images, test_labels in test_ds:
            test_step(
                model, test_images, test_labels, loss_object, test_loss, test_accuracy
            )

        print(
            f"Epoch {epoch + 1}, "
            f"Loss: {train_loss.result()}, "
            f"Accuracy: {train_accuracy.result() * 100}, "
            f"Test Loss: {test_loss.result()}, "
            f"Test Accuracy: {test_accuracy.result() * 100}"
        )
