"""

VM Overview
---------------------------
LOAD - Load a value
MOV - Move register A into B
ADD - Add registers
SUB - Subtract registers
PUSH - Push immediate value
PUSHR - Push register
POP - Pop value off stack into register
JMP - Jump to location
RET - Jump to location at sp
JZ - Jump if Zero Flag
JNZ - Jump if Zero Flag not set
CMP - Compare registers and set zero flag
INC - Increase register
DEC - Decrease register
ENTER - push all registers
LEAVE - pop all registers
BRK - Break
DBG - Print Debug info

--------------------------
Registers:
R0 - Register 0
R1 - Register 1
R2 - Register 2
R3 - Register 3
SP - Stack Pointer

-------------------------
Flags:
EF - Equal Flag
ZF - Zero Flag

-------------------------
Enter Frame
Push Registers R0 through R3

-------------------------
Leave Frame
Pop Registers R3 through R0
"""

LOAD = 10
MOV = 11
ADD = 20
SUB = 21
PUSH = 30
PUSHR = 31
POP = 40
JMP = 50
RET = 51
JZ = 52
JNZ = 53
CMP = 60
INC = 70
DEC = 71

ENTER = 90
LEAVE = 91
BRK = 99
DBG = 100


opcodes = {
    LOAD: "Load",
    MOV: "Move",
    ADD: "Add",
    PUSH: "Push",
    PUSHR: "Push Register",
    POP: "Pop",
    JMP: "Jump",
    RET: "Return",
    CMP: "Compare",
    INC: "Increase",
    DEC: "Decrease",
    ENTER: "Enter Frame",
    LEAVE: "Leave Frame",
    BRK: "Break"
}

R0 = r1 = 0
R1 = r2 = 1
R2 = r3 = 2
R3 = r4 = 3

SP = 4
NULL = 0

EF = 0 #equal flag
ZF = 1 #zero flag





class SimpleVM:
    def __init__(self,memory_size=100):
        self.memory = [0] * memory_size # 100 bytes of memory
        self.registers = [0] * 5 # 5 registers
        self.ip = 0 # instruction pointer
        self.registers[SP] = 75 # stack pointer
        self.flags = [0] * 2


    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def display_memory(self):
        print("Memory: ")
        for index,value in enumerate(self.memory):
            print(f"{value:02} ",end="")
            if (index+1) % 3 == 0:
                print()
        print()

    def print_flags(self):
        print("Flags: ")
        print("Zero: ",self.flags[ZF])
        print("Equal: ",self.flags[EF])

    def display_stack(self):
        print("Stack: ")
        for index, value in enumerate(self.memory[self.getSP()-1::-1]):
            print(f"{value:02} ",end="")
            if (index+1) % 8 == 0:
                print()
        print()
            

    def debug(self):
        print("Registers: ", self.registers)
        print("SP: ",self.getSP())
        self.print_flags()
        self.display_stack()

    def fetch(self):
        value = self.memory[self.ip]
        self.ip += 1
        return value

    def getSP(self):
        return self.registers[SP]

    def popValue(self):
        self.registers[SP] -= 1
        value = self.memory[self.getSP()]
        return value

    def pushValue(self, value):
        self.memory[self.getSP()] = value
        self.registers[SP] += 1
        

    def enter_frame(self):
        self.pushValue(self.registers[R0])
        self.pushValue(self.registers[R1])
        self.pushValue(self.registers[R2])
        self.pushValue(self.registers[R3])

    def leave_frame(self):
        self.registers[R3] = self.popValue()
        self.registers[R2] = self.popValue()
        self.registers[R1] = self.popValue()
        self.registers[R0] = self.popValue()

    def run(self):
        while self.ip <= len(self.memory):
            instruction = self.fetch()

            if instruction == LOAD: # load instruction
                # get operands
                dest = self.fetch()
                value = self.fetch()
                print(f"Loading {value} into R{dest}")
                if dest > len(self.registers):
                    print("Invalid register index")
                    continue
                # execute instruction
                self.registers[dest] = value

            elif instruction == DBG:
                print("DEBUG MODE")
                self.debug()
                break

            elif instruction == CMP:
                #get operands
                dest = self.fetch()
                src = self.fetch()
                if self.registers[dest] == self.registers[src]:
                    self.flags[ZF] = True

            elif instruction == MOV:
                dest = self.fetch()
                src = self.fetch()
                print(f"Moving R{src}({self.registers[src]}) into R{dest}")
                self.registers[dest] = self.registers[src]

            elif instruction == JMP:
                #get operands
                value = self.fetch()
                self.ip = value
                print(f"Jump to {value}")
                #input("Enter to continue..")
                #self.debug()

            elif instruction == RET:
                location = self.popValue()
                self.ip = location
                print(f"Returning to {location}")

            elif instruction == JNZ:
                #get operands
                location = self.fetch()
                if not self.flags[ZF]:
                    print(f"Jumping(NOT ZF) to {location}")
                    self.ip = location
                else:
                    pass

            elif instruction == JZ:
                #get operands
                location = self.fetch()
                if self.flags[ZF]:
                    print(f"Jumping(ZF) to {location}")
                    self.ip = location
                else:
                    pass

            elif instruction == ADD: # add instruction
                #get operands
                dest = self.fetch()
                src = self.fetch()
                sum = int(self.registers[dest]) + int(self.registers[src])
                print(f"Adding R{dest}({self.registers[dest]}) to R{value}({self.registers[src]})")
                self.registers[dest] = sum

            elif instruction == SUB:
                #get operands
                dest = self.fetch()
                src = self.fetch()
                sum = int(self.registers[dest]) - int(self.registers[src])
                print(f"Subtracting R{dest}({self.registers[dest]}) from R{src}({self.registers[src]})")
                if sum <= 0:
                    self.flags[ZF] = True
                    print("Zero flag was set")

                self.registers[dest] = sum

            elif instruction == PUSH: #push instruction
                #get operands
                value = self.fetch()
                self.memory[self.getSP()] = value
                print(f"Pushing {value}")
                self.registers[SP] += 1

            elif instruction == POP: #pop instruction
                #get operands
                dest = self.fetch()
                self.registers[SP] -= 1
                value = self.memory[self.getSP()]
                self.registers[dest] = value
                print(f"Popping value ({value})")
                


            elif instruction == PUSHR:
                #get operands
                dest = self.fetch()
                self.memory[self.getSP()] = self.registers[dest]
                print(f"Pushing register R{dest}({self.registers[dest]})")
                self.registers[SP] += 1


            elif instruction == BRK:
                print("Break")
                break

            elif instruction == ENTER:
                print("Enter Frame(Push all Registers)")
                self.enter_frame()
            elif instruction == LEAVE:
                print("Exit Frame (Pop all Registers)")
                self.leave_frame()
            else:
                print("Invalid instruction")
                break
        print("End of Memory was Reached")
            


program = [
    PUSH, 4,
    RET,
    DBG,
    BRK
]

vm = SimpleVM()
vm.load_program(program)
try:
    vm.run()
except IndexError:
    print("Err")
except KeyboardInterrupt:
    print("Control-C")
