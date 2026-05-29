code segment
        assume cs:code
    start:
        mov ax,5h
        mov bx,6h
        add ax,bx

        mov ah,4ch
        int 21h
code ends
    end start
