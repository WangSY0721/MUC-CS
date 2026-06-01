module ALU_74181   
(
	input [3:0] a,        
	input [3:0] b,        
	input [3:0] s,        
    input  m,         
    input  cn,         
    output [3:0] f,      
    output aeqb,      
    output c4,        
    output p,          
    output g          
);
reg [3:0] result;      
wire [4:0]temp;       
wire p0,p1,p2,p3;     
wire g0,g1,g2,g3;  
assign temp = {s, m, cn};

always @(temp or a or b) begin
	 case (temp)
        6'b000000: result = a;
		  6'b000001: result = a+1;
        6'b000010: result = ~a;
		  6'b000011: result = ~a;

		  6'b000100: result = a|b;
		  6'b000101: result = (a|b)+1;
        6'b000110: result = ~(a|b);
		  6'b000111: result = ~(a|b);
        
		  6'b001000: result = a|~b;
		  6'b001001: result = (a|~b)+1;
        6'b001010: result = ~a&b;
		  6'b001011: result = ~a&b;
        
		  6'b001100: result = (result + 4'b1111);
		  6'b001101: result = 4'b0000;
        6'b001110: result = 4'b0000;
		  6'b001111: result = 4'b0000;
		  
		  6'b010000: result = a+(a&~b);
		  6'b010001: result = a+(a&~b)+1;
        6'b010010: result = ~(a&b);
		  6'b010011: result = ~(a&b);
		  
		  6'b010100: result = (a&~b)+(a|b);
		  6'b010101: result = (a&~b)+(a|b)+1;
        6'b010110: result = ~b;
		  6'b010111: result = ~b;
		  
		  6'b011000: result = a-b-1;
		  6'b011001: result = a-b;
        6'b011010: result = a^b;
		  6'b011011: result = a^b;
		  
		  6'b011100: result = (a&~b)-1;
		  6'b011101: result = a&~b;
        6'b011110: result = a&~b;
		  6'b011111: result = a&~b;
		  
		  6'b100000: result = a+(a&b);
		  6'b100001: result = a+(a&b)+1;
        6'b100010: result = (~a|b);
		  6'b100011: result = (~a|b);
		  
		  6'b100100: result = a+b;
		  6'b100101: result = a+b+1;
        6'b100110: result = ~(a^b);
		  6'b100111: result = ~(a^b);
		  
		  6'b101000: result = (a|~b)+(a&b);
		  6'b101001: result = (a|~b)+(a&b)+1;
        6'b101010: result = b;
		  6'b101011: result = b;
		  
		  6'b101100: result = a&b-1;
		  6'b101101: result = a&b;
        6'b101110: result = a&b;
		  6'b101111: result = a&b;
		  
		  6'b110000: result = a;
		  6'b110001: result = a+a+1;
        6'b110010: result = 4'b0001;
		  6'b110011: result = 4'b0001;
		  
		  6'b110100: result = a+(a|b);
		  6'b110101: result = a+(a|b)+1;
        6'b110110: result = a|~b;
		  6'b110111: result = a|~b;
		  
		  6'b111000: result = a+(a|~b);
		  6'b111001: result = a+(a|~b)+1;
        6'b111010: result = a|b;
		  6'b111011: result = a|b;
		  
		  6'b111100: result = a-1;
		  6'b111101: result = a;
        6'b111110: result = a;
		  6'b111110: result = a;
		  
		  default: result = 4'b0000;
    endcase
end

assign f=result;        //?????result????f
//??????????
assign g0=a[0]&b[0]; //g???a?b??
assign g1=a[1]&b[1];
assign g2=a[2]&b[0];
assign g3=a[3]&b[0];

assign p0=a[0]^b[0]; //p???a?b???
assign p1=a[1]^b[1];
assign p2=a[2]^b[2];
assign p3=a[3]^b[3];


assign  c4=g3|(g2&p3)|(g1&p2&p3)|(g0&p0&p1&p2)|(cn&p0&p1&p2&p3);
//g3 + p3g2 + p3p2g1 + p3p2p1g0 + p3p2p1p0cn
assign  p=p0&p1&p2&p3;    
assign  g=g3+g2&p3+g1&p2&p3+g0&p1&p2&p3;
assign aeqb=(a==b)?1'b1:1'b0;
endmodule
