module ALU_74182(
  input wire PN3,
  input wire GN3,
  input wire PN2,
  input wire GN2,
  input wire PN1,
  input wire GN1,
  input wire PN0,
  input wire GN0,
  input wire CI,
  output wire GN,
  output wire PN,
  output wire CZ,
  output wire CY,
  output wire CX
);

  // 对输入信号进行逻辑运算
  wire wire1 = PN0 & GN1;
  wire wire2 = GN0 & PN1;
  wire wire3 = GN0 | PN2 | GN2 | PN3;
  wire wire4 = GN0 & GN1 & GN2 & GN3;
  wire wire5 = GN0 | GN1 | GN2 | GN3;
  wire wire6 = PN0 | PN1 | PN2 | PN3;
  wire wire7 = GN0 & GN1 & PN2;
  wire wire8 = GN0 | PN1 | PN2;
  wire wire9 = GN0 & GN2 & PN3;
  wire wire10 = GN0 | GN1 | PN2;
  wire wire11 = GN1 | GN2 | PN3;
  wire wire12 = GN0 & PN1;
  wire wire13 = GN2 & PN3;
  wire wire14 = GN2 | PN3;
  wire wire15 = GN0 & GN1;
  wire wire16 = GN0 & GN2;
  wire wire17 = GN0 & GN3;
  wire wire18 = PN1 & GN2;
  wire wire19 = GN1 & PN2;
  wire wire20 = GN3 & PN0;
  wire wire21 = GN2 & GN3;
  wire wire22 = GN1 & GN2 & GN3;
  wire wire23 = GN1 & GN2;
  wire wire24 = GN1 & PN1;
  wire wire25 = GN3 & PN1;
  wire wire26 = GN3 | PN3;

  // 输出信号赋值
  assign GN = wire4 | wire5 | wire13 | wire21 | wire22 | wire25 | wire26;
  assign PN = wire6;
  assign CZ = ~(wire7 | wire8 | wire12 | wire18 | wire19);
  assign CY = ~(wire11 | wire16 | wire17 | wire20 | wire23 | wire24);
  assign CX = ~(wire9 | wire10 | wire14 | wire15);

endmodule