from collections import deque


def stackAndQueue():
    # stack: last-in, first-out --> pop
    # queue: first-in, first-out --> popleft
    queue = deque(["Eric", "John", "Michael"])
    queue.append("Terry")
    queue.append("Graham")
    print(queue.popleft())
    print(queue.popleft())
    print(queue)


def transposed():
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    print(*matrix)
    print(list(zip(*matrix)))
    print([[row[i] for row in matrix] for i in range(4)])


if __name__ == "__main__":
    transposed()
