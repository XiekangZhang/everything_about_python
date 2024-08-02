import tensorflow as tf
import os
import shutil
import re
import string
import matplotlib.pyplot as plt


def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
    return tf.strings.regex_replace(
        stripped_html, "[%s]" % re.escape(string.punctuation), ""
    )


def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label


if __name__ == "__main__":
    url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    dataset = tf.keras.utils.get_file(
        "aclImdb_v1", url, untar=True, cache_dir=".", cache_subdir=""
    )
    dataset_dir = os.path.join(os.path.dirname(dataset), "aclImdb")
    train_dir = os.path.join(dataset_dir, "train")

    # file structure for call text_dataset_from_directory
    # root/
    #   class_a/
    #       txt
    #   class_b/
    #       txt
    remove_dir = os.path.join(train_dir, "unsup")
    shutil.rmtree(remove_dir)

    batch_size = 32
    seed = 42
    raw_train_ds = tf.keras.utils.text_dataset_from_directory(
        "aclImdb/train",
        batch_size=batch_size,
        validation_split=0.2,
        subset="training",
        seed=seed,
    )

    # Example for take data
    for text_batch, label_batch in raw_train_ds.take(1):
        for i in range(3):
            print("Review: ", text_batch.numpy()[i])
            print("Label", label_batch.numpy()[i])

    # When using the "validation_split" and "subset" arguments, make sure to either specify a random seed, or to pass shuffle=False, so that the validation and training
    # splits have no overlap.
    raw_val_ds = tf.keras.utils.text_dataset_from_directory(
        "aclImdb/train",
        batch_size=batch_size,
        validation_split=0.2,
        subset="validation",
        seed=seed,
    )
    raw_test_ds = tf.keras.utils.text_dataset_from_directory(
        "aclImdb/test", batch_size=batch_size
    )

    # Prepare the dataset for training
    # * info
    # * Standardization: removing punctuation or HTML elements
    # * Tokenization: splitting strings into tokens
    # * Vectorization: converting tokens into numbers
    max_features = 10000
    sequence_length = 250
    vectorize_layer = tf.keras.layers.TextVectorization(
        standardize=custom_standardization,
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length,
    )
    # Next, you will call adapt to fit the state of the preprocessing layer to the dataset.
    # This will cause the model to build an index of strings to integers.
    # * It's important to only use your training data when calling adapt, using the test set would leak information
    # Make a text-only dataset without labels, then call adapt
    train_text = raw_train_ds.map(lambda x, y: x)
    vectorize_layer.adapt(train_text)

    # retrieve a batch of 32 reviews and labels from the dataset
    text_batch, label_batch = next(iter(raw_train_ds))
    first_review, first_label = text_batch[0], label_batch[0]
    print("Review", first_review)
    print("Label", raw_train_ds.class_names[first_label])
    print("Vectorized review", vectorize_text(first_review, first_label))
    # You can lookup the token (string) that each integer corresponds to by calling .get_vocabulary() on the layer
    print("1287 ---> ", vectorize_layer.get_vocabulary()[1287])
    print(" 313 --> ", vectorize_layer.get_vocabulary()[313])
    print("Vocabulary size: {}".format(len(vectorize_layer.get_vocabulary())))
    train_ds = raw_train_ds.map(vectorize_text)
    val_ds = raw_val_ds.map(vectorize_text)
    test_ds = raw_test_ds.map(vectorize_text)

    # * These are two important methods you should use when loading data to make sure that I/O does not become blocking
    # * .cache() keeps data in memory after it's loaded off disk. This will ensure the dataset does not become a bottleneck while training your model.
    # * If your dataset is too large to fit into memory, you can also use this method to create a performant on-disk cache, which is more efficient to read
    # * than many small files
    # * .prefetch() overlaps data preprocessing and model execution while training
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Create the model
    # TODO: Embedding layer
    # TODO: GlobalAveragePooling1D
    embedding_dim = 16
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Embedding(max_features + 1, embedding_dim),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1),
        ]
    )
    print(model.summary())
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        optimizer="adam",
        metrics=tf.keras.metrics.BinaryAccuracy(threshold=0.0),
    )
    epochs = 10
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)
    loss, accuracy = model.evaluate(test_ds)
    print("Loss: ", loss)
    print("Accuracy: ", accuracy)
    history_dict = history.history
    print(history_dict.keys())

    """
    acc = history_dict["binary_accuracy"]
    val_acc = history_dict["val_binary_accuracy"]
    loss = history_dict["loss"]
    val_loss = history_dict["val_loss"]

    epochs = range(1, len(acc) + 1)

    # "bo" is for "blue dot"
    plt.plot(epochs, loss, "bo", label="Training loss")
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, "b", label="Validation loss")
    plt.title("Training and validation loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()

    plt.show()

    plt.plot(epochs, acc, "bo", label="Training acc")
    plt.plot(epochs, val_acc, "b", label="Validation acc")
    plt.title("Training and validation accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right")

    plt.show()
    """

    export_model = tf.keras.Sequential(
        [vectorize_layer, model, tf.keras.layers.Activation("sigmoid")]
    )

    export_model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
        optimizer="adam",
        metrics=["accuracy"],
    )

    # Test it with `raw_test_ds`, which yields raw strings
    loss, accuracy = export_model.evaluate(raw_test_ds)
    print(accuracy)

    examples = [
    "The movie was great!",
    "The movie was okay.",
    "The movie was terrible..."
    ]

    print(export_model.predict(examples))