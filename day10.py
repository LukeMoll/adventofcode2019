import aoc
from typing import List, Tuple, Set, Dict
from collections import namedtuple
import math
from pprint import pprint

class Vector(namedtuple('Vector', ['x','y'])):
    def __add__(self, other):
        assert type(other) == Vector
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        assert type(other) == Vector
        return Vector(self.x-other.x, self.y-other.y)

def main():
    aoc.header("Monitoring Station")
    aoc.run_tests()

    # aoc.output(1, part1)
    # aoc.output(2, part2)

def test():
    
    inp1 = [
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##"
    ]
    t = to_points(inp1)
    print_field({
        '#': t[0],
        ".": t[1]
    }, t[2])

    print(t[2])
    edge_vectors = set(edges(t[2]))
    pprint(edge_vectors)
    print_field({'+' : edge_vectors}, t[2])

    for origin, asteroids in naive_raytrace(t[0],t[1],t[2]):
        print_field({
            "*": t[0],
            "#": asteroids,
            ".": {origin}
        },t[2])
        input()

def part1():
    pass

def part2():
    pass

def to_points(lines : List[str]) -> Tuple[Set[Vector], Set[Vector], Vector]:
    edge = Vector(len(lines[-1]) - 1, len(lines) - 1)
    asteroids = set()
    gaps = set()
    for x in range(edge.x+1):
        for y in range(edge.y+1):
            if      lines[y][x] == "#": asteroids.add(Vector(x,y))
            elif    lines[y][x] == ".": gaps.add(Vector(x,y))
    return (asteroids, gaps, edge)


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

def trace(origin : Vector, rays: Set[Vector], asteroids : Set[Vector], edge : Vector) -> Set[Vector]:
    for ray in rays:
        print(f" Tracing along {ray}", end="", flush=True)
        p = origin + ray
        while in_field(p, edge):
            print(".", end="", flush=True)
            if p in asteroids:
                yield p
                print(f"asteroid at {p}")
                break
            p = p + ray
        print()

def naive_raytrace(asteroids : Set[Vector], gaps : Set[Vector], edge : Vector):
    edge_vectors = set(edges(edge))

    for gap in gaps:
        print(f"Tracing from {gap}")
        r = rays(gap, edge, edge_vectors)
        print(f" Got rays ({len(r)})")
        yield gap, trace(gap, r, asteroids, edge)

                
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
