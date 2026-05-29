.model small
.stack 100h

.data

.code
start:
    mov ax, @data ; 初始化数据段
    mov ds, ax

    mov cx, 0 ; 初始化外层循环计数器

outer_loop:
    push cx ; 保存当前的行数到栈中

    mov bx, cx ; 将行数复制到bx，作为内层循环计数器
    inc bx ; 行数加1，因为我们打印从当前行数开始

inner_loop:
    push bx ; 保存内层循环计数器
    mov ax, bx ; 将bx的值移动到ax
    dec ax ; 减1，因为我们需要打印当前行数减1的值
    add al, '0' ; 将数字转换为其ASCII码
    mov dl, al ; 准备打印的字符
    mov ah, 02h ; 准备使用功能号2的中断，用于显示字符
    int 21h ; 调用中断打印字符

    mov dl, ' ' ; 准备打印空格
    int 21h ; 调用中断打印空格

    pop bx ; 恢复内层循环计数器
    dec bx ; 内层循环计数器递减
    cmp bx, 0 ; 比较bx是否为0
    jnz inner_loop ; 如果不为0，则跳转继续内层循环

    ; 打印换行
    mov dl, 13 ; carriage return
    int 21h
    mov dl, 10 ; line feed
    int 21h

    pop cx ; 恢复外层循环计数器
    inc cx ; 外层循环计数器递增
    cmp cx, 9 ; 检查是否已经打印到了9行
    jbe outer_loop ; 如果小于或等于9，继续外层循环

end_program:
    mov ax, 4C00h ; 设置退出码
    int 21h ; 调用中断以结束程序

    end start ; 程序入口点
