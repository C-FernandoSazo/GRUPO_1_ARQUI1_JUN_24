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
    mov x5, 0x7FFFFFFFFFFFFFFF
    ldr x0, =input

bucle_lectura:
    ldrb w1, [x0], 1
    cmp w1, 44
    beq procesar_numero
    cmp w1, 10
    beq fin
    sub w1, w1, 48
    mov w2, w4
    mov w4, 10
    mul w2, w2, w4
    add w4, w2, w1
    b bucle_lectura

procesar_numero:
    cmp x4, x5
    blt actualizar_menor
    mov x4, 0
    b bucle_lectura

actualizar_menor:
    mov x5, x4
    mov x4, 0
    b bucle_lectura

fin:
    cmp x4, x5
    blt actualizar_menor_final
    b salir

actualizar_menor_final:
    mov x5, x4

salir:
    mov x0, x5
    mov x8, 93
    svc 0
    
