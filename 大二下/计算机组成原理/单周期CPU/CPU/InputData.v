module InputData(
	input clk,
	input [7:0] inputData,
	output reg [7:0] outputData
);

always @(posedge clk)
begin
	outputData<=inputData;
end
endmodule