module Extend(
	input [15:0] imme,
	output reg [31:0] extendImme
);
//暂时都设置成有符号扩展
always @(imme)
begin
	extendImme[15:0]=imme;
	if(imme[15]==1)
		begin
			extendImme[31:16]=16'hFFFF;
		end
	else
		begin
			extendImme[31:16]=16'h0000;
		end
end
endmodule