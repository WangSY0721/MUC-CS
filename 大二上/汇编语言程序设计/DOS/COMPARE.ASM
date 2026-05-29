.model small
.stack 100h
.data
    STRING1 db 'HELLO', 0
    STRING2 db 'HELLO', 0
    MATCH_MSG db 'MATCH$'
    NO_MATCH_MSG db 'NO MATCH$'

.code
start:
    mov ax, @data
    mov ds, ax
    mov si, offset STRING1
    mov di, offset STRING2

compare_loop:
    mov al, [si]
    mov bl, [di]
    cmp al, bl
    jne no_match
    cmp al, 0
    je match
    inc si
    inc di
    jmp compare_loop

match:
    mov dx, offset MATCH_MSG
    jmp print_message

no_match:
    mov dx, offset NO_MATCH_MSG

print_message:
    mov ah, 9
    int 21h

exit_program:
    mov ax, 4C00h
    int 21h

end start