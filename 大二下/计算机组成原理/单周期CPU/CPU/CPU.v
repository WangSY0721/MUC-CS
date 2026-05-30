// Copyright (C) 1991-2015 Altera Corporation. All rights reserved.
// Your use of Altera Corporation's design tools, logic functions 
// and other software and tools, and its AMPP partner logic 
// functions, and any output files from any of the foregoing 
// (including device programming or simulation files), and any 
// associated documentation or information are expressly subject 
// to the terms and conditions of the Altera Program License 
// Subscription Agreement, the Altera Quartus II License Agreement,
// the Altera MegaCore Function License Agreement, or other 
// applicable license agreement, including, without limitation, 
// that your use is for the sole purpose of programming logic 
// devices manufactured by Altera and sold by Altera or its 
// authorized distributors.  Please refer to the applicable 
// agreement for further details.

// PROGRAM		"Quartus II 64-Bit"
// VERSION		"Version 15.0.0 Build 145 04/22/2015 SJ Full Version"
// CREATED		"Fri Dec 23 19:08:02 2022"

module CPU(
	reset,
	clk,
	RandomNumber,
	out1,
	out2,
	out3,
	out4,
	out5,
	out6,
	out7,
	out8
);


input wire	reset;
input wire	clk;
input wire	[7:0] RandomNumber;
output wire	[6:0] out1;
output wire	[6:0] out2;
output wire	[6:0] out3;
output wire	[6:0] out4;
output wire	[6:0] out5;
output wire	[6:0] out6;
output wire	[6:0] out7;
output wire	[6:0] out8;

wire	SYNTHESIZED_WIRE_0;
wire	[31:0] SYNTHESIZED_WIRE_1;
wire	[4:0] SYNTHESIZED_WIRE_2;
wire	[31:0] SYNTHESIZED_WIRE_3;
wire	[31:0] SYNTHESIZED_WIRE_4;
wire	[4:0] SYNTHESIZED_WIRE_5;
wire	[31:0] SYNTHESIZED_WIRE_35;
wire	[31:0] SYNTHESIZED_WIRE_36;
wire	[31:0] SYNTHESIZED_WIRE_8;
wire	SYNTHESIZED_WIRE_9;
wire	[31:0] SYNTHESIZED_WIRE_10;
wire	SYNTHESIZED_WIRE_12;
wire	SYNTHESIZED_WIRE_13;
wire	SYNTHESIZED_WIRE_14;
wire	[31:0] SYNTHESIZED_WIRE_15;
wire	[31:0] SYNTHESIZED_WIRE_16;
wire	[7:0] SYNTHESIZED_WIRE_17;
wire	[31:0] SYNTHESIZED_WIRE_18;
wire	[31:0] SYNTHESIZED_WIRE_20;
wire	[5:0] SYNTHESIZED_WIRE_21;
wire	[5:0] SYNTHESIZED_WIRE_22;
wire	SYNTHESIZED_WIRE_23;
wire	[31:0] SYNTHESIZED_WIRE_24;
wire	SYNTHESIZED_WIRE_26;
wire	[4:0] SYNTHESIZED_WIRE_37;
wire	[4:0] SYNTHESIZED_WIRE_28;
wire	SYNTHESIZED_WIRE_29;
wire	[4:0] SYNTHESIZED_WIRE_30;
wire	[4:0] SYNTHESIZED_WIRE_32;
wire	[31:0] SYNTHESIZED_WIRE_33;
wire	[15:0] SYNTHESIZED_WIRE_34;





PC	b2v_inst1(
	.clk(clk),
	.reset(reset),
	.Pcwre(SYNTHESIZED_WIRE_0),
	.nextPc(SYNTHESIZED_WIRE_1),
	.curPc(SYNTHESIZED_WIRE_36));


ALU	b2v_inst10(
	.ALUOp(SYNTHESIZED_WIRE_2),
	.ReadData1(SYNTHESIZED_WIRE_3),
	.ReadData2(SYNTHESIZED_WIRE_4),
	.sa(SYNTHESIZED_WIRE_5),
	.zero(SYNTHESIZED_WIRE_13),
	.result(SYNTHESIZED_WIRE_16));


Left	b2v_inst11(
	.datain(SYNTHESIZED_WIRE_35),
	.dataout(SYNTHESIZED_WIRE_8));


Add	b2v_inst12(
	.DataA(SYNTHESIZED_WIRE_36),
	.DataB(SYNTHESIZED_WIRE_8),
	.sum(SYNTHESIZED_WIRE_10));


