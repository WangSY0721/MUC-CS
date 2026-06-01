`timescale 1ns / 1ps
module ALU(
		input CLK,
		input CLK1,
      input ALUSrcA,
		input ALUSrcB,
      input [31:0] ReadData1,
		input [31:0] ReadData2,
		input [4:0] sa,
      input [31:0] extend,
		input [4:0] ALUOp,
		output reg zero,
      output reg[31:0] result
);
reg [31:0] A;
reg [31:0] B;
reg [63:0] extresult;
	// reg [63:0] extresult;
	 reg [31:0] resulthi;
	 reg [31:0] resultlo;
  	 initial begin
	 resulthi<=0;
	 resultlo<=0;
	 extresult<=0;
	 end
always@(negedge CLK1)
if(CLK)
begin
   //定义两个输入接口
	A = (ALUSrcA == 0) ? ReadData1 : sa;
   B = (ALUSrcB == 0) ? ReadData2 : extend;

		      case(ALUOp)
				    // 1 add
					 5'b00001: begin
					     result = A + B;
					 end
					 // 2 and
					 5'b00010: begin
					     result = A & B;
					 end
					 // 3 nor
					 5'b00011: begin
					     result = ~(A | B);
					 end
					 // 4 or
					 5'b00100: begin
					     result = A | B;
						  zero = (result == 0)? 1 : 0;
					 end
					 // 5 slt
					 5'b00101: begin
					     result = (A<B)? 1 : 0;
					 end
					 // 6 sll
					 5'b00110: begin
					     result = B<<sa;
				    end
					 // 7 srl(logical)
					 5'b00111: begin
					     result = B>>>sa;
					 end
					 // 8 sub
					 5'b01000: begin
					     result = A - B;
					 end
					 // 9 div
					 5'b01001: begin
					     resulthi = A / B;
						  resultlo = A % B;
					 end
					 // 10 mfhi
					 5'b01010: begin
					     result = resulthi;
					 end
					 // 11 mflo
					 5'b01011: begin
					     result = resultlo;
					 end
					 // 12 mult
					 5'b01100: begin
					     extresult = A * B;
						  resulthi=extresult[63:32];
						  resultlo=extresult[31:0];
						  result=extresult[31:0];
					 end
					 // 13 sra
					 5'b01101: begin
					     result = B >>sa;
					 end
					 // 14 addi
					 5'b01110: begin
					     result = A + B;
					 end
					 // 15 bne
					 5'b01111: begin
					     result = A - B;
					 end 
					 // 16 lw
					 5'b10000: begin
					     result = A + B;
					 end 
					 // 17 sw
					 5'b10001: begin
					     result = A + B;
					 end 
					 //18 中断，全亮
					 5'b10010: begin
					     result =32'b11111111111111111111111111111111;
					 end 
		  // 21 addu
					 5'b10101: begin
					     result =A+B;
					 end
					 //22 xor
					 5'b10110: begin
					     result = A ^ B;
					 end
					 // 23 bltz
					 5'b10111: begin
					 
					     if (A < 0)          // Check if A < 0
						result = 0;    // Set ALUout to 1 if true
					     else                // bgez: Check if A >= 0
						result =1;    // Set ALUout to 0 if false
					end
					
					 // 24 bgez
					 5'b11000: begin
					        if (A < 0)          // Check if A < 0
						result = 0;    // Set ALUout to 1 if true
					     else                // bgez: Check if A >= 0
						result =1;    // Set ALUout to 0 if false
					end
					
					 // 25 beq
					 5'b11001: begin
					     result = A - B;
					 end 
					 //26 slti
					 5'b11010: begin
					     result = A<B ?1:0;
					 end 
//27 ori
					 5'b11011: begin
					     result = A | B;
					 end 
		      endcase
   zero = (result == 0) ? 1 : 0;
end
endmodule
