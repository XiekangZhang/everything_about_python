if __name__ == "__main__":
    with open("pi_digits.txt") as file_object:
        # * read whole file
        contents = file_object.read()
    print(contents)

    with open("pi_digits.txt") as file_object:
        # * read line by line
        for line in file_object:
            print(line.rstrip())

    with open("pi_digits.txt") as file_object:
        # * a list of lines from a File
        lines = file_object.readlines()

    for line in lines:
        print(line.rstrip())