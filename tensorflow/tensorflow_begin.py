# a user-friendly starting code
import tensorflow as tf
import numpy

if __name__ == "__main__":
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10),
        ]
    )

    # * This loss is euqal to the negative log probability of the true class:
    # * the loss is zero if the model is sure of the correct class.
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])

    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test, y_test, verbose=2)  # type: ignore

    # * It possible to bake the tf.nn.softmax function into the activation function 
    # * for the last layer of the network. While this can make the model output
    # * more directly interpretable, this approach is discouraged as it's impossible
    # * to provide an exact and numerically stable loss calculation for all models
    # * when using a softmax output.
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    print("model: {}".format(model(x_test[:5])))
    print(f"probability: {probability_model(x_test[:5])}")
