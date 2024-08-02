# * glob helps selct multiple files using patterns
import glob
import numpy as np
from matplotlib import image

if __name__ == "__main__":
    our_own_dataset = []
    for image_file_name in glob.glob("my_own_images/2828_my_own_?.png"):
        label = int(image_file_name[-5:-4])
        print(f"loading ... {image_file_name} with label {label}")
        img_array = image.imread(image_file_name)
        #img_data = 255.0 - img_array.reshape(784)
        img_data = (img_array / 255.0 * 0.99) + 0.01
        record = np.append(label, img_data)
        our_own_dataset.append(record)