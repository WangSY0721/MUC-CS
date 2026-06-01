module Pc(
	input clk,
	input reset,
	input Pcwre,
	input	[31:0]nextPc,
	output reg [31:0]curPc
);
initial
begin
	curPc=0;
end
always@(posedge clk or negedge reset)
begin
	if(!reset)
		curPc=0;
	else
		begin
			//为1时说明继续
			if(Pcwre)
				curPc=nextPc+4;
			else
				curPc=curPc;
		end
end
endmodule