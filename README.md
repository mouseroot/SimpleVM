# SimpleVM

A very basic Virtual Machine written in python

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
```assembler
    add R0, R1
```
SUB - Subtract registers
```
    sub R0, R1
```
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
JMP - Jump to location
```
    jmp 231
```
RET - Jump to location at sp
```
    ...
    ret
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
INC - Increase registerrom it being called.
```
    inc R0
```
DEC - Decrease register
```
    dec R2
```
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
BRK - Break
```
    brk
```
DBG - Print Debug info
```
    dbg
```
CALL - Runs a function and returns to the location from where it was called from.
```
    call 456
```
Registers
----
R0 - Register 0

R1 - Register 1

R2 - Register 2

R3 - Register 3

SP - Stack Pointer


Flags:
-------
EF - Equal Flag

ZF - Zero Flag

DF - Direction Flag
