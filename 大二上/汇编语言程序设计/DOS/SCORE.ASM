Datas segment
	STU db 76,69,84,90,73,88,99,63,100,80
	S6 db 0
	S7 db 0
	S8 db 0
	S9 db 0
	S10 db 0
Datas ends 
 
Code segment
	assume ds:Datas,cs:Code
start:
	mov ax,Datas
	mov ds,ax
	
	xor ax,ax
	mov si,0
	mov cx,10
	
next:
	mov al,byte ptr [si]
	
	cmp ax,69
	jg jmp1
	add S6,1
	jmp final
jmp1:
	cmp ax,79
	jg jmp2
	add S7,1
	jmp final
jmp2:
	cmp ax,89
	jg jmp3
	add S8,1
	jmp final
jmp3:
	cmp ax,99
	jg jmp4
	add S9,1
	jmp final
jmp4:
	add S10,1
	
final:
	inc si
	loop next
	
	mov dl,S6
	add dl,30h
	mov ah,2H
	int 21H

	mov dl,S7
	add dl,30h
	mov ah,2H
	int 21H

	mov dl,S8
	add dl,30h
	mov ah,2H
	int 21H

	mov dl,S9
	add dl,30h
	mov ah,2H
	int 21H

	mov dl,S10
	add dl,30h
	mov ah,2H
	int 21H
	
	mov ah,4cH
	int 21H
	
Code ends
	end start