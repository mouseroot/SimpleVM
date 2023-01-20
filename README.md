# SimpleVM

A very basic Virtual Machine written in python

## Basic instruction Set
Instructions are read as the following:
- INSTRUCTION A,B
- INSTRUCTION A
- INSTRUCTION

---
LOAD 
- Loads an immediate(integer) value into the specified register
```
    load R0,100
```

MOV 
- Move register B into A
- Copies the value from B
- Stores the value into A
```
    mov R0, R1
```
ADD 
- Adds two registers together
- (A = A + B)
- Stores the sum into A 
```
    add R0, R1
```
SUB 
- Subtracts two registers
- (A = A - B)
- Store the sum into A
```
    sub R0, R1
```
MUL
- Multiply two registers
- (A = A * B)
- Store the sum into A
```
    mul R0,R2
```
INC 
- Increase register by 1
```
    inc R0
```
DEC 
- Decrease register by 1
```
    dec R2
```
BRK 
- Stops execution by breaking out of the main loop
```
    brk
```
DBG 
- Drop into debug shell
```
    dbg
```
IR 
- Invoke interrupt
```
    IR PRINT_STRING
```

## Conditional Instrucutions
---
JMP 
- Jump to location
- Sets IP to the location
```
    jmp 231
```
JZ 
- Jump if Zero Flag set
```
    jz 124
```
JNZ 
- Jump if Zero Flag not set
```
    jnz 122
```
JE 
- Jump if Equal Flag set
```
    je 312
```
JNE 
- Jump if Equal Flag not set
```
    jne 130
```
CMP 
- Compare registers and set zero flag and equal flag
- Checks if the registers are equal
```
    cmp R0,R3
```


## Subroutine instructions
---
CALL 
- Runs a function and returns to the location from where it was called from
- stores the location AFTER the call to the memory location the stack pointer is pointing to
```
    call 456
```
RET 
- Jump to location at stack pointer
```
    ...
    ret
```
## Stack instructions
---
PUSH 
- Push immediate value
```
    push 1337
```
PUSHR
 - Push register
```
    pushr R0
```
POP 
- Pop value off stack into register
```
    pop R0
```

## Flag Instructions
---
CDF 
- Change Direction Flag
```
    CDF 0
```
CLF 
- Clear Flags
```
    CLF
```

# Registers

R0 
- Register 0 or A
```
    A general purpose register
```

R1 
- Register 1 or B
```
    A general purpose register
```
R2 
- Register 2 or C
```
    GPR, Counter
```

R3 
- Register 3 or D
```
    GPR, Return Value
```
SP 
- Stack Pointer
```
    Stack Pointer only
```
IP
- Instruction Pointer
```
    The location in memory the program is currently reading from
    Cannot be modified using MOV or LOAD instructions,
    
    JMP sets the IP to the Operand and is one of the only ways of
    directly setting the IP
```

# Flags

EF 
- Equal Flag
```
    Set by the CMP instruction
    
    This is used to determine if a conditional jump is made or not
```
ZF 
- Zero Flag
```
    Set by the CMP and DEC instructions
    
    This is used to determine if a conditional jump is made or not
```

DF 
- Direction Flag
```
    Set by the CDF instruction (Change Direction Flag)
    
    Used by read instructions to determine how the data is read
    0 or False - Forward ++
    1 or True - Backwards --
```

# Interrupts

Interrupts are system calls or built in functions that include but are not limited to:
- writing to the screen
- reading input
- opening, reading and checking if files exist
- sockets
- requests
- raw exec

## 01 - PRINT_CHAR 
- Prints the character at the memory location the stack pointer is pointing to.
- Does NOT incriment the stack pointer

## 02 - PRINT_STRING 
- Prints chars to the screen at the memory location the stack pointer is pointing to
- increments untill a NULL value is found
- a newline character is printed to terminate the string

## 03 - READ_LINE 
- Reads a line from standard input, this includes spaces, up to and NOT including the newline character, 
- the string is then written to the memory location the stack pointer is pointer to
- the stack pointer is increased by the length of the string.

# Debug Functions
When the DBG instruction is read the virtual machine drops into a command line shell which allows you to:
- Show registers - r or registers
- Show stack - s or stack
- Continue execution - c or continue
- Step execution - st or step
- Dump memory to file - d or dump <filename>

```
    DEBUG MODE
    Debug:11>
```
The command line shows the current instruction pointer and which mode the VM is currently in
# Examples


### A simple loop
```python
    program = [
        LOAD, R0, 0,  # R0 = 0
        LOAD, R1, 5,  # R1 = 5
        INC,  R0,     # R0++
        CMP,  R0, R1, # if R0 == R1 
        JE,   15,     # jump to end
        JNE,  6,      # else jump to R0++
        BRK
    ]


    vm = SimpleVM(memory_size=1024, stack_location=500)
    vm.load_program(program)
    vm.run()

```

### Calling a function
```python

    program = [
        LOAD, R0, 0, 
        LOAD, R1, 5,
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
    vm.run()
```

### Using Interrupts to Read and Print strings
```python
    program = [
        MOV, R0, SP,        # Move the stack pointer into R0
        IR,READ_LINE,       # Read input
        MOV, SP, R0,        # Restore stack pointer from R0
        IR, PRINT_STRING,   # Call print string
        DBG,
        BRK
    ]

    vm = SimpleVM(memory_size=1024,stack_location=255)
    vm.load_program(program)
    vm.run()
```