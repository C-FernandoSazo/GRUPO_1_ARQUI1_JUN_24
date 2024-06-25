.global _start

.bss
input: .space 1000

.text
_start:
    mov x0, 0
    ldr x1, =input
    mov x2, 1000
    mov x8, 63
    svc 0
    mov x3, 0      
    mov x4, 0      
    ldr x0, =input

bucle_lectura:
    ldrb w1, [x0], 1
    cmp w1, 44      
    beq procesar_numero
    cmp w1, 10     
    beq fin
    sub w1, w1, 48  
    mov x2, x3
    mov x3, 10
    mul x2, x2, x3
    add x3, x2, x1
    b bucle_lectura

procesar_numero:
    cmp x3, x4
    bgt actualizar_mayor
    mov x3, 0
    b bucle_lectura

actualizar_mayor:
    mov x4, x3
    mov x3, 0
    b bucle_lectura

fin:
    cmp x3, x4
    bgt actualizar_mayor_final
    b salir

actualizar_mayor_final:
    mov x4, x3

salir:
    mov x0, x4
    mov x8, 93
    svc 0
    