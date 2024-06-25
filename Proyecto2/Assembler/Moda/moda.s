.global _start
.bss
input: .space 100
frecuencias: .space 400
.text
_start:
mov x0, 0
ldr x1, =input
mov x2, 100
mov x8, 63
svc 0
ldr x0, =frecuencias
mov x1, 0
mov x2, 100
inicializar_frecuencias:
str xzr, [x0], 8
add x1, x1, 1
cmp x1, x2
bne inicializar_frecuencias
mov x4, 0
ldr x0, =input
contar_frecuencias:
ldrb w1, [x0], 1
cmp w1, 44
beq sumar_frecuencia
cmp w1, 10
beq encontrar_moda
sub w1, w1, 48
mov w2, w4
mov w4, 10
mul w2, w2, w4
add w4, w2, w1
b contar_frecuencias
sumar_frecuencia:
ldr x1, =frecuencias
lsl x2, x4, 3
add x1, x1, x2
ldr x2, [x1]
add x2, x2, 1
str x2, [x1]
mov x4, 0
b contar_frecuencias
encontrar_moda:
ldr x1, =frecuencias
lsl x2, x4, 3
add x1, x1, x2
ldr x2, [x1]
add x2, x2, 1
str x2, [x1]
mov x3, 0
mov x4, 0
mov x5, 0
ldr x0, =frecuencias
bucle_moda:
ldr x1, [x0], 8
cmp x1, x4
csel x4, x1, x4, gt
csel x5, x3, x5, gt
add x3, x3, 1
cmp x3, 100
bne bucle_moda
mov x0, x5
mov x8, 93
svc 0
