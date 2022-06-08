if __name__ == "__main__":
    filename = "programming.txt"

    with open(filename, "w") as file_object:
        file_object.write("I love programming")