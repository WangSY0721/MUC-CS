module InstructionMem(
	input [31:0] Addr,
	output reg[31:0] Iout
);

reg[7:0] ram[128:0];
integer i;
initial
begin
	$readmemb("D:/Ajzlab/lab4/instruction.txt",ram);
	//ram[0]=8'b00100000;
	//ram[1]=8'b00000001;
	//ram[2]=8'b00000000;
	//ram[3]=8'b00001010;
	//ram[4]=8'b11111100;
	//ram[5]=8'b00000000;
	//ram[6]=8'b00000000;
	//ram[7]=8'b00000000;
end

always@(Addr)
begin
	Iout[31:24]=ram[Addr];
	Iout[23:16]=ram[Addr+1];
	Iout[15:8]=ram[Addr+2];
	Iout[7:0]=ram[Addr+3];
end

endmodule