module lab2_RippleCarry
#(parameter WIDTH=4)
(
	input signed [WIDTH-1:0] dataa,
	input signed [WIDTH-1:0] datab,
	input add_sub,	  // if this is 1, add; else subtract
	input clk,    
	input cclr,
	input carry_in,
	output overflow,
	output carry_out,
	output reg [WIDTH-1:0] result
);

wire [WIDTH:0] dataa_temp;
wire [WIDTH:0] datab_temp;
reg  [WIDTH:0] ci_temp;
reg  [WIDTH:0] result_temp;
reg carry_in_temp;
integer i; 
integer  temp ;
assign dataa_temp[WIDTH:0]= {dataa[WIDTH-1],dataa[WIDTH-1:0]};
assign datab_temp[WIDTH:0]=(add_sub==1)?{datab[WIDTH-1],datab[WIDTH-1:0]}:~{datab[WIDTH-1],datab[WIDTH-1:0]};

assign overflow= (result_temp[WIDTH]^result_temp[WIDTH-1])==1?1'b1:1'b0; 

assign carry_out=ci_temp[WIDTH];

always @ (dataa_temp or datab_temp or carry_in )
	begin
		carry_in_temp=(add_sub==1)?{carry_in}:~{carry_in};
		ci_temp[0]=carry_in_temp;
		temp=carry_in_temp;
		result_temp[0]= dataa_temp[0]^datab_temp[0]^ci_temp[0]; 

		for (i=0;i<WIDTH;i=i+1)
		begin  
	         ci_temp[i+1]=(dataa_temp[i]^datab_temp[i])&temp|(dataa_temp[i]&datab_temp[i]);//????
	         result_temp[i+1]= dataa_temp[i+1]^datab_temp[i+1]^ci_temp[i+1]; 
	         temp=ci_temp[i+1];
	    end
	end

always @ (posedge clk or  negedge cclr)
	begin
		if (!cclr )
		begin 
		result<= 0;
		end 
		else 	
		begin 
			result[WIDTH-1:0]<=result_temp[WIDTH-1:0];
		end
	end

endmodule