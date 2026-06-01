module inputextend(
	input [7:0] RandomNumber,
	output reg [31:0] outputNumber
);
always@(RandomNumber)
begin
	outputNumber={24'b0,RandomNumber};
end
endmodule