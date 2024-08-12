#!/usr/bin/env python3
# password: present
# https://cws.pym.dev/test-onboarding/
import ast
from functools import partial
from inspect import getsource
import os
from pathlib import Path
import re
import shutil
import sys
from textwrap import dedent
import unittest

from test_data import MODULES, TESTS


class Color:
    BOLD = "\033[1m"
    UNDER = "\033[4m"
    END = "\033[0m"
    RED = "\033[91m"


def _assert_op_sub(op, match):
    node = ast.parse(match[0])
    expression1, expression2, *_ = node.body[0].value.args
    if hasattr(ast, "unparse"):
        expression1 = ast.unparse(expression1)
        expression2 = ast.unparse(expression2)
    else:
        expression1 = ast.get_source_segment(match[0], expression1)
        expression2 = ast.get_source_segment(match[0], expression2)
    return f"assert {expression1} {op} {expression2}"


def reformat_source(method_source):
    # Remove first line and dedent
    source = dedent("".join(method_source.splitlines(keepends=True)[1:]))

    # Convert common assertions
    source = re.sub(
        r"self.assertEqual\((.*), (.*)\)",
        partial(_assert_op_sub, "=="),
        source
    )
    source = re.sub(
        r"self.assertIs\((.*), (.*)\)",
        partial(_assert_op_sub, "is"),
        source
    )
    source = re.sub(
        r"self.assertIn\((.*), (.*)\)",
        partial(_assert_op_sub, "in"),
        source
    )

    source = re.sub(
        r"self.assertIsNone\((.*)\)",
        r"assert \1 is None",
        source
    )
    source = re.sub(
        r"self.assert(True|False)\((.*)\)",
        r"assert \2 == \1",
        source
    )

    # characters
    source = re.sub(
        r"self.assertEqual\(\n *(.*),\n *(.*?),?\n[ ]*\)\n",
        r"assert \1 == \2\n",
        source
    )

    # tags_equal
    source = re.sub(
        r"self.assert(True|False)\((.*\()\n(.*)\n(.*)\n([ ]*\))\)\n",
        r"assert \2\n\3\n\4\n\5 == \1\n",
        source
    )

    # count.py
    source = re.sub(
        r"self.assertEqual\((.*), (\[\n[^]]+\])\)\n",
        r"assert \1 == \2\n",
        source
    )
    return source


def reformat_error(traceback_message):
    *lines, last_line = str(traceback_message).splitlines(keepends=True)
    extra = ""
    if last_line.startswith("AssertionError: None !="):
        extra += "Maybe your function didn't return anything?"
        extra += "\nMore on return values at: https://trey.io/ret"
    if "takes 0 positional arguments but" in last_line:
        extra += "Your function doesn't accept any arguments yet."
        extra += "\nMore on arguments at: https://trey.io/args"
    if extra:
        extra = f"\n{Color.BOLD}HINT:{Color.END} {extra}\n"
    return "".join([*lines, Color.RED + last_line + Color.END, extra])


class VerboseTestResult(unittest.TextTestResult):
    def printErrorList(self, flavor, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            description = self.getDescription(test)
            self.stream.writeln(f"{flavor}: {description}")
            self.stream.writeln(self.separator2)
            if hasattr(test, "_testMethodName"):
                full_source = getsource(
                    getattr(type(test), test._testMethodName)
                )
                self.stream.writeln(
                    Color.BOLD +
                    reformat_source(full_source) +
                    Color.END
                )
            self.stream.writeln(reformat_error(err))
            self.stream.flush()


class VerboseTestRunner(unittest.TextTestRunner):
    resultclass = VerboseTestResult


def executable():
    """Return simplest "python" command that seems to work."""
    possible_executables = [
        "python",
        "python3",
        "python3.12",
        "python3.11",
        "python3.10",
        "python3.9",
        "python3.8",
    ]
    for name in possible_executables:
        path = shutil.which(name)
        if path == sys.executable:
            return name
    path = shutil.which("py")
    if path:
        return "py"
    return sys.executable


def get_test(obj_name):
    if obj_name not in TESTS:
        raise SystemExit("Test for {} doesn't exist.".format(obj_name))
    return unittest.defaultTestLoader.loadTestsFromName(TESTS[obj_name])


def run_tests(tests):
    test_suite = unittest.TestSuite(tests)
    return VerboseTestRunner(verbosity=2).run(test_suite).wasSuccessful()


def print_object_names():
    for module, objects in MODULES.items():
        module_path = Path(module).with_suffix(".py")
        if module_path.exists():
            module = module_path
        print(f"{Color.BOLD}{module}{Color.END}")
        for obj in objects:
            print(obj)
        print()


def main(*arguments):
    os.system("")  # Enables ANSI escape characters in terminal
    if not arguments:
        print("Welcome to the Test Framework! ✨\n")
        print("To show all testable exercises run:")
        print(f"{Color.BOLD}{executable()} test.py --list{Color.END}\n")
        print("To test an exercise run:")
        print(f"{Color.BOLD}{executable()} test.py <EXERCISE_NAME>{Color.END}\n")
        print("The message confirms the Test Framework is working! Yay! 🎉")
    elif len(arguments) > 1:
        print("""
Can only call test.py with one argument: the name of the exercise being tested

Examples:

- {executable()} test.py longest_first
- {executable()} test.py Row

This test script runs Trey's tests against your code.
The tests are written in files that end in "_test.py".

If you'd like to test your code manually, you can either:

1. Open a Python REPL, import your code, and execute it with specific arguments
2. Write your own test code at the bottom of your file (e.g. functions.py) and
run that file (e.g. "{executable()} functions.py").

Consult the website for instructions for running the exercises and ask Trey
for help when you get stuck.
        """.strip())
    elif arguments[0] == "--list":
        print("All testable exercises, by section:\n")
        print_object_names()
    elif ' ' in arguments[0] or '(' in arguments[0] or ',' in arguments[0]:
        print("Invalid characters found: {}\n".format(arguments[0]))
        print("This test script doesn't accept code, just an exercise name.\n")
        print("Example usage:")
        print("{executable()} test.py <exercise_name>\n")
    else:
        [argument] = arguments
        if argument.startswith(('modules/', 'modules\\', './modules/')):
            argument = argument.split('/', 1)[1]
        if argument == '--all':
            arguments = list(TESTS)
        else:
            arguments = [argument]
        tests = [
            get_test(arg)
            for arg in arguments
        ]
        print("Testing {}\n".format(', '.join(arguments)))
        test_classes = set(
            tuple(test.id().split('.')[:-1])
            for suite in tests
            for test in suite._tests
        )
        for module, cls in test_classes:
            print("Running {} test class in {}.py\n".format(cls, module))
        success = run_tests(tests)
        sys.exit(not success)


if __name__ == "__main__":
    # Version check before all else
    major, minor, micro, releaselevel, serial = sys.version_info
    if (major, minor) < (3, 6):
        print("You are running Python {0}.{1}".format(major, minor))
        print("Must use Python version 3.6 or above")
        sys.exit(1)
    main(*sys.argv[1:])
