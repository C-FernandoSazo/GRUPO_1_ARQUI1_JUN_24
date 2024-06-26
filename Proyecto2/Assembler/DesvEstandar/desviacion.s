.section .data
input_file: .asciz "entradaBaro.txt"
output_file: .asciz "Resul_des_bar.txt"
buffer: .space 1024
buffer2: .space 256
numbers: .space 1024
count: .quad 0
sum: .quad 0
newline: .asciz "\n"

.section .text
.global _start

_start:
    mov r0, #-100
    ldr r1, =input_file
    mov r2, #0
    mov r7, #5
    swi 0
    cmp r0, #0
    moveq r0, #-1
    beq error
    mov r9, r0

    mov r0, r9
    ldr r1, =buffer
    mov r2, #1024
    mov r7, #3
    swi 0
    cmp r0, #0
    moveq r0, #-1
    beq error
    mov r10, r0

    mov r6, #0
    ldr r5, =numbers
    mov r4, #0
    ldr r1, =buffer

parse_loop:
    mov r0, r1
    bl atoi
    cmp r0, #-1
    beq parse_end
    str r0, [r5, r4, LSL #2]
    add r4, r4, #1
    add r6, r6, r0
    ldrb r2, [r1], #1
    cmp r2, #','
    beq parse_loop
    cmp r2, #0
    bne parse_loop

parse_end:
    ldr r3, =sum
    str r6, [r3]
    ldr r3, =count
    str r4, [r3]

    mov r3, #10
    mul r6, r6, r3
    bl divide
    mov r3, #0
    mov r4, #0

calc_variance_loop:
    ldr r2, [r5, r4, LSL #2]
    mul r2, r2, #10
    sub r2, r2, r6
    mul r2, r2, r2
    add r3, r3, r2
    add r4, r4, #1
    cmp r4, r6
    blt calc_variance_loop

    sub r6, r6, #1
    bl divide

    mov r0, r3
    bl sqrt

    ldr r1, =buffer2
    bl itoa_fixed_point

    mov r0, #-100
    ldr r1, =output_file
    mov r2, #577
    mov r3, #644
    mov r7, #5
    swi 0
    cmp r0, #0
    moveq r0, #-1
    beq error
    mov r8, r0

    mov r0, r8
    ldr r1, =buffer2
    bl write_string

    mov r0, r8
    ldr r1, =newline
    bl write_string

    mov r0, r9
    mov r7, #6
    swi 0

    mov r0, r8
    mov r7, #6
    swi 0

    mov r0, #0
    mov r7, #1
    swi 0

error:
    mov r0, #-1
    mov r7, #1
    swi 0
