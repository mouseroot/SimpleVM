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
CDF = 92
CLF = 93
BRK = 99
DBG = 100
NOP = 255
IR = 7

PRINT_CHAR = 1
PRINT_STRING = 2

READ_LINE = 3

opcodes = {
    LOAD: "Load",
    MOV: "Move",
    ADD: "Add",
    SUB: "Sub",
    INC: "Increase",
    DEC: "Decrease",
    BRK: "Break",
    IR: "Interrupt",

    DBG: "Debug",
    CMP: "Compare",
    JMP: "Jump",
    JZ: "Jump if Zero",
    JNZ: "Jump if Not Zero",
    JE: "Jump if Equal",
    JNE: "Jump if Not Equal",

    PUSH: "Push",
    PUSHR: "Push Register",
    POP: "Pop",

    CALL: "Call",
    RET: "Return",
    ENTER: "Enter Frame",
    LEAVE: "Leave Frame",

    CDF: "Change Direction Flag",
    CLF: "Clear Flags"
}

R0 = 0
R1 = 1
R2 = 2
R3 = 3
SP = 4

NULL = 0

EF = EQUAL_FLAG =  0 #equal flag
ZF = ZERO_FLAG =  1 #zero flag
DF = DIR_FLAG =  2 #direction flag





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

    def write_string_at(self, pos, string):
        for i,s in enumerate(string):
            self.memory[pos + i] = ord(s)

    def display_memory(self):
        print("Memory: ")
        for index,value in enumerate(self.memory):
            print(f"{value:02} ",end="")
            if (index+1) % 3 == 0:
                print()
        print()

    def fill_memory(self, value):
        for i in range(len(self.memory)):
            if type(value) == str:
                self.memory[i] = ord(value)
            elif type(value) == int:
                self.memory[i] = value

    def call_interupt(self, interupt_id):
        if interupt_id == PRINT_CHAR:
            ch = self.memory[self.get_stackpointer()]
            print(chr(ch),end='')
        elif interupt_id == PRINT_STRING:
            i = 0
            ch = self.memory[self.get_stackpointer() + i]
            while ch != NULL:
                ch = self.memory[self.get_stackpointer() + i]
                print(chr(ch),end='')
                i += 1
            print()
        elif interupt_id == READ_LINE:
            input_line = input("? ")
            self.write_string_at(self.get_stackpointer(),input_line)
            self.registers[SP] += len(input_line)
            self.memory[self.get_stackpointer()] = NULL
            self.registers[SP] += 1


    def print_flags(self):
        print("Flags: ")
        print("Zero: ",self.flags[ZF])
        print("Equal: ",self.flags[EF])
        print("Direction: ", self.flags[DF])

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

            elif instruction == IR:
                i_id = self.fetch()
                self.call_interupt(i_id)
                if self.verbose_debug:
                    print(f"Intterupt {i_id}")

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
                #get operand
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
    MOV, R0, SP,        # Move the stack pointer into R0
    IR,READ_LINE,       # Read input
    MOV, SP, R0,        # Restore stack pointer from R0
    IR, PRINT_STRING,   # Call print string
    MOV, SP, R0,        # Restore again
    DBG,
    BRK
]

func_program = [
    ENTER,
    LOAD, R3, 45,
    NOP,
    LEAVE,
    RET
]


vm = SimpleVM(memory_size=1024,stack_location=700)
vm.fill_memory(NOP)
#vm.load_program(program)
#vm.load_program_at(300,func_program)
vm.load_program(program)
#vm.write_string_at(150,"SimpleVM")

vm.verbose_debug = False
vm.run()