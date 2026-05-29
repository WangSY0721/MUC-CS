.model small
.stack 100h

.data
input_string db 'HELLO WORLD$',0

.code
start:
    mov ax, @data
    mov ds, ax    ; 初始化数据段寄存器
    mov es, ax    ; 在需要的情况下初始化附加段寄存器
    mov ss, ax    ; 初始化堆栈段寄存器
    mov sp, 100h  ; 初始化堆栈指针

    lea dx, input_string ; 加载字符串的地址
    call ConvertToLower  ; 调用子程序转换为小写
    mov ah, 9            ; 准备输出字符串
    int 21h              ; 输出转换后的字符串

    mov ax, 4C00h        ; 退出程序
    int 21h              ; 调用中断

; 子程序：将大写字母转换为小写
ConvertToLower proc near
    push ax
    push bx
    push cx
    push dx
    push si

    lea si, input_string ; 将字符串地址加载到 SI 寄存器

    next_char:
        mov al, [si]           ; 获取当前字符
        cmp al, '$'            ; 检查是否为'$'结束符
        je  end_conversion     ; 如果是，则结束转换
        cmp al, 'A'
        jb  skip_conversion
        cmp al, 'Z'
        ja  skip_conversion
        add al, 32             ; 将大写字母转换为小写字母
        mov [si], al           ; 存回字符串

    skip_conversion:
        inc si                 ; 移至下一个字符
        jmp next_char          ; 继续下一个字符的转换

    end_conversion:
        pop si
        pop dx
        pop cx
        pop bx
        pop ax
        ret
ConvertToLower endp

end start
