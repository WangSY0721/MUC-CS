module MultiCycleCPU(
input CLK1,
input clk2,
input Reset,
input en,
input halt,
input [3:0] x,
output [31:0] result,
output [6:0] out1,
output [6:0] out2,
output [6:0] out3,
output [6:0] out4,
output [6:0] out5,
output [6:0] out6,
output [6:0] out7,
output [6:0] out8
);
wire CLK;
wire [31:0] curPC;
wire [31:0] nextPC;
wire [31:0] instruction;
wire [5:0] op;
wire [4:0] rs;
wire [4:0] rt;
wire [4:0] rd;
wire [5:0] funct;
wire [31:0] DB;
wire [31:0] A;
wire [31:0] B;
wire [2:0] PCSrc;
wire [3:0] InPut;
wire zero;
wire PCWre;
wire show_result;//是否输出标志，1输出
wire input_number;
wire output_number;
wire ExtSel;		
wire InstMemRW;	
wire RegDst;	
wire RegWre;		
wire ALUSrcA;		
wire ALUSrcB;		
wire [4:0]ALUOp;	
wire MemRead;		
wire MemWrite;		
wire DBDataSrc;
wire [31:0] extend;
wire [31:0] DataOut;
wire [4:0] sa;
wire [15:0] immediate;
wire [25:0] addr;

CLKmode clks(
.CLK1(rco),
.CLK(CLK)
);

div_20	b2v_inst1(
	.clk(CLK1),
	.en(en),
	.rco(rco));

PC pc(
.CLK(CLK),
.Reset(Reset),
.PCWre(PCWre),
.PCSrc(PCSrc),
.nextPC(nextPC),
.curPC(curPC));

totalMEM totalMEM( 
.IAddr(nextPC+'d4),
.InstMemRW(InstMemRW),
.InPut(InPut),
.CLK1(CLK1),
.input_number(input_number),
.IDataOut(instruction),
.MemRead(MemRead),
.MemWrite(MemWrite),
.CLK(CLK),
.DBDataSrc(DBDataSrc),
.DAddr(result),
.DataIn(B),
.DataOut(DataOut),
.DB(DB));





InstructionCut InstructionCut(
.instruction(instruction),
.op(op),
.rs(rs),
.rt(rt),
.rd(rd),
.sa(sa),
.funct(funct),
.immediate(immediate),
.addr(addr));

ControlUnit ControlUnit(
.CLK(CLK),
.halt(halt),
.zero(zero),
.op(op),
.funct(funct),
.input_number(input_number),
.output_number(output_number),
.PCWre(PCWre),
.ExtSel(ExtSel),
.InstMemRW(InstMemRW),
.RegDst(RegDst),
.RegWre(RegWre),
.ALUSrcA(ALUSrcA),
.ALUSrcB(ALUSrcB),
.PCSrc(PCSrc),
.ALUOp(ALUOp),
.MemRead(MemRead),
.MemWrite(MemWrite),
.DBDataSrc(DBDataSrc));

RegisterFile RegisterFile(
.CLK(CLK),
.ReadReg1(rs),
.ReadReg2(rt),
.WriteData(DB),
.WriteReg(RegDst ? rd : rt),
.RegWre(RegWre),
.ReadData1(A),
.ReadData2(B));//

ALU alu(
.CLK(CLK),
.CLK1(rco),
.ALUSrcA(ALUSrcA),
.ALUSrcB(ALUSrcB),
.ReadData1(A),
.ReadData2(B),
.sa(sa),
.extend(extend),
.ALUOp(ALUOp),
.zero(zero),
.result(result));

PCAddr PCAddr(
.CLK(CLK),
//.Reset(Reset),
.PCSrc(PCSrc),
.immediate(extend),
.addr(addr),
.curPC(curPC),
.nextPC(nextPC));


SignZeroExtend SignZeroExtend(
.immediate(immediate),
.ExtSel(ExtSel),
.extendImmediate(extend));

IO IO1(
.x(x),
.input_number(input_number),
.output_number(output_number),
.InPut(InPut),
.show_result(show_result));

show show1(
.result(result),
.show_result(show_result),
.out1(out1),
.out2(out2),
.out3(out3),
.out4(out4),
.out5(out5),
.out6(out6),
.out7(out7),
.out8(out8)
);
endmodule
