.global _start
.bss
input: .space 1024

.text
_start:
    mov x0, 0
    ldr x1, =input
    mov x2, 1024
    mov x8, 63
    svc 0

    mov x3, 0
    mov x4, 0
    ldr x0, =input

leer_numeros:
    ldrb w1, [x0], 1
    cmp w1, 44
    beq comparar_numero
    cmp w1, 10
    beq fin
    sub w1, w1, 48
    mov w2, w4
    mov w4, 10
    mul w2, w2, w4
    add w4, w2, w1
    b leer_numeros

comparar_numero:
    cmp w4, 0
    beq incrementar
reiniciar:
    mov w4, 0
    b leer_numeros

incrementar:
    add x3, x3, 1
    b reiniciar

fin:
    cmp w4, 0
    beq incrementar_fin
    b salir

incrementar_fin:
    add x3, x3, 1

salir:
    mov x0, x3
    mov x8, 93
    svc 0
