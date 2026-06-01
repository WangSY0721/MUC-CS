module Mux2_1(
	input [31:0] DataA,DataB,
	input sign,
	output wire[31:0] OData4
);

//1表示选中信号A，否则则选中信号B
assign OData4=sign?DataA:DataB;
//assign OData4=DataA;
endmodule 