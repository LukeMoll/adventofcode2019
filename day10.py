import aoc
from typing import List, Tuple, Set, Dict
from collections import namedtuple
import math
from functools import lru_cache
from operator import itemgetter
from pprint import pprint

class Vector(namedtuple('Vector', ['x','y'])):
    def __add__(self, other):
        assert type(other) == Vector
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        assert type(other) == Vector
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        assert type(other) == int
        return Vector(self.x * other, self.y * other)

    def __floordiv__(self, other):
        assert type(other) == int
        return Vector(self.x // other, self.y // other)

def main():
    aoc.header("Monitoring Station")
    aoc.run_tests()

    aoc.output(1, part1)
    # aoc.output(2, part2)

def test():
    def assert_best(inp : List[str], station : Vector, count : int):
        (ast, edge) = to_points(inp)
        best = find_best(ast, edge)
        assert best[0] == station
        assert count == best[1]

    assert_best([
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##"
    ], Vector(3,4), 8)

    assert_best([
        "......#.#.",
        "#..#.#....",
        "..#######.",
        ".#.#.###..",
        ".#..#.....",
        "..#....#.#",
        "#..#....#.",
        ".##.#..###",
        "##...#..#.",
        ".#....####"
    ], Vector(5,8), 33)

    assert_best([
        "#.#...#.#.",
        ".###....#.",
        ".#....#...",
        "##.#.#.#.#",
        "....#.#.#.",
        ".##..###.#",
        "..#...##..",
        "..##....##",
        "......#...",
        ".####.###."
    ], Vector(1,2), 35)

    assert_best([
        ".#..#..###",
        "####.###.#",
        "....###.#.",
        "..###.##.#",
        "##.##.#.#.",
        "....###..#",
        "..#.#..#.#",
        "#..#.#.###",
        ".##...##.#",
        ".....#.#.."
    ], Vector(6,3), 41)

    assert_best([
        ".#..##.###...#######",
        "##.############..##.",
        ".#.######.########.#",
        ".###.#######.####.#.",
        "#####.##.#.##.###.##",
        "..#####..#.#########",
        "####################",
        "#.####....###.#.#.##",
        "##.#################",
        "#####.##.###..####..",
        "..######..##.#######",
        "####.##.####...##..#",
        ".#####..#.######.###",
        "##...#.##########...",
        "#.##########.#######",
        ".####.#.###.###.#.##",
        "....##.##.###..#####",
        ".#.#.###########.###",
        "#.#.#.#####.####.###",
        "###.##.####.##.#..##"
    ], Vector(11,13), 210)

def part1():
    (asteroids, edge) = to_points(aoc.get_input().readlines())
    best = find_best(asteroids, edge)
    return best[1]

def part2():
    pass

def to_points(lines : List[str]) -> Tuple[Set[Vector], Vector]:
    edge = Vector(len(lines[-1]) - 1, len(lines) - 1)
    asteroids = set()
    for x in range(edge.x+1):
        for y in range(edge.y+1):
            if      lines[y][x] == "#": asteroids.add(Vector(x,y))
    return (asteroids, edge)


def edges(edge : Vector):
    for x in range(edge.x+1):
        yield Vector(x,0)
        yield Vector(x,edge.y)
    for y in range(edge.x+1):
        yield Vector(0,y)
        yield Vector(edge.x,y)

def in_field(test : Vector, edge : Vector):
        return 0<=test.x<=edge.x and 0<=test.y<=edge.y

def rays(origin : Vector, edge : Vector, edge_vectors):
    # This is problematic
    # Consider a ray of normalised length
    # where 1 step from the origin is before the edge, 
    # and two steps from the origin is after the edge
    # It will never be generated
    rays = set()
    for e in map(lambda e: e - origin, edge_vectors):
        if (g := math.gcd(e.x,e.y)) > 1:
            rays.add(Vector(e.x//g, e.y//g))
        elif g > 0:
            rays.add(e)
    return rays

@lru_cache
def rays_fixed(edge : Vector):
    def it(origin : Vector):
        for x in range(edge.x + 1):
            for y in range(edge.y + 1):
                ray = origin - Vector(x,y)
                if (g := math.gcd(origin.x - x, origin.y - y)) > 0:
                    yield(ray // g)
    rays = set()    
    rays.update(it(Vector(      0,      0 )))
    rays.update(it(Vector( edge.x,      0 )))
    rays.update(it(Vector(      0, edge.y )))
    rays.update(it(Vector( edge.x, edge.y )))
    return rays

def trace(origin : Vector, rays: Set[Vector], asteroids : Set[Vector], edge : Vector) -> Set[Vector]:
    for ray in rays:
        # print(f" Tracing along {ray}", end="", flush=True)
        p = origin + ray
        while in_field(p, edge):
            # print(".", end="", flush=True)
            if p in asteroids:
                yield p
                # print(f"asteroid at {p}")
                break
            p = p + ray
        # print()

def naive_raytrace(asteroids : Set[Vector], edge : Vector):
    r = rays_fixed(edge)

    for asteroid in asteroids:
        # print(f"Tracing from {asteroid}")
        # print(f" Got rays ({len(r)})")
        yield asteroid, trace(asteroid, r, asteroids, edge)

def find_best(asteroids : Set[Vector], edge : Vector):
    return max(
        map(
            lambda t: (t[0], len(set(t[1]))),
            naive_raytrace(asteroids, edge)
        ),
        key=itemgetter(1)        
    )
                
def print_field(mappings : Dict[str,Set[Vector]], edge : Vector):
    field = [[" "] * (edge.x + 1) for _ in range((edge.y + 1))]
    for c,s in mappings.items():
        for v in s:
            try:
                field[v.y][v.x] = c
            except IndexError as identifier:
                print(identifier)
                print(f"{v=}\n{c=}\n{edge=}")
                exit()

    for line in field:
        print("".join(line))

    

if __name__ == "__main__":
    main()
