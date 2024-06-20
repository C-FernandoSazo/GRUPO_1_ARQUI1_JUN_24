.global _start
.bss
input:
    .space 100  
.text
_start:
    mov x0, 0        
    ldr x1, =input   
    mov x2, 100      
    mov x8, 63       
    svc 0            
    ldr x0, =input   
    mov x3, 1        
bucle_contar:
    ldrb w1, [x0], 1 
    cmp w1, 0        
    beq fin          
    cmp w1, 44       
    beq incrementar  
    b bucle_contar
incrementar:
    add x3, x3, 1    
    b bucle_contar
fin:
    mov x0, x3       
    mov x8, 93       
    svc 0
    