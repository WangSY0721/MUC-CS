module Multiplier(clk,reset,start,x,y,p,temp,states,done);

input clk,reset,start;
input [3:0]x,y;

output reg[8:0]p;		//9位的部分积
output reg[2:0]states;
output reg done;
output reg [4:0]temp;

reg [3:0]rx,ry;
reg [2:0] state;
parameter [2:0]S0=0,S1=1,S2=2,S3=3,S4=4;

always@(posedge clk)
begin
	if(reset)
	begin
		if(!start)
			state<=S0;
	end
	
	else
	begin
		case(state)
			S0:
				if(start)
					state<=S1;
				else	
					state<=S0;
			S1:
					state<=S2;
			S2:
				state<=S3;
			S3:
				state<=S4;
			S4:
				if(start)
					state<=S0;
				else
					state<=S4;
		endcase
	end
	states=state;
end

// 计算逻辑
always @* begin
    case(state)
        S0: begin
            rx = x;
            ry = y;
            temp = 5'b00000;
            p = {5'b00000, y};
            done = 0;
        end
        S1, S2, S3, S4: begin
            if (p[0] == 1)
                temp = p[8:4] + {1'b0, rx};
            else
                temp = p[8:4];
            p = {1'b0, temp, p[3:1]};
            if (state == S4)
                done = 1;
        end
    endcase
end
endmodule