module div_20(clk,rco,en);
input clk,en;
output rco;
reg rco;
reg [25:0] tmp;
	always @(posedge clk or posedge en)
	if(en) 
		begin
			tmp<=0;
			rco<=0;
		end
	else
	if (tmp==1) //10000000
		begin
			tmp<=0;
			rco<=~rco;
		end
		
	else
		tmp<=tmp+1;
endmodule
