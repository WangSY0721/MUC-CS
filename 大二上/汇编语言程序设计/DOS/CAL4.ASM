data segment
	x db 3
	y db 2
	z db 7
	w db ?,?
data ends
code segment
	assume cs:code,ds:data
start:
	mov ax,data
	mov ds,ax
	mov al,x
	add al,y
	sub al,z
	mov w,al
	
	mov ah,0
	mov al,w
	test al,al  #判断负数
	js negative  #负数进
	jz iszero  #0进

iszero：
	mov ah,2
	mov ah,0
	mov al,w
	test al,al
	js negative
	jz iszero

iszero:
	mov ah,2
	add al,30h
	mov dl,al
	int 21h
	jmp end

negative:
	mov ah,2
	mov dl,'-'  #输出负号
	int 21h
	neg al  #将负数变为正数
	add al,30h
	mov dl,al
	int 21h
end:
	mov ah,4ch
	int 21h
code ends
	end start