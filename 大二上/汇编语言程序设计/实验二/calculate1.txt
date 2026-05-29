data segment
	x db 1
	y db 5
	z db 2
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
	
	mov ah,2
	add al,30h
	mov dl,al
	int 21h

	mov ah,4ch
	int 21h
code ends
	end start