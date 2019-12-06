import aoc
import typing
import pprint

Coord = typing.Tuple[int,int]

def main():
    aoc.header("Crossed Wires")
    aoc.run_tests()

    inp = aoc.get_input()
    path_a = list(inp.readline().split(","))
    path_b = list(inp.readline().split(","))
    aoc.output(1, part1, args=[path_a, path_b])
    aoc.output(2, part2, args=[path_a, path_b])

def manhattan(c : Coord): return abs(c[0]) + abs(c[1])

def test():
    # part 1
    def assert_manhattan(str_a, str_b, dist):
        closest = closest_intersection(str_a.split(","), str_b.split(","))
        assert manhattan(closest) == dist, f"Expected {dist}, got {manhattan(closest)}"

    assert_manhattan("R8,U5,L5,D3", "U7,R6,D4,L4", 6)
    assert_manhattan("U7,R6,D4,L4", "R8,U5,L5,D3", 6)
    assert_manhattan("R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83", 159)
    assert_manhattan("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135)

    # part 2
    def assert_steps(str_a, str_b, steps):
        res = shortest_intersection(str_a.split(","), str_b.split(","))
        assert res == steps, f"Expected {steps}, got {res}"

    assert_steps("R8,U5,L5,D3", "U7,R6,D4,L4", 30)
    assert_steps("R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83", 610)
    assert_steps("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410)

def part1(path_a : typing.Iterable[str], path_b : typing.Iterable[str]) -> int:
    closest = closest_intersection(path_a, path_b)
    return manhattan(closest)

def part2(path_a : typing.Iterable[str], path_b : typing.Iterable[str]) -> int:
    return shortest_intersection(path_a, path_b)

directions = {
    'R': ( 1, 0),
    'U': ( 0, 1),
    'L': (-1, 0),
    'D': ( 0,-1)
}

def path_to_coords(path : typing.Iterable[str]) -> typing.Iterator[Coord]:
    # start at origin
    position = (0,0)
    
    for direction in path:
        offset = directions[direction[0]]
        count = int(direction[1:])
        
        for i in range(count):
            yield (
                position[0] + (i + 1) * offset[0],
                position[1] + (i + 1) * offset[1]
            )

        position = (
            position[0] + count * offset[0],
            position[1] + count * offset[1]
        )
    
def closest_intersection(path_a : typing.Iterable[str], path_b : typing.Iterable[str]) -> Coord:
    intersections = set(path_to_coords(path_a)).intersection(set(path_to_coords(path_b)))
    return sorted(intersections, key=manhattan)[0]

def shortest_intersection(path_a : typing.Iterable[str], path_b : typing.Iterable[str]):
    seq_a = list(path_to_coords(path_a))
    seq_b = list(path_to_coords(path_b))
    intersections = set(seq_a).intersection(set(seq_b)) # we could reuse this from p1
    lengths = map(lambda c:seq_a.index(c) + seq_b.index(c) + 2, intersections)
    return min(lengths)

if __name__ == "__main__":
    main()