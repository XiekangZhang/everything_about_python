import matplotlib.pyplot as plt
import os

# support regular expression
import re
import shutil
import string
import tensorflow as tf

# * sentiment analysis --> the training and testing sets are balanced, meaning they contain an equal number of positive and negative reviews
def get_data(
    url: str = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz",
):
    dataset = tf.keras.utils.get_file(
        "aclImdb_v1", url, untar=True, cache_dir=".", cache_subdir=""
    )
    dataset_dir = os.path.join(os.path.dirname(dataset), "aclImdb")
    train_dir = os.path.join(dataset_dir, "train")
    print(os.listdir(dataset_dir))
    return train_dir


# text_dataset_from_directory:
# root/
#   class_a/
#       txt
#   class_b/
#       txt
def read_data(train_dir: str):
    # clean the folder
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
    return raw_train_ds, raw_val_ds, raw_test_ds

def preprocessing(input_data):
    # Standardization --> remove punctuation or HTML elements
    # Tokenization --> splitting stringsinto tokens
    # Vectorization --> converting tokens into numbers
    # all could be done via TextVectorization layer
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
    stripped_punc = tf.strings.regex_replace(stripped_html, "[%s]" % re.escape(string.punctuation), "")
    max_features = 10000
    sequence_length = 250
    vectorize_layer = tf.keras.layers.TextVectorization(
        standardize=stripped_punc,
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length
    )