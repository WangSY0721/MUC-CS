module inputNumber(
	input clk,
	input [7:0] RandomNumber,
	output reg [7:0] OutputRandomNumber
);

always @(posedge clk)
begin
	OutputRandomNumber<=RandomNumber;
end

endmodule