import aoc
import re
from enum import Enum

def main():
    aoc.header("Secure Container")
    test()

    (lower, upper) = aoc.get_input().readline().split("-")
    aoc.output(1, part, args=[int(lower),int(upper),validate_p1])
    aoc.output(2, part, args=[int(lower),int(upper),validate_p2])
    # aoc.output(2, part2)

def test():
    assert rule2("111111")
    assert not rule2("123789")

    assert rule4("112233")
    assert not rule4("123444")
    assert rule4("111122")

    print("✓ All tests passed!")

def part(lower : int, upper : int, validate):
    i = lower
    passwords = []
    while i < upper:
        i = succ(i) # not all outputs from succ pass rule3 :thinking:
        if validate(i): passwords.append(i)
    if passwords[-1] >= upper: passwords.pop()

    for i in passwords: 
        if not validate(i): print(i)
    return len(passwords)

def rule2(s : str):
    for o in range(5):
        if s[o] == s[o+1]:
            return True
    return False

def rule3(s : str):
    for o in range(5):
        if int(s[o]) > int(s[o+1]):
            return False
    return True

class R4State(Enum):
    SINGLE = 1
    DOUBLE = 2
    TRAP = 3

def rule4(s : str):
    state = R4State.SINGLE

    matching = s[0]
    for current in s[1:]:
        if current == matching:
            if state == R4State.SINGLE:
                state = R4State.DOUBLE
            elif state == R4State.DOUBLE:
                state = R4State.TRAP
        else:
            if state == R4State.DOUBLE:
                return True
            state = R4State.SINGLE
            matching = current

    return state == R4State.DOUBLE

r3_re = re.compile(r"^(\d*)([1-9])(0+)$")
def succ(i : int) -> int:
    # Would like to make this implicitly pass rule3
    i += 1
    m = r3_re.match(str(i))
    if m is not None:
        return int(f"{m.group(1)}{m.group(2)}{m.group(2) * len(m.group(3))}")
    else: return i

def validate_p1(i : int) -> bool:
    s = str(i)
    return rule2(s) and rule3(s)

def validate_p2(i : int) -> bool:
    s = str(i)
    return rule4(s) and rule3(s)

if __name__ == "__main__":
    main()
