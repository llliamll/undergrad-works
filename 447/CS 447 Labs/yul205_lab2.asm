#Yuanyi Li
#yul205

# THIS MACRO WILL OVERWRITE WHATEVER IS IN THE a0 AND v0 REGISTERS.
.eqv INPUT_SIZE 3

.macro print_str %str
	.data
	print_str_message: .asciiz %str
	.text
	la	a0, print_str_message
	li	v0, 4
	syscall
.end_macro

.data 
	display: .
	input: .space INPUT_SIZE
.text

.globl main
main: