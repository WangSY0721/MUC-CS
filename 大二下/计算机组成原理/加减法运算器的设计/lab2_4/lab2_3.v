// Copyright (C) 1991-2010 Altera Corporation
// Your use of Altera Corporation's design tools, logic functions 
// and other software and tools, and its AMPP partner logic 
// functions, and any output files from any of the foregoing 
// (including device programming or simulation files), and any 
// associated documentation or information are expressly subject 
// to the terms and conditions of the Altera Program License 
// Subscription Agreement, Altera MegaCore Function License 
// Agreement, or other applicable license agreement, including, 
// without limitation, that your use is for the sole purpose of 
// programming logic devices manufactured by Altera and sold by 
// Altera or its authorized distributors.  Please refer to the 
// applicable agreement for further details.

// PROGRAM		"Quartus II"
// VERSION		"Version 10.0 Build 218 06/27/2010 SJ Web Edition"
// CREATED		"Sat Apr 28 21:11:03 2018"

module lab2_3(
	clock,
	cclr,
	c0,
	a,
	b,
	carry_out3,
	out
);


input wire	clock;
input wire	cclr;
input wire	c0;
input wire	[31:0] a;
input wire	[31:0] b;
output wire	carry_out3;
output wire	[31:0] out;

wire	carry_out;
wire	[31:0] out_ALTERA_SYNTHESIZED;
wire	SYNTHESIZED_WIRE_0;
wire	SYNTHESIZED_WIRE_1;
wire	SYNTHESIZED_WIRE_2;
wire	SYNTHESIZED_WIRE_3;
wire	SYNTHESIZED_WIRE_4;
wire	SYNTHESIZED_WIRE_5;





lab2_LookaheadCarry	b2v_inst(
	.c0(c0),
	.clk(clock),
	.cclr(cclr),
	.a(a[3:0]),
	.b(b[3:0]),
	.carry_out(SYNTHESIZED_WIRE_0),
	.sum(out_ALTERA_SYNTHESIZED[3:0]));


lab2_LookaheadCarry	b2v_inst2(
	.c0(SYNTHESIZED_WIRE_0),
	.clk(clock),
	.cclr(cclr),
	.a(a[7:4]),
	.b(b[7:4]),
	.carry_out(SYNTHESIZED_WIRE_1),
	.sum(out_ALTERA_SYNTHESIZED[7:4]));


lab2_LookaheadCarry	b2v_inst3(
	.c0(SYNTHESIZED_WIRE_1),
	.clk(clock),
	.cclr(cclr),
	.a(a[11:8]),
	.b(b[11:8]),
	.carry_out(SYNTHESIZED_WIRE_2),
	.sum(out_ALTERA_SYNTHESIZED[11:8]));


lab2_LookaheadCarry	b2v_inst4(
	.c0(SYNTHESIZED_WIRE_2),
	.clk(clock),
	.cclr(cclr),
	.a(a[15:12]),
	.b(b[15:12]),
	.carry_out(carry_out),
	.sum(out_ALTERA_SYNTHESIZED[15:12]));


lab2_LookaheadCarry	b2v_inst5(
	.c0(carry_out),
	.clk(clock),
	.cclr(cclr),
	.a(a[19:16]),
	.b(b[19:16]),
	.carry_out(SYNTHESIZED_WIRE_3),
	.sum(out_ALTERA_SYNTHESIZED[19:16]));


lab2_LookaheadCarry	b2v_inst6(
	.c0(SYNTHESIZED_WIRE_3),
	.clk(clock),
	.cclr(cclr),
	.a(a[23:20]),
	.b(b[23:20]),
	.carry_out(SYNTHESIZED_WIRE_4),
	.sum(out_ALTERA_SYNTHESIZED[23:20]));


lab2_LookaheadCarry	b2v_inst7(
	.c0(SYNTHESIZED_WIRE_4),
	.clk(clock),
	.cclr(cclr),
	.a(a[27:24]),
	.b(b[27:24]),
	.carry_out(SYNTHESIZED_WIRE_5),
	.sum(out_ALTERA_SYNTHESIZED[27:24]));


lab2_LookaheadCarry	b2v_inst8(
	.c0(SYNTHESIZED_WIRE_5),
	.clk(clock),
	.cclr(cclr),
	.a(a[31:28]),
	.b(b[31:28]),
	.carry_out(carry_out3),
	.sum(out_ALTERA_SYNTHESIZED[31:28]));

assign	out = out_ALTERA_SYNTHESIZED;

endmodule
