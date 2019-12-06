import sys, os, shutil, time
import __main__

def get_input():
    basename = __main__.__file__.replace(".py", ".txt")
    input_fn = os.path.join(
        os.path.dirname(__file__),
        "input",
        basename
    )
    if not os.path.exists(input_fn):
        print(f"\n{basename} not found, have you downloaded it?")
        exit(1)
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

def output(part : int, func, post=None, comment=None, args=[], kwargs={}):
    print(f"⧖ Part {part}", end="", flush=True)
    t0 = time.perf_counter()
    result = func(*args, **kwargs)
    t1 = time.perf_counter()

    print(f"\r✓ Part {part}", flush=True)
    print(f"   Elapsed: {(t1-t0)*1000:>10.3f} ms")

    if comment is not None: print(f"   {comment}")
    if post is not None:
        post(result)
    else:
        print(f"   {result}")
    
    print()

def run_tests():
    try:
        t0 = time.perf_counter()
        __main__.test()
        t1 = time.perf_counter()
        print("✓ All tests passed!")
        print(f"   Elapsed: {(t1-t0)*1000:>10.3f} ms")
    except NameError as e:
        print(f"✗ NameError:")
        print(f"   {e}")
        print(f"   Have you defined test()?")
    except AssertionError as e:
        print(f"✗ Tests failed!\n")
        raise e
    print()

def __find_next_day():
    days = map(
        lambda fn: int(os.path.basename(fn).replace("day","").replace(".py","")),
        filter(
            lambda fn: fn.startswith("day"), 
            os.listdir(os.path.dirname(__file__))
        )
    )
    return max(days) + 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    parser_new = subparser.add_parser("new", help="Create a file for a new day")
    parser_new.add_argument("day", type=int, nargs="?", default=__find_next_day(), help="Day to create (defaults to next day that doesn't exist)")

    args = parser.parse_args()
    if args.command == "new":
        filename = os.path.join(os.path.dirname(__file__), f"day{args.day:02}.py")
        if os.path.exists(filename):
            print(f"day{args.day:02}.py exists, overwrite? (y/N)")
            if input().lower() != "y":
                exit()
        with open(filename, 'w') as fd:
            fd.write(
"""import aoc

def main():
    aoc.header("Your title here")
    aoc.run_tests()

    # aoc.output(1, part1)
    # aoc.output(2, part2)

def test():
    pass
    print("✓ All tests passed!")

def part1():
    pass

def part2():
    pass

if __name__ == "__main__":
    main()
""")
            print(f"Created day{args.day:02}.py")

    

