`timescale 1ns /1ps
module PCAddr(
input CLK,
input [2:0] PCSrc,
input [31:0] immediate,//beq
input [25:0] addr,//j
input [31:0] curPC,
output reg [31:0] nextPC);
reg [31:0] stayPC;//记录中断时当前指令地址
initial begin
nextPC <= 0;
end

always @(negedge CLK) 
begin
	if (PCSrc==0) nextPC<=curPC;//no jump
	//else if (PCSrc==1) begin nextPC=curPC+4; end //bne
	
	else if (PCSrc==1) begin nextPC<=curPC+immediate*4; end //bne
	// BranchAddr = { 14{immediate[15]}, immediate, 2'b0 }
	
	//else if (PCSrc==2) nextPC={curPC[31:28], addr[25:0],2'b00};//j
	//JumpAddr =    { PC+4[31:28], address, 2?b0 }
	
	
	else if(PCSrc==3)//中断
		begin
			stayPC<=curPC;
			nextPC<=44;
		end
	else if(PCSrc==4)//关中断
		begin
			nextPC<=stayPC;
		end
		
		
	//else if (PCSrc==3) nextPC=ReadData2+4;//jr
end


endmodule
