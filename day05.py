import aoc
from enum import IntEnum
import typing, itertools

def main():
    aoc.header("Sunny with a Chance of Asteroids")
    test()

    # aoc.output(1, part1)
    # aoc.output(2, part2)

def test():
    for enc_mode in map(lambda x:x*100, [0,1,10,11,100,101,110,111]):
        dec_mode = Instruction.decode_modes(enc_mode)
        assert Instruction.encode_modes(dec_mode) == enc_mode, f"Expected {enc_mode}, got {Instruction.encode_modes(dec_mode)} (Decoded {dec_mode})"

    def assert_finishes(
        initial_memory,
        inpt=[],
        expected_output=None,
        expected_memory=None
    ):

        initial_memory = list(itertools.chain.from_iterable(map(lambda e: e.expand() if type(e) == Instruction else e, initial_memory)))
        print(initial_memory)
        m = IntcodeMachine(initial_memory, inpt=inpt)
        while m.step(): pass
        if expected_output is not None:
            assert m.output[-1] == expected_output
        if expected_memory is not None:
            assert list(m.memory.values()) == expected_memory
    
    assert_finishes([
        *IAdd("10","10",100).expand(),
        *IHalt().expand()
    ],
    expected_memory=[1101,10,10,100,99,20])

    print("✓ All tests passed!")

def part1():
    pass

def part2():
    pass

class Mode(IntEnum):
    DIRECT    = 0 # Operand is an address of the value 
    IMMEDIATE = 1 # Operand is the value

class IntcodeMachine: 

    def __init__(self, initial_memory : typing.List[int], inpt=[]):
        self.memory = {
            i:initial_memory[i] for i in range(len(initial_memory))
        }
        self.memory_top = len(initial_memory) + 1
        self.pc = -1
        self.running = True
        self.input = inpt
        self.output = []

    def next_pc(self):
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

        print(full_opcode)
        inst = INSTRUCTIONS[full_opcode % 100]
        args = tuple(
            self.memory[self.next_pc()]
            for _ in range(inst.OPERANDS)
        )
        print(self.pc, inst.__name__)
        print(full_opcode, "<self>", *args)
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

    def output(self, value):
        self.output.append(value)

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
    def exec(full_opcode : int, machine : IntcodeMachine, *args):
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
    def exec(full_opcode : int, machine : IntcodeMachine, op0, op1, op2):
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
    def exec(full_opcode : int, machine : IntcodeMachine, op0, op1, op2):
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
    def exec(full_opcode : int, machine : IntcodeMachine):
        machine.running = False

class IInput(Instruction):
    OPCODE = 3
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine : IntcodeMachine, op):
        machine.store(op, machine.input.pop(0))

class IOutput(Instruction):
    OPCODE = 4
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine : IntcodeMachine, op):
        machine.output(machine.fetch(op, Instruction.decode_modes()[0]))
        
INSTRUCTIONS = {
    i.OPCODE : i for i in [IAdd, IMult, IHalt, IInput, IOutput]
}

if __name__ == "__main__":
    main()
