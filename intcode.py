import typing
from instruction import IntcodeInstruction, AddressingMode

class IntcodeMachine: 

    def __init__(self, initial_memory : typing.List[int], instruction_set : typing.Dict[int, IntcodeInstruction], inpt=[]):
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


    def fetch(self, op, mode : AddressingMode):
        if mode == AddressingMode.IMMEDIATE: return op
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