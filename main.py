"""

VM Overview
---------------------------
LOAD - Load a value
MOV - Move register A into B
ADD - Add registers
SUB - Subtract registers
MUL - Multiply registers
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
R1 - Register 0
R2 - Register 1
R3 - Register 2
R4 - Register 3
AC - Accumulator
R5 - Register A
R6 - Register B
R7 - Register C
R8 - Register D

FP - Frame Pointer
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

LOAD = 2    # load imm to registers
LOADM = 3   # loadm imm to memory

MOV = 11    # mov register,register
MOVM = 12   # movm memory
MOVMM = 13  # movmm memory,memory

ADD = 20    # add register,register
ADDI = 21   # addi register,imm

SUB = 22    # sub register,register
SUBI = 23   # subi register,imm

MUL = 24    # mul register,register
MULI = 25   # muli register,imm

PUSH = 30   # push imm
PUSHR = 31  # pushr register
PUSHM = 32  # pushm memory

POP = 40    # pop register
POPM = 41   # popm memory

JMP = 50    # jmp imm
JMPR = 51   # jmpr register
RET = 52    # ret

JZ = 53     # jz imm
JNZ = 54    # jnz imm
CALL = 55   # call imm
JE = 56     # je imm
JNE = 57    # jne imm

CMP = 60    # cmp register,register

INC = 70    # inc imm
DEC = 71    # dec imm

CDF = 92    # cdf
CLF = 93    # clf
BRK = 99    # brk
DBG = 100   # dbg
HLT = 101   # hlt
NOP = 255   # nop
IR = 7      # ir

PRINT_CHAR = 1
PRINT_STRING = 2

READ_LINE = 3

STRING_COMPARE = 4

opcodes = {
    LOAD: "Load",
    MOV: "Move",
    ADD: "Add",
    SUB: "Sub",
    MUL: "Mul",
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

    CDF: "Change Direction Flag",
    CLF: "Clear Flags"
}

AC = 0
R1 = 1
R2 = 2
R3 = 3
R4 = 4

R5 = 5
R6 = 6
R7 = 7
R8 = 8

SP = 9
FP = 10

NULL = 0


EF = EQUAL_FLAG =  0 #equal flag
ZF = ZERO_FLAG =  1 #zero flag
DF = DIR_FLAG =  2 #direction flag





class SimpleVM:
    def __init__(self,memory_size=100,stack_location=75):
        self.memory = [0] * memory_size # 100 bytes of memory
        self.registers = [0] * 11 # 10 registers
        self.ip = 0 # instruction pointer
        self.registers[SP] = stack_location # stack pointer
        self.registers[FP] = self.registers[SP]
        self.flags = [0] * 3
        self.verbose_debug = True
        self.frame_size = 0


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

    def read_string(self, address):
        return_str = ""
        i = 0
        ch = self.memory[address]
        while ch != NULL:
            ch = self.memory[address + i]
            i += 1
            return_str += ch
        return return_str
        

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
        elif interupt_id == STRING_COMPARE:
            strA = ""
            strB = ""


    def print_flags(self):
        print("Flags: ")
        print("Zero: ",self.flags[ZF])
        print("Equal: ",self.flags[EF])
        print("Direction: ", self.flags[DF])

    def display_stack(self):
        print("Stack: ")
        for index, value in enumerate(self.memory[self.get_stackpointer()-1:self.get_stackpointer()-50:-1]):
            print(f"{value:02} ",end="")
            if (index+1) % 8 == 0:
                print()
        print()
            

    def debug(self):
        print("Registers: ", self.registers)
        print("SP: ",self.get_stackpointer())
        print("FP", self.registers[FP])
        self.print_flags()
        self.display_stack()

    def fetch(self):
        value = self.memory[self.ip]
        self.ip += 1
        return value

    def get_stackpointer(self):
        return self.registers[SP]

    def get_framepointer(self):
        return self.registers[FP]

    def pop_value(self):
        self.registers[SP] -= 1
        value = self.memory[self.get_stackpointer()]
        self.frame_size -= 1
        return value

    def preview_pop(self):
        return self.memory[self.get_stackpointer() + 1]

    def push_value(self, value):
        self.memory[self.get_stackpointer()] = value
        self.registers[SP] += 1
        self.frame_size += 1
        

    def push_state(self):
        if self.verbose_debug:
            print(f"Push State")
        self.push_value(self.registers[R1])
        self.push_value(self.registers[R2])
        self.push_value(self.registers[R3])
        self.push_value(self.registers[R4])
        self.push_value(self.registers[R5])
        self.push_value(self.registers[R6])
        self.push_value(self.registers[R7])
        self.push_value(self.registers[R8])
        instruction_pointer = self.ip
        self.push_value(instruction_pointer)
        if self.verbose_debug:
            print(f"ip: ",instruction_pointer)
        nFrameSize = self.frame_size
        self.push_value(nFrameSize)
        if self.verbose_debug:
            print(f"frame size: ", nFrameSize)
        self.registers[FP] = self.registers[SP]
        self.frame_size = 0


    def pop_state(self):
        if self.verbose_debug:
            print(f"Pop State")
        fpAddres = self.registers[FP]
        self.registers[SP] = fpAddres
        nFrameSize = self.pop_value()
        self.frame_size = nFrameSize
        if self.verbose_debug:
            print("frame size: ",nFrameSize)

        nIP = self.pop_value()
        self.ip = nIP
        if self.verbose_debug:
            print("ip: ",nIP)
        self.registers[R8] = self.pop_value()
        self.registers[R7] = self.pop_value()
        self.registers[R6] = self.pop_value()
        self.registers[R5] = self.pop_value()
        self.registers[R4] = self.pop_value()
        self.registers[R3] = self.pop_value()
        self.registers[R2] = self.pop_value()
        self.registers[R1] = self.pop_value()
        self.registers[FP] = int(fpAddres + nFrameSize + 2)
        nArgs = self.pop_value()
        if self.verbose_debug:
            print(f"args: {nArgs}")
        for i in range(nArgs):
            pValue = self.pop_value()
            if self.verbose_debug:
                print(f"Popping Var: {pValue}")

    def debug_prompt(self):
        while True:
            read_line = input(f"Debug:{self.ip}>")
            commands = read_line.split(" ")
            command = commands[0]
            
            if command == "continue" or command == "c":
                break
            elif command == "registers" or command == "r":
                print("Registers:")
                try:
                    print(f"IP: {self.ip} -> {opcodes[self.ip]}")
                except KeyError:
                    print(f"IP: {self.ip} -> {self.memory[self.ip]}")
                print(f"R1: {self.registers[R1]}")
                print(f"R2: {self.registers[R2]}")
                print(f"R3: {self.registers[R3]}")
                print(f"R4: {self.registers[R4]}")
                print(f"R5: {self.registers[R5]}")
                print(f"R6: {self.registers[R6]}")
                print(f"R7: {self.registers[R7]}")
                print(f"R8: {self.registers[R8]}")
                print(f"AC: {self.registers[AC]}")
                print(f"SP: {self.registers[SP]} -> {self.memory[self.get_stackpointer()]}")
                print(f"FP: {self.registers[FP]} -> {self.memory[self.registers[FP]]}")

            elif command == "frame" or command == "f":
                print("Frame Size: ",self.frame_size)
                print("Frame Pointer: ", self.registers[FP])
                fp = self.registers[FP]
                for index, item in enumerate(self.memory[fp:fp + self.frame_size]):
                    print(f"Frame+{index}: {item}")

            elif command == "stack" or command == "s":
                sp = self.get_stackpointer()
                print("Stack Pointer: ",sp)
                print(self.memory[sp:sp+7])
                
            elif command == "memory" or command == "m":
                if len(command) >= 2:
                    arg = int(commands[1])
                    print(self.memory[arg:arg+10])
                else:
                    print(self.memory)
            elif command == "quit" or command == "q":
                self.ip = len(self.memory)
                break
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
            
            elif instruction == LOADM:
                mem = self.fetch()
                value = self.fetch()
                self.memory[mem] = value
                if self.verbose_debug:
                    print(f"Loading {value} into memory {mem}")

            elif instruction == DBG:
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
                location = self.fetch()
                if self.verbose_debug:
                    print(f"Calling function at {location}")
                self.push_state()
                self.ip = location

                

            elif instruction == NOP:
                pass

            elif instruction == RET:
                self.pop_state()
                return_ip = self.ip
                if self.verbose_debug:
                    print(f"Returning to {return_ip}")

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
                self.registers[AC] = calc

            elif instruction == ADDI:
                dest = self.fetch()
                value = self.fetch()
                calc = int(self.registers[dest]) + value
                self.registers[AC] = calc

            elif instruction == SUB:
                #get operands
                dest = self.fetch()
                src = self.fetch()
                calc = int(self.registers[dest]) - int(self.registers[src])
                if self.verbose_debug:
                    print(f"Subtracting R{dest}({self.registers[dest]}) from R{src}({self.registers[src]})")
                self.registers[AC] = calc

            elif instruction == SUBI:
                #get operands
                dest = self.fetch()
                value = self.fetch()
                calc = int(self.registers[dest]) + value
                self.registers[AC] = calc

            elif instruction == MUL:
                dest = self.fetch()
                src = self.fetch()
                calc = int(self.registers[dest]) * int(self.registers[src])
                if self.verbose_debug:
                    print(f"Miltiply R{dest} with R{src}")
                self.registers[AC] = calc

            elif instruction == MULI:
                dest = self.fetch()
                value = self.fetch()
                calc = int(self.registers[dest]) * value
                self.registers[AC] = calc


            elif instruction == PUSH: #push instruction
                #get operands
                value = self.fetch()
                self.push_value(value)
                if self.verbose_debug:
                    print(f"Pushing {value}")
            
            elif instruction == PUSHM:
                mem = self.fetch()
                value = self.memory[mem]
                self.push_value(value)
                if self.verbose_debug:
                    print(f"Pushing memory {mem} -> {value}")

            elif instruction == POP: #pop instruction
                #get operands
                dest = self.fetch()
                value = self.pop_value()
                self.registers[dest] = value
                if self.verbose_debug:
                    print(f"Popping value ({value}) into R{dest}")
                
            elif instruction == PUSHR:
                #get operand
                dest = self.fetch()
                self.push_value(self.registers[dest])
                if self.verbose_debug:
                    print(f"Pushing register R{dest}({self.registers[dest]})")

            elif instruction == BRK:
                if self.verbose_debug:
                    print("Break")
                break
            else:
                if self.verbose_debug:
                    print("Invalid instruction")
                break
        print("End of Memory was Reached")
            


program = [
    LOAD, R2, 2,
    INC, R2,
    CALL, 300,
    DBG,
    JMP, 3,
    BRK,

]

func_program = [
    POP, R4,
    DBG,
    RET
]


vm = SimpleVM(memory_size=1000,stack_location=500)
#vm.fill_memory(NOP)
#vm.load_program(program)
vm.load_program_at(300,func_program)
vm.load_program(program)
#vm.write_string_at(150,"SimpleVM")

vm.verbose_debug = True
vm.run()