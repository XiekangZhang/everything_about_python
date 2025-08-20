def f():
    raise OSError("This is an OSError")


if __name__ == "__main__":
    excs = []
    for i in range(3):
        try:
            f()
        except OSError as e:
            e.add_note(f"Happened in Iteration {i+1}")
            excs.append(e)
    raise ExceptionGroup("Multiple OSErrors", excs)
