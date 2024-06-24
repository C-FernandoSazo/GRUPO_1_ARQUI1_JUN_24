.global _start
.bss
input: .space 100
.text
_start:
    mov x0, 0
    ldr x1, =input
    mov x2, 100
    mov x8, 63
    svc 0

    mov x3, 0
    mov x4, 0
    mov x5, 0
    ldr x0, =input

bucle_suma:
    ldrb w1, [x0], 1
    cmp w1, 44
    beq sumar_numero
    cmp w1, 10
    beq fin
    sub w1, w1, 48
    mov w2, w4
    mov w4, 10
    mul w2, w2, w4
    add w4, w2, w1
    b bucle_suma

sumar_numero:
    add x3, x3, x4
    mov x4, 0
    add x5, x5, 1
    b bucle_suma

fin:
    add x3, x3, x4
    add x5, x5, 1
    udiv x0, x3, x5

    mov x8, 93
    svc 0

    mov x8, 94
    svc 0
    
