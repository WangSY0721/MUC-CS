module Timer(reset,
				clk,
				start,
				data_in,
				counter,
				mystate,
				
);

input clk,reset,start;
input [7:0]data_in;

output reg [7:0]counter;
output reg [1:0]mystate;

reg [1:0]state;
parameter [1:0] S0=0,S1=1,S2=2,S3=3;

always@(posedge clk)
begin
	if(!reset)
		begin
			if(!start)
				state<=S0;
		end
	else
	case(state)
		S0:
			if(start)
				state<=S1;
			else
				state<=S0;
		S1:
			if(start)
				state<=S1;
			else
				state<=S2;
		S2:
			if(counter==1)
				state<=S3;
			else
				state<=S2;
		S3:	
				state<=S0;
	endcase
	mystate=state;	
end
always@(posedge clk)
begin
	case(state)
	S0:
		begin
			counter<=8'b00000000;
		end
	S1:
		counter<=data_in;
	S2:
		if(counter==1)
		begin
			counter<=8'b00000000;
		end
		else
			counter<=counter-1;
	S3:
		counter<=counter;
	endcase
end

endmodule