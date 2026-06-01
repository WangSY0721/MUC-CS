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
// CREATED		"Wed Nov 01 13:07:32 2023"

module ALU_64bit(
	M,
	c,
	a,
	b,
	s,
	f
);


input wire	M;
input wire	c;
input wire	[63:0] a;
input wire	[63:0] b;
input wire	[3:0] s;
output wire	[63:0] f;

wire	c1;
wire	c2;
wire	c3;
wire	[63:0] f_ALTERA_SYNTHESIZED;
wire	g1;
wire	g2;
wire	g3;
wire	g4;
wire	p1;
wire	p2;
wire	p3;
wire	p4;





ALU_16bit	b2v_inst(
	.M(M),
	.c(c),
	.a(a[15:0]),
	.b(b[15:0]),
	.s(s),
	.p(p1),
	.g(g1),
	.f(f_ALTERA_SYNTHESIZED[15:0]));


ALU_16bit	b2v_inst2(
	.M(M),
	.c(c1),
	.a(a[31:16]),
	.b(b[31:16]),
	.s(s),
	.p(p2),
	.g(g2),
	.f(f_ALTERA_SYNTHESIZED[31:16]));


ALU_16bit	b2v_inst3(
	.M(M),
	.c(c2),
	.a(a[47:32]),
	.b(b[47:32]),
	.s(s),
	.p(p3),
	.g(g3),
	.f(f_ALTERA_SYNTHESIZED[47:32]));


ALU_16bit	b2v_inst5(
	.M(M),
	.c(c3),
	.a(a[63:48]),
	.b(b[63:48]),
	.s(s),
	.p(p4),
	.g(g4),
	.f(f_ALTERA_SYNTHESIZED[63:48]));


ALU_74182	b2v_inst6(
	.PN3(p4),
	.GN3(p3),
	.PN2(p2),
	.GN2(p1),
	.PN1(g4),
	.GN1(g3),
	.PN0(g2),
	.GN0(g1),
	.CI(c),
	
	
	.CZ(c3),
	.CY(c2),
	.CX(c1));

assign	f = f_ALTERA_SYNTHESIZED;

endmodule
