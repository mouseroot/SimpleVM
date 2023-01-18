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
CALL - Execute function

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
DF - Direction Flag

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
CALL = 54
JE = 55
JNE = 56

CMP = 60
INC = 70
DEC = 71

ENTER = 90
LEAVE = 91
BRK = 99
DBG = 100
NOP = 255


opcodes = {
    LOAD: "Load",
    MOV: "Move",
    ADD: "Add",
    PUSH: "Push",
    PUSHR: "Push Register",
    POP: "Pop",
    JMP: "Jump",
    CALL: "Call",
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
    def __init__(self,memory_size=100,stack_location=75):
        self.memory = [0] * memory_size # 100 bytes of memory
        self.registers = [0] * 5 # 5 registers
        self.ip = 0 # instruction pointer
        self.registers[SP] = stack_location # stack pointer
        self.flags = [0] * 2
        self.verbose_debug = True


    def load_program(self, source):
        for i, instruction in enumerate(source):
            self.memory[i] = instruction

    def load_program_at(self, start_position, source):
        for i, instruction in enumerate(source):
            self.memory[start_position + i] = instruction

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
        for index, value in enumerate(self.memory[self.get_stackpointer()-1::-1]):
            print(f"{value:02} ",end="")
            if (index+1) % 8 == 0:
                print()
        print()
            

    def debug(self):
        print("Registers: ", self.registers)
        print("SP: ",self.get_stackpointer())
        self.print_flags()
        self.display_stack()

    def fetch(self):
        value = self.memory[self.ip]
        self.ip += 1
        return value

    def get_stackpointer(self):
        return self.registers[SP]

    def pop_value(self):
        self.registers[SP] -= 1
        value = self.memory[self.get_stackpointer()]
        return value

    def push_value(self, value):
        self.memory[self.get_stackpointer()] = value
        self.registers[SP] += 1
        

    def enter_frame(self):
        self.push_value(self.registers[R0])
        self.push_value(self.registers[R1])
        self.push_value(self.registers[R2])
        self.push_value(self.registers[R3])

    def leave_frame(self):
        self.registers[R3] = self.pop_value()
        self.registers[R2] = self.pop_value()
        self.registers[R1] = self.pop_value()
        self.registers[R0] = self.pop_value()

    def debug_prompt(self):
        while True:
            read_line = input(f"Debug:{self.ip}>")
            commands = read_line.split(" ")
            command = commands[0]
            if command == "continue" or command == "c":
                break
            elif command == "registers" or command == "r":
                print(f"Registers: {self.registers}")
            elif command == "stack" or command == "s":
                self.display_stack()
            else:
                print(f"Unknown command ({command})")

    def run(self):
        while self.ip < len(self.memory):
            instruction = self.fetch()

            if instruction == LOAD: # load instruction
                # get operands
                dest = self.fetch()
                value = self.fetch()
                if self.verbose_debug:
                    print(f"Loading {value} into R{dest}")
                # execute instruction
                self.registers[dest] = value

            elif instruction == DBG:
                print("DEBUG MODE")
                self.debug_prompt()

            elif instruction == CMP:
                #get operands
                dest = self.fetch()
                src = self.fetch()
                if self.verbose_debug:
                    print(f"Compare: R{dest} vs. R{src}")
                if self.registers[dest] == self.registers[src]:
                    self.flags[EF] = True
                    if self.verbose_debug:
                        print(f"CMP: EF Set")
                if self.registers[src] == 0:
                    self.flags[ZF] = True
                    if self.verbose_debug:
                        print(f"CMP ZF Set")

            elif instruction == MOV:
                dest = self.fetch()
                src = self.fetch()
                if self.verbose_debug:
                    print(f"Moving R{src}({self.registers[src]}) into R{dest}")
                self.registers[dest] = self.registers[src]

            elif instruction == JMP:
                #get operands
                value = self.fetch()
                self.ip = value
                if self.verbose_debug:
                    print(f"Jump to {value}")
                #input("Enter to continue..")
                #self.debug()

            elif instruction == CALL:
                #get operands
                self.push_value(self.ip+1) #store IP + 2 on stack
                location = self.fetch()
                self.ip = location
                if self.verbose_debug:
                    print(f"Calling function at {location}")
                

            elif instruction == NOP:
                pass

            elif instruction == RET:
                location = self.pop_value()
                self.ip = location
                if self.verbose_debug:
                    print(f"Returning to {location}")

            elif instruction == JNZ:
                #get operands
                location = self.fetch()
                if not self.flags[ZF]:
                    if self.verbose_debug:
                        print(f"Jumping(Not ZF) to {location}")
                    self.ip = location
                else:
                    pass

            elif instruction == JZ:
                #get operands
                location = self.fetch()
                if self.flags[ZF]:
                    if self.verbose_debug:
                        print(f"Jumping(ZF) to {location}")
                    self.ip = location
                else:
                    pass

            elif instruction == JE:
                #get operands
                location = self.fetch()
                if self.flags[EF]:
                    if self.verbose_debug:
                        print(f"Jumping (EF) to {location}")
                    self.ip = location
                else:
                    pass

            elif instruction == JNE:
                #get operands
                pos = self.fetch()
                if not self.flags[EF]:
                    if self.verbose_debug:
                        print(f"Jumping (Not EF) to {pos}")
                    self.ip = pos
                else:
                    pass

            elif instruction == INC:
                #get operands
                dest = self.fetch()
                self.registers[dest] += 1
                if self.verbose_debug:
                    print(f"increase R{dest}")

            elif instruction == DEC:
                #get operands
                dest = self.fetch()
                self.registers[dest] -= 1
                if self.verbose_debug:
                    print(f"decrease R{dest}")

            elif instruction == ADD: # add instruction
                #get operands
                dest = self.fetch()
                src = self.fetch()
                calc = int(self.registers[dest]) + int(self.registers[src])
                if self.verbose_debug:
                    print(f"Adding R{dest}({self.registers[dest]}) to R{value}({self.registers[src]})")
                self.registers[dest] = calc

            elif instruction == SUB:
                #get operands
                dest = self.fetch()
                src = self.fetch()
                calc = int(self.registers[dest]) - int(self.registers[src])
                if self.verbose_debug:
                    print(f"Subtracting R{dest}({self.registers[dest]}) from R{src}({self.registers[src]})")
                if calc <= 0:
                    self.flags[ZF] = True
                    if self.verbose_debug:
                        print("Zero flag was set")
                self.registers[dest] = calc

            elif instruction == PUSH: #push instruction
                #get operands
                value = self.fetch()
                self.memory[self.get_stackpointer()] = value
                if self.verbose_debug:
                    print(f"Pushing {value}")
                self.registers[SP] += 1

            elif instruction == POP: #pop instruction
                #get operands
                dest = self.fetch()
                self.registers[SP] -= 1
                value = self.memory[self.get_stackpointer()]
                self.registers[dest] = value
                if self.verbose_debug:
                    print(f"Popping value ({value})")
                
            elif instruction == PUSHR:
                #get operands
                dest = self.fetch()
                self.memory[self.get_stackpointer()] = self.registers[dest]
                if self.verbose_debug:
                    print(f"Pushing register R{dest}({self.registers[dest]})")
                self.registers[SP] += 1


            elif instruction == BRK:
                if self.verbose_debug:
                    print("Break")
                break

            elif instruction == ENTER:
                if self.verbose_debug:
                    print("Enter Frame(Push all Registers)")
                self.enter_frame()

            elif instruction == LEAVE:
                if self.verbose_debug:
                    print("Exit Frame (Pop all Registers)")
                self.leave_frame()
            else:
                if self.verbose_debug:
                    print("Invalid instruction")
                break
        print("End of Memory was Reached")
            


program = [
    LOAD, R0, 0, 
    LOAD, R1, 5,
    INC, R0,
    CMP, R0, R1, #if R0 == R1
    JE,15,       # jump to 300(func_program)
    JNE,6,       # else jump to INC
    CALL, 300,
    DBG,
    BRK
]

func_program = [
    ENTER,
    LOAD, R3, 45,
    DBG,
    LEAVE,
    RET
]


vm = SimpleVM(memory_size=1024,stack_location=900)
vm.load_program(program)
vm.load_program_at(300,func_program)
vm.verbose_debug = True
try:
    vm.run()
except IndexError:
    print("Err")
except KeyboardInterrupt:
    print("Control-C")
