import aoc
from enum import IntEnum
import typing, itertools

def main():
    aoc.header("Sunny with a Chance of Asteroids")
    aoc.run_tests()

    test_program = list(map(int, aoc.get_input().readline().split(",")))
    aoc.output(1, run, args=[test_program, [1], INSTRUCTIONS_P1])
    aoc.output(2, run, args=[test_program, [5], INSTRUCTIONS_P2])

def test():
    for enc_mode in map(lambda x:x*100, [0,1,10,11,100,101,110,111]):
        dec_mode = Instruction.decode_modes(enc_mode)
        assert Instruction.encode_modes(dec_mode) == enc_mode, f"Expected {enc_mode}, got {Instruction.encode_modes(dec_mode)} (Decoded {dec_mode})"

    def assert_finishes(
        initial_memory,
        inpt=[],
        expected_output=None,
        expected_memory=None,
        instruction_set=INSTRUCTIONS_P1
    ):

        def f():
            for ele in initial_memory:
                if issubclass(ele.__class__, Instruction):
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

class Mode(IntEnum):
    DIRECT    = 0 # Operand is an address of the value 
    IMMEDIATE = 1 # Operand is the value

class Instruction:
    def __init__(self, *args):
        assert len(args) == self.OPERANDS
        self.args = args

    def expand(self):
        return (
            self.OPCODE + 
            Instruction.encode_modes([
                Mode.IMMEDIATE if type(a) == str else Mode.DIRECT
                for a in self.args
            ]),
            *map(int, self.args)
        )

    @staticmethod
    def exec(full_opcode : int, machine, *args):
        raise NotImplemented()

    @staticmethod
    def decode_modes(full_opcode : int) -> typing.Sequence[Mode]:
        m_str = f"{full_opcode//100:03}"
        return tuple(Mode(int(c)) for c in m_str[::-1])

    @staticmethod
    def encode_modes(modes : typing.Sequence[Mode]):
        result = 0
        for i in range(len(modes)):
            result += modes[i] * 10**(2+i)
        return result

class IAdd(Instruction):
    OPCODE = 1
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = Instruction.decode_modes(full_opcode)
        machine.store(
            op2,
            machine.fetch(op0, modes[0]) +
            machine.fetch(op1, modes[1]) 
        )

class IMult(Instruction):
    OPCODE = 2
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = Instruction.decode_modes(full_opcode)
        machine.store(
            op2,
            machine.fetch(op0, modes[0]) *
            machine.fetch(op1, modes[1]) 
        )

class IHalt(Instruction):
    OPCODE = 99
    OPERANDS = 0
    @staticmethod
    def exec(full_opcode : int, machine):
        machine.running = False

class IInput(Instruction):
    OPCODE = 3
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine, op):
        machine.store(op, machine.input.pop(0))

class IOutput(Instruction):
    OPCODE = 4
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine, op):
        modes = Instruction.decode_modes(full_opcode)
        val = machine.fetch(op, modes[0])
        machine.output.append(val)

class IJumpNZ(Instruction):
    OPCODE = 5
    OPERANDS = 2
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1):
        modes = Instruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) != 0:
            machine.jump(machine.fetch(op1, modes[1]))

class IJumpZ(Instruction):
    OPCODE = 6
    OPERANDS = 2
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1):
        modes = Instruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) == 0:
            machine.jump(machine.fetch(op1, modes[1]))

class ILessThan(Instruction):
    OPCODE = 7
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = Instruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) < machine.fetch(op1, modes[1]):
            val = 1
        else: val = 0

        machine.store(op2, val)

class IEquals(Instruction):
    OPCODE = 8
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = Instruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) == machine.fetch(op1, modes[1]):
            val = 1
        else: val = 0

        machine.store(op2, val)

INSTRUCTIONS_P1 = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput]
}

INSTRUCTIONS_P2 = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput, IJumpNZ, IJumpZ, ILessThan, IEquals]
}

class IntcodeMachine: 

    def __init__(self, initial_memory : typing.List[int], instruction_set : typing.Dict[int, Instruction], inpt=[]):
        self.memory = {
            i:initial_memory[i] for i in range(len(initial_memory))
        }
        self.memory_top = len(initial_memory) + 1
        self.pc = -1
        self.running = True
        self.jumped = False
        self.input = inpt
        self.output = []
        self.instruction_set = instruction_set

    def next_pc(self):
        if self.jumped: 
            self.jumped = False
            return self.pc

        self.pc += 1
        while self.pc not in self.memory: 
            self.pc += 1
            if self.pc > self.memory_top:
                # Halt; run off the end of memory
                raise KeyError("Run off the end of memory!")
        return self.pc

    def step(self) -> bool:
        try: full_opcode = self.memory[self.next_pc()]
        except KeyError: return False

        inst = self.instruction_set[full_opcode % 100]
        args = tuple(
            self.memory[self.next_pc()]
            for _ in range(inst.OPERANDS)
        )
        # print(full_opcode, *args)
        inst.exec(full_opcode, self, *args)
        return self.running


    def fetch(self, op, mode : Mode):
        if mode == Mode.IMMEDIATE: return op
        # else
        if op in self.memory:
            return self.memory[op]
        else:
            raise RuntimeError(f"Uninitialised access at address {op}")

    def store(self, address : int, value : int):
        self.memory[address] = value
        if address > self.memory_top: self.memory_top = address + 1

    def jump(self, address):
        self.pc = address
        self.jumped = True


if __name__ == "__main__":
    main()
