def f():
    raise OSError("operation failed")


if __name__ == "__main__":
    exes = []
    for i in range(3):
        try:
            f()
        except Exception as e:
            e.add_note(f"Happened in Iteration {i + 1}")
            exes.append(e)
        else:
            print("aaaaaa")
        finally:
            print("bbbbbb")
    raise ExceptionGroup("We have some problems", exes)