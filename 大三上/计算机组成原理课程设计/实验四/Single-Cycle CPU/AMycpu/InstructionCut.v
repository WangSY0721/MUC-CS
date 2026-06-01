module InstructionCut(
	input myreset,
	input [31:0] Inst,
	output reg[5:0] OP,
	output reg[5:0] FUNC,
	output reg[4:0] SHMAT,
	
	output reg[4:0] RS,
	output reg[4:0] RT,
	output reg[4:0] RD,
	
	output reg[15:0] IMME,
	output reg[25:0] ADDR//J型指令

);
always@(Inst)
begin
	//if(!myreset)
	//begin
		//OP=6'd0;
		//RS=5'd0;
		//RT=5'd0;
		//RD=5'd0;
	//end

	//else
	//begin
		//R OP+RS+RT+RD+SHAMT+FUNC
		OP=Inst[31:26];
		RS=Inst[25:21];
		RT=Inst[20:16];
		RD=Inst[15:11];
		SHMAT=Inst[10:6];
		FUNC=Inst[5:0];
		//I OP+RS+RT+IMME
		IMME=Inst[15:0];
		//J OP+ADDR
		ADDR=Inst[25:0];
	//end
end

endmodule
