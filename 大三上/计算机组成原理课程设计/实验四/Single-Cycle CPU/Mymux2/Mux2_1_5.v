module Mux2_1_5(
	input [4:0] dataA,dataB,
	input sign,
	output wire [4:0] Odata
);
assign Odata=sign?dataA:dataB;
endmodule