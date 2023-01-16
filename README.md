# SimpleVM

A very basic Virtual Machine written in python

---
LOAD - Load a value

MOV - Move register A into B

ADD - Add registers

SUB - Subtract registers

PUSH - Push immediate value

PUSHR - Push register

POP - Pop value off stack into register

JMP - Jump to location

RET - Jump to location at sp

JZ - Jump if Zero Flag set

JNZ - Jump if Zero Flag not set

CMP - Compare registers and set zero flag

INC - Increase register

DEC - Decrease register

ENTER - push all registers

LEAVE - pop all registers

BRK - Break

DBG - Print Debug info

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
