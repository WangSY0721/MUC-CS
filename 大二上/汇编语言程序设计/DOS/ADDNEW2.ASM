DATA   SEGMENT
         X DB  ?
         Y DB  ?
         Z DB  ?
         W DW  ?,?   
         MESSAGE DB 'Press any key to continue...', '$'
DATA   ENDS

CODE   SEGMENT
       ASSUME CS:CODE,DS:DATA
START: MOV AX,DATA
       MOV DS,AX

       MOV  AH,1
       INT 21H 
       SUB AL,30H
       MOV X,AL

       MOV AH,1
       INT 21H 
       SUB AL,30H
       MOV Y,AL

       MOV AH,1
       INT 21H 
       SUB AL,30H
       MOV Z,AL

        MOV AH,2     
        MOV DL,13   
        INT 21H       

        MOV AH,2     
        MOV DL,10   
        INT 21H

        MOV AH,2     
        MOV DL,X  
        ADD DL,30H
        INT 21H      

        MOV AH,2     
        MOV DL,'+'  
        INT 21H       

        MOV AH,2     
        MOV DL,Y    
        ADD DL,30H
        INT 21H  
        
        MOV AH,2     
        MOV DL,'-'  
        INT 21H   
        
        MOV AH,2     
        MOV DL,Z    
        ADD DL,30H
        INT 21H  
        
        MOV AH,2     
        MOV DL,'=' 
        INT 21H    

       MOV AL,X    
       ADD AL,Y  
       SUB AL,Z   
       MOV W,AX
       
       CMP AL,10
       JL SKIP_TENS  
       MOV AH,0
       MOV BL,10   
       DIV BL  
       MOV W,AX
       MOV BX,W
       MOV AX,0

       MOV AH,2   
       MOV AL,BL
       ADD AL,30H   
       MOV DL,AL
       INT 21H      

       MOV AH,2      
       MOV AL,BH
       ADD AL,30H    
       MOV DL,AL
       INT 21H 
       JMP ENDING

       SKIP_TENS:
       
       TEST AL,AL  
       JS  OUTPUT_NEG 
       
       MOV AH,2      
       ADD AL,30H    
       MOV DL,AL
       INT 21H 
       JMP ENDING    
       
       OUTPUT_NEG:

       MOV DL,'-'  
       MOV AH,2    
       INT 21H
       MOV AX,W
       NEG AL
       MOV AH,2      
       ADD AL,30H    
       MOV DL,AL
       INT 21H 

       ENDING:
        MOV  AH,4CH
        INT  21H
CODE   ENDS
END    START