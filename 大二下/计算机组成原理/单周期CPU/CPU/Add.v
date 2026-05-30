module Add(
	input [31:0] DataA,DataB,
	output reg [31:0] sum 
);
always @(DataA or DataB)
begin
	sum=DataA+DataB;
end
endmodule