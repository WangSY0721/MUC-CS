module ALU(
	input [31:0] ReadData1,	//数据A
	input [31:0] ReadData2, //数据B
	input [4:0]  sa,			//移动的位数
	input [4:0]  ALUOp,			//控制操作的信号
	output reg zero,			//零标志位
	output reg [31:0] result//得到的结果
);

reg [31:0] A;
reg [31:0] B;

always @(ReadData1 or ReadData2 or ALUOp or sa)
	begin
	//算是自带选择器了
		A=ReadData1;
		B=ReadData2;
		case(ALUOp)
			//sll
			5'b00000:
					result=B<<sa;
			//sra
			5'b00001:
					result=B>>sa;
			//srl
			5'b00010:
					result=B>>>sa;
			//add
			5'b00011:
				result=A+B;
			//sub
			5'b00100:
				result=A-B;
			//and
			5'b00101:
				result=A&B;
			//or
			5'b00110:
				result=A|B;
			//xor
			5'b00111:
				result=A^B;
			//~|
			5'b01000:
				result=~(A|B);
			//sltu
			5'b01001:
				result=(A<B)?1:0;
			//slt
			5'b01010:
				if(A[31]==B[31])
					result=(A<B)?1:0;
				else
					result=A[31];
			5'b01111:
				result=A-B;
			5'b01101:
				result=A*B;
			default:
					result=0;
		endcase
			//bne指令不相等时跳转0标志位才是1
			if(ALUOp==5'b01111)
				zero=(result==0)?0:1;
			else
				zero=(result==0)?1:0;
	end
endmodule