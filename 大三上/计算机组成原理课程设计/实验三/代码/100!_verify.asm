.data
    array: 
        .space 0x100  # 为结果分配空间，足够存储计算的结果

    # 目标值以字符串形式存储
    target_value: 
        .asciiz "93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000"

    yes_string: .asciiz "yes\n"
    no_string: .asciiz "no\n"

.text                   
main:                    
    li $a1, 1  # 从1开始
    li $t0, 1  # 初始化阶乘的值
    la $s0, array # 数组地址
    sw $t0, 0($s0) # 存储初始值1

factorial:
    li $t2, 0  # 循环计数器

loop:	
    # 计算当前阶乘
    lw $t0, 0($s0)  # 加载当前值
    multu $t0, $a1  # 计算乘法
    mflo $t0  # 获取低位结果
    sw $t0, 0($s0)  # 存储结果

    addi $a1, $a1, 1  # 当前值加1	
    bne $a1, 101, loop  # 如果未达到100，继续计算阶乘

    # 阶乘计算完成后，准备与目标值比较
    la $t9, target_value  # 加载目标值的字符串地址
    la $t8, array  # 加载计算结果的地址

compare_loop:
    lb $t0, 0($t8)      # 加载计算结果的当前字符
    lb $t1, 0($t9)      # 加载目标值的当前字符
    beqz $t0, end_compare  # 如果结果到达结束，跳转
    beqz $t1, not_same  # 如果目标值到达结束，跳转到not_same

    # 比较字符
    beq $t0, $t1, next_char  # 如果相同，比较下一个字符
    j not_same  # 如果不同，跳转到not_same

next_char:
    addi $t8, $t8, 1  # 移动到下一个计算结果字符
    addi $t9, $t9, 1  # 移动到下一个目标字符
    j compare_loop  # 继续比较

not_same:
    # 输出 "no"
    li $v0, 4
    la $a0, no_string
    syscall
    j end_compare

end_compare:
    # 输出 "yes" 如果到达这里，说明所有字符都匹配
    li $v0, 4
    la $a0, yes_string
    syscall

    # 结束程序
    li $v0, 10
    syscall




	
