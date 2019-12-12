import aoc
from typing import Tuple, List
from collections import namedtuple
import itertools
from operator import attrgetter
import re

class Vector(namedtuple('Vector', ['x','y','z'])):
    def __add__(self, other):
        assert type(other) == Vector
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        assert type(other) == Vector
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __str__(self):
        return f"<x={self.x:>3}, y={self.y:>3}, z={self.z:>3}>"

class Moon:
    def __init__(self, position : Vector):
        self.position = position
        self.velocity = Vector(0,0,0)

    def potential_energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def kinetic_energy(self):
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __str__(self):
        return f"pos={self.position}, vel={self.velocity}"

    def __repr__(self): return str(self)


def main():
    aoc.header("The N-Body Problem")
    aoc.run_tests()

    aoc.output(1, part1)
    # aoc.output(2, part2)

def test():
    initial = [
        Vector(-8, -10, 0),
        Vector(5, 5, 10),
        Vector(2, -7, 3),
        Vector(9, -8, -3)
    ]

    result = next(itertools.islice(
        run_simulation(initial),
        100, 101
    ))
    energy = sum(map(lambda m: m.energy(), result))

    assert energy == 1940, f"Expected 1940, got {energy}"
    
    initial = [ Vector(-1,0,2), Vector(2,-10,-7), Vector(4,-8, 8), Vector(3,5,-1) ]
    for m in itertools.islice(run_simulation(initial), 3000):
        # Prints some interesting periodic results
        print(sum(map(lambda moon: moon.kinetic_energy(), m)), sum(map(lambda moon: moon.potential_energy(), m)))

def part1():
    initial = list(parse_input(aoc.get_input().readlines()))
    result = next(itertools.islice(
        run_simulation(initial),
        1000,1001
    ))
    return sum(map(lambda m: m.energy(), result))

def part2():
    pass

def parse_input(lines : List[str]):
    pattern = re.compile(r"<x=(-?\d+),\s+y=(-?\d+),\s+z=(-?\d+)>")
    for line in lines:
        match = re.match(pattern, line)
        assert match is not None
        yield Vector(int(match.group(1)), int(match.group(2)), int(match.group(3)))


def gravity_tick(moons : List[Moon]):
    for a, b in itertools.combinations(moons, 2):
        # print(a)
        # print(b)
        for i,t in [(0,'x'),(1,'y'),(2,'z')]:
            getter = attrgetter(t)
            a_t = getter(a.position)
            b_t = getter(b.position)
            t_unit = Vector(*[1 if j==i else 0 for j in range(3)])
            
            # print(f" {t}: {a_t:>3} {'<' if a_t < b_t else ''}{'>' if a_t > b_t else ''}{'=' if a_t == b_t else ''}{b_t:>3}\t{t_unit}")
            if a_t < b_t:
                a.velocity += t_unit
                b.velocity -= t_unit
            elif a_t > b_t:
                a.velocity -= t_unit
                b.velocity += t_unit
        # print(a)
        # print(b)
        # print()
        

def run_simulation(initial_positions : List[Vector]):
    moons = [Moon(p) for p in initial_positions]
    while True:
        yield list(moons) # nth element of iterator is nth step of simulation; 0th element of element is after 0 steps of simulation
        gravity_tick(moons)
        for moon in moons:
            moon.position += moon.velocity
        


if __name__ == "__main__":
    main()
