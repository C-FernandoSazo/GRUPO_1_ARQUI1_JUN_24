.global _start
.bss
input: .space 100
numeros: .space 400
suma_cuadrados: .quad 0

.text
_start:
    mov x0, 0
    ldr x1, =input
    mov x2, 100
    mov x8, 63
    svc 0

    mov x4, 0
    mov x5, 0
    mov x6, 0
    ldr x0, =input
    ldr x1, =numeros

leer_numeros:
    ldrb w2, [x0], 1
    cmp w2, 44
    beq guardar_numero
    cmp w2, 10
    beq calcular_media
    sub w2, w2, 48
    mov w3, w4
    mov w4, 10
    mul w3, w3, w4
    add w4, w3, w2
    b leer_numeros

guardar_numero:
    str w4, [x1], 4
    add x6, x6, x4
    mov w4, 0
    add x5, x5, 1
    b leer_numeros

calcular_media:
    str w4, [x1], 4
    add x6, x6, x4
    add x5, x5, 1
    sdiv x7, x6, x5

    ldr x0, =numeros
    mov x1, 0
    ldr x2, =suma_cuadrados
    str xzr, [x2]

calcular_diferencias:
    ldr w3, [x0], 4
    sub w4, w3, w7
    mul w4, w4, w4
    ldr x9, [x2]
    add x9, x9, x4
    str x9, [x2]
    add x1, x1, 1
    cmp x1, x5
    blt calcular_diferencias

    ldr x0, [x2]
    sdiv x0, x0, x5
    
    mov x1, x0
    lsr x1, x1, 1
    mov x2, 10
    
raiz_cuadrada:
    sdiv x3, x0, x1
    add x3, x3, x1
    lsr x1, x3, 1
    subs x2, x2, 1
    bne raiz_cuadrada

fin:
    mov x0, x1
    mov x8, 93
    svc 0
    