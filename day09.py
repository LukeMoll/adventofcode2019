import aoc
from intcode import IntcodeMachine
from instruction import *
from typing import List

INSTRUCTIONS = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput, IJumpNZ, IJumpZ, ILessThan, IEquals, IAdjustOffset]
}

def main():
    aoc.header("Sensor Boost")
    aoc.run_tests()

    program = list(map(int,aoc.get_input().readline().split(",")))
    aoc.output(1, part, args=[program, [1]])
    aoc.output(2, part, args=[program, [2]])
    # aoc.output(2, part2)

def test():
    def assert_finishes(
        initial_memory,
        inpt=[],
        expected_output=None,
        expected_memory=None,
    ):
        m = IntcodeMachine(initial_memory, INSTRUCTIONS, inpt=list(inpt))
        while m.step(): pass
        if expected_output is not None:
            assert m.output == expected_output, f"Expected output: {expected_output}, got {m.output}"
        if expected_memory is not None:
            assert list(m.memory.values()) == expected_memory

    golf = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    assert_finishes(golf, expected_output=golf)

    m = IntcodeMachine([1102,34915192,34915192,7,4,7,99,0], INSTRUCTIONS)
    while m.step(): pass
    assert len(str(m.output[-1])) == 16

    assert_finishes([104,1125899906842624,99], expected_output=[1125899906842624])

    inp = [12345]
    assert_finishes([203, 10, 204, 10, 99], inpt=inp, expected_output=inp)
    assert_finishes([109, 1000, 203, 10, 204, 10, 99], inpt=inp, expected_output=inp)
    assert_finishes([109, 1000, 203, 10, 4, 1010, 99], inpt=inp, expected_output=inp)

def part(program : List[int], inpt : List[int]):
    m = IntcodeMachine(program, INSTRUCTIONS, inpt=inpt)
    while m.step(): pass
    assert len(m.output) == 1
    return m.output[-1]

if __name__ == "__main__":
    main()
