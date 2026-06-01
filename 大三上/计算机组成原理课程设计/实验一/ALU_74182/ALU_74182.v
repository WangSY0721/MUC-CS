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
// CREATED		"Wed Nov 01 12:07:01 2023"

module ALU_74182(
	PN3,
	GN3,
	PN2,
	GN2,
	PN1,
	GN1,
	PN0,
	GN0,
	CI,
	GN,
	PN,
	CZ,
	CY,
	CX
);


input wire	PN3;
input wire	GN3;
input wire	PN2;
input wire	GN2;
input wire	PN1;
input wire	GN1;
input wire	PN0;
input wire	GN0;
input wire	CI;
output wire	GN;
output wire	PN;
output wire	CZ;
output wire	CY;
output wire	CX;

wire	SYNTHESIZED_WIRE_16;
wire	SYNTHESIZED_WIRE_3;
wire	SYNTHESIZED_WIRE_4;
wire	SYNTHESIZED_WIRE_5;
wire	SYNTHESIZED_WIRE_6;
wire	SYNTHESIZED_WIRE_7;
wire	SYNTHESIZED_WIRE_8;
wire	SYNTHESIZED_WIRE_9;
wire	SYNTHESIZED_WIRE_10;
wire	SYNTHESIZED_WIRE_11;
wire	SYNTHESIZED_WIRE_12;
wire	SYNTHESIZED_WIRE_13;
wire	SYNTHESIZED_WIRE_14;
wire	SYNTHESIZED_WIRE_15;




assign	PN = PN3 | PN2 | PN1 | PN0;

assign	SYNTHESIZED_WIRE_3 = GN3 & GN2 & GN1 & GN0;

assign	SYNTHESIZED_WIRE_4 = PN1 & GN2 & GN3 & GN1;

assign	SYNTHESIZED_WIRE_5 = GN2 & PN2 & GN3;

assign	SYNTHESIZED_WIRE_6 = PN3 & GN3;

assign	SYNTHESIZED_WIRE_7 = GN2 & GN1 & GN0 & SYNTHESIZED_WIRE_16;

assign	SYNTHESIZED_WIRE_8 = GN2 & PN0 & GN1 & GN0;

assign	SYNTHESIZED_WIRE_9 = GN1 & PN1 & GN2;

assign	SYNTHESIZED_WIRE_10 = GN2 & PN2;

assign	SYNTHESIZED_WIRE_13 = SYNTHESIZED_WIRE_16 & GN1 & GN0;

assign	SYNTHESIZED_WIRE_12 = GN0 & PN0 & GN1;

assign	SYNTHESIZED_WIRE_11 = GN1 & PN1;

assign	SYNTHESIZED_WIRE_14 = GN0 & SYNTHESIZED_WIRE_16;

assign	SYNTHESIZED_WIRE_15 = GN0 & PN0;

assign	GN = SYNTHESIZED_WIRE_3 | SYNTHESIZED_WIRE_4 | SYNTHESIZED_WIRE_5 | SYNTHESIZED_WIRE_6;

assign	CZ = ~(SYNTHESIZED_WIRE_7 | SYNTHESIZED_WIRE_8 | SYNTHESIZED_WIRE_9 | SYNTHESIZED_WIRE_10);

assign	CY = ~(SYNTHESIZED_WIRE_11 | SYNTHESIZED_WIRE_12 | SYNTHESIZED_WIRE_13);

assign	CX = ~(SYNTHESIZED_WIRE_14 | SYNTHESIZED_WIRE_15);

assign	SYNTHESIZED_WIRE_16 =  ~CI;


endmodule
