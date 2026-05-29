DATA SEGMENT
    X   DB ?
    Y   DB ?
    Z   DB ?
    W   DB ?, ?
DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE, DS:DATA

START:
    MOV AX, DATA
    MOV DS, AX

    MOV AH, 01h      ; Function to read a character from keyboard
    INT 21h          ; Interrupt 21h
    SUB AL, 30h      ; Convert ASCII digit to binary value
    MOV X, AL

  
    MOV AH, 01h      ; Function to read a character from keyboard
    INT 21h          ; Interrupt 21h
    SUB AL, 30h      ; Convert ASCII digit to binary value
    MOV Y, AL


    MOV AH, 01h      ; Function to read a character from keyboard
    INT 21h          ; Interrupt 21h
    SUB AL, 30h      ; Convert ASCII digit to binary value
    MOV Z, AL


    MOV AL, X
    ADD AL, Y
    SUB AL, Z
    MOV W, AL


    MOV AH, 02h      ; Function to output a character
    ADD AL, 30h      ; Convert binary value back to ASCII digit
    MOV DL, AL
    INT 21h          ; Interrupt 21h


    MOV AH, 4Ch      ; Function to exit the program
    INT 21h          ; Interrupt 21h

CODE ENDS
END START