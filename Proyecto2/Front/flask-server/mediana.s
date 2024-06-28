.global _start
.bss
input: .space 1024
numeros: .space 1024

.text
_start:
    mov x0, 0
    ldr x1, =input
    mov x2, 1024
    mov x8, 63
    svc 0

    mov x4, 0
    mov x5, 0
    ldr x0, =input
    ldr x1, =numeros

leer_numeros:
    ldrb w2, [x0], 1
    cmp w2, 44
    beq guardar_numero
    cmp w2, 10
    beq ordenar
    sub w2, w2, 48
    mov w3, w4
    mov w4, 10
    mul w3, w3, w4
    add w4, w3, w2
    b leer_numeros

guardar_numero:
    str w4, [x1], 4
    mov w4, 0
    add x5, x5, 1
    b leer_numeros

ordenar:
    str w4, [x1], 4
    add x5, x5, 1
    mov x6, 0

bucle_externo:
    mov x7, 0
    ldr x0, =numeros

bucle_interno:
    ldr w1, [x0]
    ldr w2, [x0, 4]
    cmp w1, w2
    ble no_intercambiar
    str w2, [x0]
    str w1, [x0, 4]

no_intercambiar:
    add x0, x0, 4
    add x7, x7, 1
    sub x8, x5, x6
    sub x8, x8, 1
    cmp x7, x8
    blt bucle_interno
    
    add x6, x6, 1
    cmp x6, x5
    blt bucle_externo

calcular_mediana:
    lsr x6, x5, 1
    lsl x7, x6, 2
    ldr x0, =numeros
    add x0, x0, x7
    ldr w1, [x0]
    
    tst x5, 1
    bne fin
    
    ldr w2, [x0, #-4]
    add w1, w1, w2
    lsr w1, w1, 1

fin:
    mov w0, w1
    mov x8, 93
    svc 0
    mov x8, 94
    svc 0
    
    
