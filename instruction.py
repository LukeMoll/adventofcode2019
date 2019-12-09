import typing
from enum import IntEnum


class AddressingMode(IntEnum):
    DIRECT    = 0 # Operand is an address of the value 
    IMMEDIATE = 1 # Operand is the value

class IntcodeInstruction:
    def __init__(self, *args):
        assert len(args) == self.OPERANDS
        self.args = args

    def expand(self):
        return (
            self.OPCODE + 
            IntcodeInstruction.encode_modes([
                AddressingMode.IMMEDIATE if type(a) == str else AddressingMode.DIRECT
                for a in self.args
            ]),
            *map(int, self.args)
        )

    @staticmethod
    def exec(full_opcode : int, machine, *args):
        raise NotImplemented()

    @staticmethod
    def decode_modes(full_opcode : int) -> typing.Sequence[AddressingMode]:
        m_str = f"{full_opcode//100:03}"
        return tuple(AddressingMode(int(c)) for c in m_str[::-1])

    @staticmethod
    def encode_modes(modes : typing.Sequence[AddressingMode]):
        result = 0
        for i in range(len(modes)):
            result += modes[i] * 10**(2+i)
        return result

class IAdd(IntcodeInstruction):
    OPCODE = 1
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        machine.store(
            op2,
            machine.fetch(op0, modes[0]) +
            machine.fetch(op1, modes[1]) 
        )

class IMult(IntcodeInstruction):
    OPCODE = 2
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        machine.store(
            op2,
            machine.fetch(op0, modes[0]) *
            machine.fetch(op1, modes[1]) 
        )

class IHalt(IntcodeInstruction):
    OPCODE = 99
    OPERANDS = 0
    @staticmethod
    def exec(full_opcode : int, machine):
        machine.running = False

class IInput(IntcodeInstruction):
    OPCODE = 3
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine, op):
        if len(machine.input) > 0:
            machine.store(op, machine.input.pop(0))
        else:
            machine.pc -= 2
            raise EOFError("Out of input!")

class IOutput(IntcodeInstruction):
    OPCODE = 4
    OPERANDS = 1
    @staticmethod
    def exec(full_opcode : int, machine, op):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        val = machine.fetch(op, modes[0])
        machine.output.append(val)

class IJumpNZ(IntcodeInstruction):
    OPCODE = 5
    OPERANDS = 2
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) != 0:
            machine.jump(machine.fetch(op1, modes[1]))

class IJumpZ(IntcodeInstruction):
    OPCODE = 6
    OPERANDS = 2
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) == 0:
            machine.jump(machine.fetch(op1, modes[1]))

class ILessThan(IntcodeInstruction):
    OPCODE = 7
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) < machine.fetch(op1, modes[1]):
            val = 1
        else: val = 0

        machine.store(op2, val)

class IEquals(IntcodeInstruction):
    OPCODE = 8
    OPERANDS = 3
    @staticmethod
    def exec(full_opcode : int, machine, op0, op1, op2):
        modes = IntcodeInstruction.decode_modes(full_opcode)
        if machine.fetch(op0, modes[0]) == machine.fetch(op1, modes[1]):
            val = 1
        else: val = 0

        machine.store(op2, val)