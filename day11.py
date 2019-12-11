import aoc
from intcode import IntcodeMachine
from instruction import *
from day08 import blocks4, print_image4, Size

from typing import List, Tuple, Set
from operator import itemgetter

Coord = Tuple[int]

INSTRUCTIONS = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput, IJumpNZ, IJumpZ, ILessThan, IEquals, IAdjustOffset]
}

def main():
    aoc.header("Space Police")

    program = list(map(int, aoc.get_input().readline().split(",")))
    aoc.output(1, run_robot, args=[program, False], post=lambda t:len(t[1]))
    aoc.output(2, run_robot, args=[program, True], output=part2_post)


directions_clockwise = [
    (0,-1),
    (1,0),
    (0,1),
    (-1,0)
]  

def run_robot(prog : List[int], start_on_white):
    white_panels = {(0,0)} if start_on_white else set()
    painted_panels = set()

    location = (0,0)
    direction = directions_clockwise[0]
    m = IntcodeMachine(prog, INSTRUCTIONS)

    while m.running: 
        try:
            m.input.append(1 if location in white_panels else 0)
            while m.step(): pass
        except EOFError as e:
            paint = m.output.pop(0)
            if paint == 0:
                white_panels -= {location}
            else:
                white_panels.add(location)

            painted_panels.add(location)

            turn = m.output.pop(0)
            x = 1 if turn == 1 else -1
            direction = directions_clockwise[(directions_clockwise.index(direction)+x)%4]

            location = (location[0] + direction[0], location[1] + direction[1])

    return (white_panels, painted_panels)

def coords_to_img(coords : Set[Coord]):
    X = set(map(itemgetter(0), coords))
    Y = set(map(itemgetter(1), coords))
    corner_tl = (
        min(X), min(Y)
    )
    corner_br = (
        max(X), max(Y)
    )
    coords = set(map(lambda c: (c[0]-corner_tl[0], c[1]-corner_tl[1]), coords))
    s = Size(corner_br[0]-corner_tl[0]+1,corner_br[1]-corner_tl[1]+1)
    img = [
        0 for _ in range(s.width * s.height)
    ]
    for x,y in coords:
        img[x + y * s.width] = 1
    return img, s

def part2_post(t):
    (white_panels, printed_panels) = t
    print_image4(*coords_to_img(white_panels))

if __name__ == "__main__":
    main()
