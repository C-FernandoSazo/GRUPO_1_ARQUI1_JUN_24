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
ldr x0, =input
bucle_maximo:
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
b bucle_maximo
comparar_numero:
cmp x4, x3
csel x3, x4, x3, gt
mov x4, 0
b bucle_maximo
fin:
cmp x4, x3
csel x3, x4, x3, gt
mov x0, x3
mov x8, 93
svc 0
