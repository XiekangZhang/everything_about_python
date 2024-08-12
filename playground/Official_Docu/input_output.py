if __name__ == '__main__':
    animals = 'eels'
    print(f"My hovercraft is full of {animals}.")
    print(f"My hovercraft is full of {animals!r}.")
    print(f"My hovercraft is full of {animals!a}.")

    table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
    print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))