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