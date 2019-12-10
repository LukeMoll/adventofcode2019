import aoc
from typing import List, Tuple, Set, Dict
from collections import namedtuple
import math
from functools import lru_cache
import itertools
from operator import itemgetter

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

    (asteroids, edge, station, _) = aoc.output(1, part1, post=itemgetter(3))
    aoc.output(2, part2, args=[asteroids, edge, station])

def test():
    # part 1
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

    large_example = [
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
    ]
    assert_best(large_example, Vector(11,13), 210)

    # part 2
    (ast, edge) = to_points(large_example)
    (station, _) = find_best(ast,edge)
    ast.remove(station)

    vaporized_ordered = list(vaporize(station, rays_sorted(edge), ast, edge))
    assert vaporized_ordered[:3] == [Vector(11,12),Vector(12,1),Vector(12,2)]

    assert vaporized_ordered[9]  == Vector(12,8)
    assert vaporized_ordered[19] == Vector(16,0)
    assert vaporized_ordered[49] == Vector(16,9)
    assert vaporized_ordered[99] == Vector(10,16)

    assert vaporized_ordered[198] == Vector(9,6)
    assert vaporized_ordered[199] == Vector(8,2)
    assert vaporized_ordered[200] == Vector(10,9)

    assert vaporized_ordered[298] == Vector(11,1)
    assert len(vaporized_ordered) == 299

    assert next(itertools.islice(vaporized_ordered, 199, None)) == Vector(8,2)


def part1():
    (asteroids, edge) = to_points(aoc.get_input().readlines())
    best = find_best(asteroids, edge)
    return (asteroids, edge, best[0], best[1])

def part2(asteroids, edge, station):
    asteroids.remove(station)
    it = vaporize(station, rays_sorted(edge), asteroids, edge)
    v = next(itertools.islice(it, 199, None))
    return (v.x * 100) + v.y

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

@lru_cache
def rays_sorted(edge : Vector):
    rays = rays_fixed(edge)
    return list(sorted(rays, key=lambda V:math.atan2(V.x, V.y), reverse=True))

def trace(origin : Vector, rays: Set[Vector], asteroids : Set[Vector], edge : Vector) -> Set[Vector]:
    for ray in rays:
        p = origin + ray
        while in_field(p, edge):
            if p in asteroids:
                yield p
                break
            p = p + ray

def vaporize(origin : Vector, rays_clockwise : List[Vector], asteroids : Set[Vector], edge : Vector):
    for ray in itertools.cycle(rays_clockwise):
        p = origin + ray
        while in_field(p, edge):
            if p in asteroids:
                yield p
                asteroids.remove(p)
                break # while in_field, go to next iteration of for
            p = p + ray
        if len(asteroids) == 0: break


def naive_raytrace(asteroids : Set[Vector], edge : Vector):
    r = rays_fixed(edge)

    for asteroid in asteroids:
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
