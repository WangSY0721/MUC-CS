.data
	array:
		.space 0x10010000
.text                   
main:                    
    	li $a1,1  #from 1
	li $t0,1  #
	li $t1,1000000
	la $s0,array #address
	
	sw $t0,0($s0)
	

factorial:
	subi $s7,$s0,32
	li $t2,0
loop:	
	addi $s7,$s7,32
	lw $t0,0($s7)
    	multu $t0,$a1
	mfhi $s1            
    	mflo $s2
	divu $s2,$t1
	mfhi $s3#remain        
    	mflo $s4#result
	addu $t0,$s3,$s6#remain + last result
	slt $t3,$t0,$t1#over 1000000
	beq $t3,1,store
	sub $t0,$t0,$t1
	addi $s4,$s4,1
store:	sw $t0,0($s7)

	addi $s7,$s7,32
	lw $t0,0($s7)
   	multu $t0,$a1
	mfhi $s1            
    	mflo $s2
	divu $s2,$t1
	mfhi $s5#remain        
    	mflo $s6#result
	addu $t0,$s5,$s4#remain + last result
	slt $t3,$t0,$t1#over 1000000, minus 1000000, forward plus 1
	beq $t3,1,store1
	sub $t0,$t0,$t1
	addi $s6,$s6,1
store1:	sw $t0,0($s7)
	
	addi $t2,$t2,1	
	bne $t2,14,loop  #sacrifice time for the code'order,100! 158 bit, need about 27 * temp(1000000)
	
    	addi $a1,$a1,1	
	bne $a1,100,factorial #factorial
	
	subi $s0,$s0,32
loop1:	#if bits less then 1000000, fill with 0,only print signed int
	li $v0,1
	lw $t8,0($s7)
	
	li $t3,100000
	li $t4,10000
	li $t5,1000
	li $t6,100
	li $t7,10
	
	slt $a1,$t8,$t3
	beq $a1,0,L1
	li $a0,0
	syscall
	slt $a1,$t8,$t4
	beq $a1,0,L1
	li $a0,0
	syscall
	slt $a1,$t8,$t5
	beq $a1,0,L1
	li $a0,0
	syscall
	slt $a1,$t8,$t6
	beq $a1,0,L1
	li $a0,0
	syscall
	slt $a1,$t8,$t7
	beq $a1,0,L1
	li $a0,0
	syscall
	
L1:	move $a0,$t8
	syscall
	
	subi $s7,$s7,32
	bne $s7,$s0,loop1
	
