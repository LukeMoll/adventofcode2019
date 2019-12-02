import functools, time
import aoc

def main():
    aoc.header("The Tyranny of the Rocket Equation")
    test()

    aoc.output(1, part1)
    aoc.output(2, part2)    

def part1():
    return sum(map(get_fuel_required, map(int, aoc.get_input().readlines())))

def part2():
    return sum(map(get_fuel_required_recursive, map(int, aoc.get_input().readlines())))

def test():
    # part 1
    assert get_fuel_required(12) == 2
    assert get_fuel_required(14) == 2
    assert get_fuel_required(1969) == 654
    assert get_fuel_required(100756) == 33583

    # part 2
    assert get_fuel_required_recursive(14) == 2
    assert get_fuel_required_recursive(1969) == 966
    assert get_fuel_required_recursive(100756) == 50346

    print("✓ All tests passed!")

@functools.lru_cache
def get_fuel_required(mass : int):
    return max((mass // 3) - 2, 0)

@functools.lru_cache
def get_fuel_required_recursive(mass : int):
    base = get_fuel_required(mass)
    if base > 8:
        return base + get_fuel_required_recursive(base)
    else: return base
    

if __name__ == "__main__":
    main()