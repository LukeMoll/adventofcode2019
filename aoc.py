import sys, os
import __main__

def get_input():
    input_fn = os.path.join(
        os.path.dirname(__file__),
        "input",
        __main__.__file__.replace(".py", ".txt")
    )
    return open(input_fn)

def header(subtitle : str):
    day = __main__.__file__.replace("day", "").replace(".py", "")
    print(f" Advent of Code 2019 - Day {int(day)}")
    print(" " + subtitle)
    print()