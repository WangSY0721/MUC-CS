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
// CREATED		"Wed Nov 01 13:03:10 2023"

module ALU_16bit(
	M,
	c,
	a,
	b,
	s,
	p,
	g,
	f
);


input wire	M;
input wire	c;
input wire	[15:0] a;
input wire	[15:0] b;
input wire	[3:0] s;
output wire	p;
output wire	g;
output wire	[15:0] f;

wire	c1;
wire	c2;
wire	c3;
wire	[15:0] f_ALTERA_SYNTHESIZED;
wire	[3:0] g_ALTERA_SYNTHESIZED;
wire	[3:0] p_ALTERA_SYNTHESIZED;




ALU_74181	b2v_inst5(
	.s(s),
	.b(b[3:0]),
	.a(a[3:0]),
	.ci(c),
	.M(M),
	.f(f_ALTERA_SYNTHESIZED[3:0]),
	.PN(p_ALTERA_SYNTHESIZED[0]),
	.GN(g_ALTERA_SYNTHESIZED[0]));


ALU_74181	b2v_inst(
	.s(s),
	.b(b[7:4]),
	.a(a[7:4]),
	.ci(c1),
	.M(M),
	.f(f_ALTERA_SYNTHESIZED[7:4]),
	.PN(p_ALTERA_SYNTHESIZED[1]),
	.GN(g_ALTERA_SYNTHESIZED[1]));


ALU_74181	b2v_inst6(
	.s(s),
	.b(b[11:8]),
	.a(a[11:8]),
	.ci(c2),
	.M(M),
	.f(f_ALTERA_SYNTHESIZED[11:8]),
	.PN(p_ALTERA_SYNTHESIZED[2]),
	.GN(g_ALTERA_SYNTHESIZED[2]));


ALU_74181	b2v_inst7(
	.s(s),
	.b(b[15:12]),
	.a(a[15:12]),
	.ci(c3),
	.M(M),
	.f(f_ALTERA_SYNTHESIZED[15:12]),
	.PN(p_ALTERA_SYNTHESIZED[3]),
	.GN(g_ALTERA_SYNTHESIZED[3]));


ALU_74182	b2v_inst8(
	.PN3(p_ALTERA_SYNTHESIZED[3]),
	.GN3(g_ALTERA_SYNTHESIZED[3]),
	.PN2(p_ALTERA_SYNTHESIZED[2]),
	.GN2(g_ALTERA_SYNTHESIZED[2]),
	.PN1(p_ALTERA_SYNTHESIZED[1]),
	.GN1(g_ALTERA_SYNTHESIZED[1]),
	.PN0(p_ALTERA_SYNTHESIZED[0]),
	.GN0(g_ALTERA_SYNTHESIZED[0]),
	.CI(c),
	.GN(g),
	.PN(p),
	.CZ(c3),
	.CY(c2),
	.CX(c1));

assign	f = f_ALTERA_SYNTHESIZED;

endmodule
