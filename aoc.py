import sys, os, shutil
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
    title = f"Advent of Code 2019 – Day {int(day)}"
    width = min(shutil.get_terminal_size().columns, 55)

    print(f" ╭{'─' * (width - 3)}╮")
    print(f" │ {{:^{width - 5}}} │".format(title))
    print(f" │ {{:^{width - 5}}} │".format(subtitle))
    print(f" ╰{'─' * (width - 3)}╯")
    print()