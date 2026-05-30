module Left(
	input [31:0] datain,
	output reg [31:0] dataout
);

always @(datain)
begin
	dataout[31:2]=datain[29:0];
	dataout[1:0]=2'b00;
end

endmodule
