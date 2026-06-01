`timescale 1ns / 1ps
//I/O,数据的输入模块
module IO(
input [3:0] x,	
input input_number,
input	output_number,
output reg [3:0] InPut,
output reg show_result
);


initial begin
	  InPut<=0;
	  show_result=0;
end
always@(input_number or output_number)
begin
	if(input_number)
		InPut=x;
	if(output_number)
		show_result=1;

end

endmodule