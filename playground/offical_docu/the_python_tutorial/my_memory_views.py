if __name__ == "__main__":
    # Example 1: creating a memory view and slicing
    data = bytearray(b"hello, world")
    mv = memoryview(data)
    sliced_mv = mv[7:]
    print(sliced_mv.tobytes())  # Output: b'world'
    # sliced view is writable
    sliced_mv[0] = ord("W")
    print(data)  # Output: bytearray(b'hello, World')

    # Example 2: working with numeric data
    data = b"\x00\x00\x00\x01\x00\x00\x00\x02"
    mv1 = memoryview(data)
    int_view = mv1.cast("i")
    print(int_view.tolist())  # Output: [1, 2]

    print(f"{bytes(memoryview(b'abcdefg')[1:4])}")
