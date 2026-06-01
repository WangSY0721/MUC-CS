`timescale 1ns / 1ps
module PC(
input CLK,
input Reset,  //是否重置地址。0- 初始化PC,否則接受新地址
input PCWre,
input [2:0] PCSrc,
input [31:0] nextPC, //新指令地址
output reg[31:0] curPC //当前指令的地址
);

initial begin
curPC <= 0;

end
always@(posedge CLK or negedge Reset)
begin
	if(!Reset) //Reset==0, PC=0
	begin
		curPC <= 0;
	end
	else
	begin
		if(PCWre) //PCWre== 1
			begin
				curPC <= nextPC + 4;
			end
		else		//PCWre == 0 ,halt
			begin
				curPC <= curPC;
			end
	end
end
endmodule
