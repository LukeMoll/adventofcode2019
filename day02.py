import aoc
import typing, time

def main():
    aoc.header("1202 Program Alarm")
    aoc.run_tests()

    aoc.output(1, part1)
    aoc.output(2, part2, comment="Nested loop")
    aoc.output(2, part2_mp, comment="Multiprocessing")

def test():
    # part 1
    def assert_becomes(input : typing.List[int], output : str):
        m = IntcodeMachine(input)
        m.run()
        assert str(m) == output, f"\n   {output}\n!= {m}"
    
    assert_becomes([1,9,10,3,2,3,11,0,99,30,40,50], "3500,9,10,70,2,3,11,0,99,30,40,50")
    assert_becomes([1,0,0,0,99], "2,0,0,0,99")
    assert_becomes([2,3,0,3,99], "2,3,0,6,99")
    assert_becomes([2,4,4,5,99,0], "2,4,4,5,99,9801")
    assert_becomes([1,1,1,4,99,5,6,0,99], "30,1,1,4,2,5,6,0,99")

def part1():
    return run(12,2)

def part2():
    for noun in range(100):
        for verb in range(100):
            if run(noun, verb) == 19690720:
                return (100*noun) + verb

def part2_mp():
    from multiprocessing import Pool
    args = [(noun, verb) for noun in range(100) for verb in range(100)]
    with Pool() as p:
        it = p.imap(run_mp, args)
        result = next(r for r in it if r[0] == 19690720)
        noun,verb = result[1:]
        return (100*noun) + verb

def run_mp(t : typing.Tuple[int]): return(run(*t), *t)

def run(noun : int, verb : int):
    initial_memory = [int(x) for x in aoc.get_input().readline().split(",")]
    initial_memory[1] = noun
    initial_memory[2] = verb
    m = IntcodeMachine(initial_memory)
    m.run()
    return m.memory[0]

class IntcodeMachine:
    def __init__(self, initial_memory: typing.List[int]):
        self.memory = {
            i:initial_memory[i] for i in range(len(initial_memory))
        }
        self.pc = -1
        self.last_key = len(initial_memory) + 1
        self.halted = False

    def run(self):
        while self.step(): pass
        return self.memory

    def __str__(self):
        return ",".join(map(str, self.memory.values()))

    def next(self):
        self.pc += 1
        while self.pc not in self.memory: 
            self.pc += 1
            if self.pc > self.last_key:
                # Halt; run off the end of memory
                raise KeyError("Run off the end of memory!")
        return self.pc

    def step(self):
        try:
            opcode = self.memory[self.next()]
        except KeyError:
            return False
        try:
            if opcode == 1:
                self.add()
            elif opcode == 2:
                self.mult()
            elif opcode == 99:
                return False
            else: 
                raise Exception(f"Unexpected opcode {opcode}!")
        except KeyError:
            print(f"KeyError: Ran out of memory providing operands for opcode {opcode}.")
        return True

    def add(self): 
        op1 = self.memory[self.next()]
        op2 = self.memory[self.next()]
        res = self.memory[self.next()]
        self.memory[res] = self.memory[op1] + self.memory[op2]
        # print(f" m[{res}] <- m[{op1}] + m[{op2}] ({self.memory[res]})")

    def mult(self): 
        op1 = self.memory[self.next()]
        op2 = self.memory[self.next()]
        res = self.memory[self.next()]
        self.memory[res] = self.memory[op1] * self.memory[op2]
        # print(f" m[{res}] <- m[{op1}] * m[{op2}] ({self.memory[res]})")

if __name__ == "__main__":
    main()