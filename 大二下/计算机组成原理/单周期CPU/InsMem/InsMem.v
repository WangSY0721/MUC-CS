module InsMem(
	input [31:0] Addr,
	output reg [31:0] Iout
);

reg[7:0] ram[128:0];
integer i;

always@(Addr)
begin
	ram[0]=8'b10101000;
	ram[1]=8'b00000001;
	ram[2]=8'b00000000;
	ram[3]=8'b00000000;

	ram[4]=8'b00100000;
	ram[5]=8'b00000010;
	ram[6]=8'b00000000;
	ram[7]=8'b00000001;

	ram[8]=8'b00100000;
	ram[9]=8'b00000011;
	ram[10]=8'b00000000;
	ram[11]=8'b00000001;

	ram[12]=8'b00000000;
	ram[13]=8'b00100010;
	ram[14]=8'b00010000;
	ram[15]=8'b00101101;

	ram[16]=8'b00000000;
	ram[17]=8'b00100011;
	ram[18]=8'b00001000;
	ram[19]=8'b00100100;

	ram[20]=8'b00010100;
	ram[21]=8'b00100011;
	ram[22]=8'b11111111;
	ram[23]=8'b11111101;

	ram[24]=8'b00010000;
	ram[25]=8'b11000111;
	ram[26]=8'b11111111;
	ram[27]=8'b11111001;

	Iout[31:24]=ram[Addr];
	Iout[23:16]=ram[Addr+1];
	Iout[15:8]=ram[Addr+2];
	Iout[7:0]=ram[Addr+3];
end
endmodule