mux_0	b2v_inst13(
	.sign(SYNTHESIZED_WIRE_9),
	.DataA(SYNTHESIZED_WIRE_10),
	.DataB(SYNTHESIZED_WIRE_36),
	.OData(SYNTHESIZED_WIRE_1));

assign	SYNTHESIZED_WIRE_9 = SYNTHESIZED_WIRE_12 & SYNTHESIZED_WIRE_13;


mux_1	b2v_inst15(
	.sign(SYNTHESIZED_WIRE_14),
	.DataA(SYNTHESIZED_WIRE_15),
	.DataB(SYNTHESIZED_WIRE_16),
	.OData(SYNTHESIZED_WIRE_33));


InputData	b2v_inst17(
	.clk(clk),
	.inputData(RandomNumber),
	.outputData(SYNTHESIZED_WIRE_17));


InputExtend	b2v_inst18(
	.RandomNumber(SYNTHESIZED_WIRE_17),
	.outputNumber(SYNTHESIZED_WIRE_15));


Result	b2v_inst2(
	.result(SYNTHESIZED_WIRE_18),
	.out1(out1),
	.out2(out2),
	.out3(out3),
	.out4(out4),
	.out5(out5),
	.out6(out6),
	.out7(out7),
	.out8(out8));


InsMem	b2v_inst3(
	.Addr(SYNTHESIZED_WIRE_36),
	.Iout(SYNTHESIZED_WIRE_20));


InstructionSlice	b2v_inst4(
	.Inst(SYNTHESIZED_WIRE_20),
	
	.FUNC(SYNTHESIZED_WIRE_21),
	.IMME(SYNTHESIZED_WIRE_34),
	.OP(SYNTHESIZED_WIRE_22),
	.RD(SYNTHESIZED_WIRE_28),
	.RS(SYNTHESIZED_WIRE_30),
	.RT(SYNTHESIZED_WIRE_37),
	.SHMAT(SYNTHESIZED_WIRE_5));


Control	b2v_inst5(
	.func(SYNTHESIZED_WIRE_21),
	.op(SYNTHESIZED_WIRE_22),
	
	.Branch(SYNTHESIZED_WIRE_12),
	
	
	.Regwre(SYNTHESIZED_WIRE_29),
	.ALUsrc(SYNTHESIZED_WIRE_23),
	.RegDst(SYNTHESIZED_WIRE_26),
	.MemtoReg(SYNTHESIZED_WIRE_14),
	.Pcwre(SYNTHESIZED_WIRE_0),
	.ALUOp(SYNTHESIZED_WIRE_2));


mux_2	b2v_inst6(
	.sign(SYNTHESIZED_WIRE_23),
	.DataA(SYNTHESIZED_WIRE_24),
	.DataB(SYNTHESIZED_WIRE_35),
	.OData(SYNTHESIZED_WIRE_4));


Mux4	b2v_inst7(
	.sign(SYNTHESIZED_WIRE_26),
	.dataA(SYNTHESIZED_WIRE_37),
	.dataB(SYNTHESIZED_WIRE_28),
	.Odata(SYNTHESIZED_WIRE_32));


RegFile	b2v_inst8(
	
	.clk(clk),
	.Regwre(SYNTHESIZED_WIRE_29),
	.Regs(SYNTHESIZED_WIRE_30),
	.Regt(SYNTHESIZED_WIRE_37),
	.Regw(SYNTHESIZED_WIRE_32),
	.wdata(SYNTHESIZED_WIRE_33),
	.outputReg1(SYNTHESIZED_WIRE_3),
	.outputReg2(SYNTHESIZED_WIRE_24),
	.outputReg3(SYNTHESIZED_WIRE_18));


InmediateExtend	b2v_inst9(
	.imme(SYNTHESIZED_WIRE_34),
	.extendImme(SYNTHESIZED_WIRE_35));


endmodule

module mux_0(sign,DataA,DataB,OData);
/* synthesis black_box */

input sign;
input [31:0] DataA;
input [31:0] DataB;
output [31:0] OData;

endmodule

module mux_1(sign,DataA,DataB,OData);
/* synthesis black_box */

input sign;
input [31:0] DataA;
input [31:0] DataB;
output [31:0] OData;

endmodule

module mux_2(sign,DataA,DataB,OData);
/* synthesis black_box */

input sign;
input [31:0] DataA;
input [31:0] DataB;
output [31:0] OData;

endmodule
