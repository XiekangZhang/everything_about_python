"""Test helpers"""
from contextlib import contextmanager
import os
import sys
from tempfile import NamedTemporaryFile


def error_message():
    print("Cannot run {} from the command-line.".format(sys.argv[0]))
    print()
    print("Run python test.py <your_exercise_name> instead")


@contextmanager
def make_file(contents=None):
    with NamedTemporaryFile(mode='wt', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        os.remove(f.name)
