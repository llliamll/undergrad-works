# Yuanyi Li
# yul205

.include "macros.asm"

.data
# maps from ASCII to MIDI note numbers, or -1 if invalid.
key_to_note_table: .byte
	-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
	-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
	-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 60 -1 -1 -1
	75 -1 61 63 -1 66 68 70 -1 73 -1 -1 -1 -1 -1 -1
	-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
	-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
	-1 -1 55 52 51 64 -1 54 56 72 58 -1 -1 59 57 74
	76 60 65 49 67 71 53 62 50 69 48 -1 -1 -1 -1 -1

demo_notes: .byte
	67 67 64 67 69 67 64 64 62 64 62
	67 67 64 67 69 67 64 62 62 64 62 60
	60 60 64 67 72 69 69 72 69 67
	67 67 64 67 69 67 64 62 64 65 64 62 60
	-1

demo_times: .word
	250 250 250 250 250 250 500 250 750 250 750
	250 250 250 250 250 250 500 375 125 250 250 1000
	375 125 250 250 1000 375 125 250 250 1000
	250 250 250 250 250 250 500 250 125 125 250 250 1000
	0

input: .space 3
.text

# -----------------------------------------------

.globl main
main:
	
	li a2, 0 #grand piano as default instrument
	main_loop:
		print_str "[k]eyboard,[d]emo,[r]ecord,[p]lay,[q]uit: "
		
		la a0, input
		li a1, 3
		li v0, 8
		syscall

		lb t0, input

		beq t0, 'q', _quit
		beq t0, 'k', _case
		beq t0, 'd', _case
		beq t0, 'r', _case
		beq t0, 'p', _case
		print_str "Not a valid command!\n"
		
		j main_loop

	li v0, 10
	syscall

# -----------------------------------------------
#case switch
_case:
			beq t0, 'k', _case_keyboard
			beq t0, 'd', _case_demo
			beq t0, 'r', _case_record
			beq t0, 'p', _case_play_record

			_case_keyboard:
				jal keyboard
				j main_loop
			_case_demo:
				jal demo
				j main_loop
			_case_record:
				jal record
				j main_loop
			_case_play_record:
				jal play_record
				j main_loop

_quit:
	li v0, 10
	syscall
# -----------------------------------------------
#keyboard & its functions
keyboard:
push ra

	_keyboard_loop:
		la a0, input
		li v0, 12
		syscall
		beq v0, '\n', _loop_exit
		jal play_note
	j _keyboard_loop

_loop_exit:
pop ra
jr ra

play_note:
push ra
push s0
push s1
push s2
push s3

	move s0, a0
	li s1, 500
	move s2, a2
	li s3, 100

	move a0, s0
	move a1, s1
	move a2, s2
	move a3, s3
	li v0, 31
	syscall

pop s3
pop s2
pop s1
pop s0
pop ra
jr ra

translate_note:
push ra
push s0
push s1
	
	lb s0, a0
	blt s0, 0, _invalid
	blt s0, 127, _valid

	_invalid:
		print_str "invalid"
		j _end_function
	_valid:
		jal key_to_note_table

_end_function:
pop s1
pop s0
pop ra
jr ra
# -----------------------------------------------
#demo & its functions
demo:
push ra

print_str "demo not implemented\n"

pop ra
jr ra
# -----------------------------------------------
#record & its functions
record:
push ra

print_str "record not implemented\n"

pop ra
jr ra
# -----------------------------------------------
#play record & its functions
play_record:
push ra

print_str "play record not implemented\n"

pop ra
jr ra

