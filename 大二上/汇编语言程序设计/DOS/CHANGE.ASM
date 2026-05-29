DATAS SEGMENT
    STR1 DB "Please enter an uppercase letter"
    DB 0DH,0AH,'$'
    STR2 DB "Error Input"
    DB 0DH,0AH,'$'
DATAS ENDS

STACKS SEGMENT

STACKS ENDS

CODES SEGMENT
    ASSUME CS:CODES,DS:DATAS,SS:STACKS
START:
    MOV AX,DATAS
    MOV DS,AX
    
    MOV DX,OFFSET STR1
    MOV AH,9
    INT 21H
    
    MOV AH,01
    INT 21H
    
    CMP AL,'A'       
    JB ERROR
    CMP AL,'Z'
    JA ERROR
    
    ADD AL,32            
    
    MOV DL,AL         
    MOV AH,02
    INT 21H
    
    MOV AH,4CH      
    INT 21H
    
    ERROR:   
        MOV DX,OFFSET STR2
        MOV AH,9
        INT 21H
        
        MOV AH,4CH
        INT 21H
    
CODES ENDS
    END START
