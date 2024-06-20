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
bucle_maximo:
    ldrb w1, [x0], 1
    cmp w1, 44     
    beq comparar_numero
    cmp w1, 10      
    beq comparar_numero
    cmp w1, 0      
    beq comparar_numero
    sub w1, w1, 48  
    and x1, x1, 0xFF  
    mov x2, 10
    mul x4, x4, x2
    add x4, x4, x1
    b bucle_maximo
comparar_numero:
    cmp x4, x3
    csel x3, x4, x3, gt
    mov x4, 0
    cmp w1, 10
    beq fin
    cmp w1, 0
    beq fin
    b bucle_maximo
fin:
    mov x0, x3
    mov x8, 93
    svc 0
    