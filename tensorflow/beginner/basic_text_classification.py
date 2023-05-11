import tensorflow as tf
import os
import shutil

if __name__ == "__main__":
    url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
    dataset = tf.keras.utils.get_file("aclImdb_v1", url, untar=True, cache_dir=".", cache_subdir="")
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
        seed=seed
    )
    raw_val_ds = tf.keras.utils.text_dataset_from_directory(
        "aclImdb/train",
        batch_size=batch_size,
        validation_split=0.2,
        subset="validation", 
        seed=seed
    )
    raw_test_ds = tf.keras.utils.text_dataset_from_directory(
        "aclImdb/test",
        batch_size=batch_size
    )

    # Prepare the dataset for training
    # * info
    # * Standardization: removing punctuation or HTML elements
    # * Tokenization: splitting strings into tokens
    # * Vectorization: converting tokens into numbers