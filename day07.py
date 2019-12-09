import aoc
from intcode import IntcodeMachine
from typing import List, Tuple
from functools import lru_cache
from itertools import permutations
from operator import itemgetter
from instruction import *

Settings = Tuple[int,int,int,int,int]
INSTRUCTIONS = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput, IJumpNZ, IJumpZ, ILessThan, IEquals]
}

def main():
    aoc.header("Amplification Circuit")
    aoc.run_tests()

    program = list(map(int, aoc.get_input().readline().split(",")))
    aoc.output(1, part1, args=[program])
    aoc.output(2, part2, args=[program])

def test():
    prog1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert single_sequence(prog1, (4,3,2,1,0)) == 43210
    m = find_max(prog1)
    assert m == ((4,3,2,1,0), 43210), f"Got {m}, expected ((4,3,2,1,0), 43210)"

    assert find_max([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == ((0,1,2,3,4),54321)
    assert find_max([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == ((1,0,4,3,2),65210)

    prog2 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    assert feedback_sequence(prog2, (9,8,7,6,5)) == 139629729
    assert find_max_feedback(prog2) == ((9,8,7,6,5), 139629729)

    assert find_max_feedback([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]) == ((9,7,8,5,6), 18216)

def part1(program : List[int]):
    (settings, val) = find_max(program)
    return val

def part2(program : List[int]):
    (settings, val) = find_max_feedback(program)
    return val

def amplifier(program : List[int], input_value : int, setting : int) -> int:
    m = IntcodeMachine(program, INSTRUCTIONS, inpt=[setting, input_value])
    while m.step(): pass
    return m.output[-1] if len(m.output) > 0 else None

def single_sequence(program : List[int], settings : Settings):
    val = 0
    for i in range(len(settings)):
        val = amplifier(program, val, settings[i])
    return val


def feedback_sequence(program : List[int], settings: Settings):
    output_vals = set()
    val = 0
    amplifiers : List[IntcodeMachine] = [
        IntcodeMachine(program, INSTRUCTIONS, inpt=[s]) for s in settings
    ]

    while True:
        for i in range(len(settings)):
            try:
                amplifiers[i].input.append(val)
                while amplifiers[i].step(): pass
                val = amplifiers[i].output[-1]
            except EOFError:
                val = amplifiers[i].output[-1]

        if not amplifiers[-1].running:
            return val
        if val in output_vals:
            raise RecursionError("Cycle detected!")
            # We never ran into this lol
        else: output_vals.add(val)


def find_max(program : List[int]) -> Tuple[Settings, int]:

    @lru_cache
    def run_recur(partial_settings: Tuple):
        val = run_recur(partial_settings[:-1]) if len(partial_settings) > 1 else 0
        return amplifier(program, val, partial_settings[-1])

    results = {}
    for settings in permutations((0,1,2,3,4)):
        results[settings] = run_recur(settings)

    return tuple(max(results.items(), key=itemgetter(1)))

def find_max_feedback(program : List[int]) -> Tuple[Settings, int]:
    results = {}
    for settings in permutations((5,6,7,8,9)):
        results[settings] = feedback_sequence(program, settings)

    return tuple(max(results.items(), key=itemgetter(1)))

if __name__ == "__main__":
    main()
