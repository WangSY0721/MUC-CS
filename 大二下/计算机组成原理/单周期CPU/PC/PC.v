module PC(
	input clk,
	input reset,
	input Pcwre,
	input	[31:0]nextPc,
	output reg [31:0]curPc
);
always@(posedge clk or negedge reset)
begin
	if(!reset)
		begin
			curPc<=0;
		end
	else
		begin
			//为1时说明继续
			if(Pcwre)
				curPc<=nextPc+4;
			else
				curPc<=curPc;
		end
end
endmodule