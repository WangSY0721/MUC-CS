.data
    result: .space 256  #int64,per 4byte is a int
    startmsg: .asciiz"Input the factorial argument: "
    donemsg: .asciiz"The result is: "
    passmsg: .asciiz "Verification passed."
    errormsg: .asciiz "Error: The calculated result is incorrect."
.text

start:
    li $v0,4                            #print string
    la $a0,startmsg          
    syscall              
    li $v0,5                            #read integer
    syscall
    move $s2,$v0                        #s2 is multiplier
    li $s1,1                            #s1 is constant 1
    li $s3,64                           #s3 is result's length
    li $s4,100000                       #the Maximum representation number
    la $s0,result                       #s0 is result[0] address
    sw $s1,0($s0)                       #Initial result's value 

fact:
    li $t0, 0                           #t0 as a index, start from lowest pos
    move $t3,$zero                      #t3 is a overflow symbol
    move $t5,$zero                      #t5 is the number needs to carry in
    move $s6,$zero
    loopmul:
        move $t1, $t0                   #t1 is result[index]
        move $t3,$zero
        sll $t1, $t1, 2                 #t1 shif left twice
        add $t1, $t1, $s0               #get address
        lw $t2, 0($t1)                  #t2 is a temp number
        move $t4, $t2                   #t4 is temp result
        beq $s5,$s1,onlyAdd
        beq $t4, $zero, isEND           #if t4=0, end this time
        
        mulu $t4, $s2, $t4
    onlyAdd:
        add $t4,$t4,$t5
        sltu $t3, $s4, $t4              #if t4>100000, t3=1, need to cin
        beq $t3, $s1, isOF              #if is true, it comes overflow
        move $s5,$zero
        move $t5,$zero
        j isEND
    isOF:
        move $t6, $t0
        add $t6, $t6, $s1               #get result[index+1]
        beq $t6,$s3,isEND

        sll $t6, $t6, 2
        add $t6, $t6, $s0
        lw $s7,0($t6)
        sltu $s6, $zero, $s7            #if high pos > 0,s6 = 1
        divu $t4,$s4
        mflo $t5                        #t5=quotient
        mfhi $t4                        #t4=remainder,result[index]=t4

    isEND:
        sw $t4, 0($t1)
        addi $t0, $t0, 1                #index++
        sltu $t8, $s6,$s1
        sltu $t9, $zero,$t3
        and $s5,$t8,$t9
        beq $t0, $s3, endloop
        j loopmul

endloop:
sub $s2, $s2, $s1                       #multiplier--
beq $s2, $s1, done                      #if multiplier=1, it's done
j fact

done:
    la $a0,donemsg
    li $v0,4
    syscall
    move $t0, $s3
    sub $t0,$t0,$s1
    li $t4,-1
    move $t1, $zero
    move $t2, $zero
printloop:
	move $t1, $t0
    sll $t1, $t1, 2
    add $t1, $t1, $s0
    lw $t2, 0($t1)
    move $a0, $t2
    li $v0,36        #print integer as unsigned
    syscall
    sub $t0, $t0, $s1
    beq $t0, $t4, verify
    j printloop

verify:
	li $s0, 1                           # 循环变量
	li $s1, 1                           # 累乘结果
	li $s2, 100                         # 待验证的数+1
verify_loop:
	beq $s0, $s2, verify_done           # 循环结束，这里只能比较到要验证的数，但是要验证的数不会累乘到结果中，故上述待验证的数加一
	mul $s1, $s1, $s0                  # 逐个累乘
	addi $s0, $s0, 1                    # 循环变量++
	j verify_loop
verify_done:
	bne $s1, $t2, error                 # 结果与上面计算的不相等时，跳转到error
	li $v0, 4                           # 提示验证通过
	la $a0, passmsg
	syscall
	j exit                              # 跳出

error:
	li $v0, 4                           # 提示验证不通过
	la $a0, errormsg
	syscall
	j exit                              # 跳出

exit:
	li $v0, 10                          # 退出程序
	syscall

