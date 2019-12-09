import aoc
import typing, itertools
from intcode import IntcodeMachine
from instruction import * # shush I know what I'm doing

def main():
    aoc.header("Sunny with a Chance of Asteroids")
    aoc.run_tests()

    test_program = list(map(int, aoc.get_input().readline().split(",")))
    aoc.output(1, run, args=[test_program, [1], INSTRUCTIONS_P1])
    aoc.output(2, run, args=[test_program, [5], INSTRUCTIONS_P2])

def test():
    for enc_mode in map(lambda x:x*100, [0,1,10,11,100,101,110,111]):
        dec_mode = IntcodeInstruction.decode_modes(enc_mode)
        assert IntcodeInstruction.encode_modes(dec_mode) == enc_mode, f"Expected {enc_mode}, got {Instruction.encode_modes(dec_mode)} (Decoded {dec_mode})"

    def assert_finishes(
        initial_memory,
        inpt=[],
        expected_output=None,
        expected_memory=None,
        instruction_set=INSTRUCTIONS_P1
    ):

        def f():
            for ele in initial_memory:
                if issubclass(ele.__class__, IntcodeInstruction):
                    # ele is an Instruction, we should expand it and flatten the result
                    for opcode in ele.expand(): yield opcode
                else: yield ele

        m = IntcodeMachine(list(f()), instruction_set, inpt=inpt)
        while m.step(): pass
        if expected_output is not None:
            assert m.output[-1] == expected_output, f"Expected output: {expected_output}, got {m.output[-1]}"
        if expected_memory is not None:
            assert list(m.memory.values()) == expected_memory
    
    assert_finishes([
        IAdd("10","10",100),
        IHalt()
    ],
    expected_memory=[1101,10,10,100,99,20])

    assert_finishes([
        IInput(10),
        IAdd("10", 10, 10),
        IOutput(10),
        IHalt()
    ], inpt=[10],
    expected_output=20)

    # part 2
    
    [
        IInput(9),
        IEquals(9,10,9),
        IOutput(9),
        IHalt(),
        -1,8
    ]

    assert_finishes([3,3,1108,-1,8,3,4,3,99],   inpt=[8],   expected_output=1, instruction_set=INSTRUCTIONS_P2)
    assert_finishes([3,3,1108,-1,8,3,4,3,99],   inpt=[100], expected_output=0, instruction_set=INSTRUCTIONS_P2)

    assert_finishes([3,3,1107,-1,8,3,4,3,99],   inpt=[8],   expected_output=0, instruction_set=INSTRUCTIONS_P2)
    assert_finishes([3,3,1107,-1,8,3,4,3,99],   inpt=[7],   expected_output=1, instruction_set=INSTRUCTIONS_P2)

    assert_finishes([3,9,8,9,10,9,4,9,99,-1,8], inpt=[100], expected_output=0, instruction_set=INSTRUCTIONS_P2)
    assert_finishes([3,9,8,9,10,9,4,9,99,-1,8], inpt=[8],   expected_output=1, instruction_set=INSTRUCTIONS_P2)

    assert_finishes([3,9,7,9,10,9,4,9,99,-1,8], inpt=[8],   expected_output=0, instruction_set=INSTRUCTIONS_P2)
    assert_finishes([3,9,7,9,10,9,4,9,99,-1,8], inpt=[-8],  expected_output=1, instruction_set=INSTRUCTIONS_P2)

    def large_example(input_value):
        if     input_value < 8: expected_value =  999
        elif   input_value > 8: expected_value = 1001
        else:                   expected_value = 1000

        assert_finishes([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
        inpt=[input_value], expected_output=expected_value, instruction_set=INSTRUCTIONS_P2)

    for i in [5,6,7,8,9,10,11,12]: large_example(i)


def run(initial_memory : typing.List[int], inpt : typing.List[int], instruction_set):
    machine = IntcodeMachine(initial_memory, instruction_set, inpt=inpt)
    while machine.step(): pass
    other_codes = set(machine.output[:-1])
    assert other_codes == {0} or len(other_codes) == 0
    return machine.output[-1]

def part2():
    pass

INSTRUCTIONS_P1 = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput]
}

INSTRUCTIONS_P2 = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput, IJumpNZ, IJumpZ, ILessThan, IEquals]
}

if __name__ == "__main__":
    main()
