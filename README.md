# SimpleVM

A very basic Virtual Machine written in python

## Basic instruction Set
---
LOAD - Load a value
```
    load R0,100
```

MOV - Move register A into B
```
    mov R0, R1
```
ADD - Add registers
```
    add R0, R1
```
SUB - Subtract registers
```
    sub R0, R1
```
INC - Increase register
```
    inc R0
```
DEC - Decrease register
```
    dec R2
```
BRK - Break
```
    brk
```
DBG - Print Debug info
```
    dbg
```

## Conditional Instrucutions
---
JMP - Jump to location
```
    jmp 231
```
JZ - Jump if Zero Flag set
```
    jz 124
```
JNZ - Jump if Zero Flag not set
```
    jnz 122
```
CMP - Compare registers and set zero flag
```
    cmp R0,R3
```


## Subroutine instructions
---
ENTER - push all registers
```
    enter
    ...
```
LEAVE - pop all registers
```
    ...
    leave
```
CALL - Runs a function and returns to the location from where it was called from.
```
    call 456
```
RET - Jump to location at sp
```
    ...
    ret
```
## Stack instructions
---
PUSH - Push immediate value
```
    push 1337
```
PUSHR - Push register
```
    pushr R0
```
POP - Pop value off stack into register
```
    pop R0
```
# Registers

R0 - Register 0

R1 - Register 1

R2 - Register 2

R3 - Register 3

SP - Stack Pointer


# Flags:

EF - Equal Flag

ZF - Zero Flag

DF - Direction Flag

# Examples:


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
