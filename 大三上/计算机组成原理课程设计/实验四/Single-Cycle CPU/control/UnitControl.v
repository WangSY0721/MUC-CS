module UnitControl(
	input [5:0]op,
	input [5:0]func,
	
	output reg [4:0] ALUOp,
	
	output reg jump,		//J型
	output reg Branch,	//是否是分支指令
	//使能信号
	output reg Memwre,	//存储器写不写 0表示不写
	output reg Memread,	//存储器读不读 0表示不读
	output reg Regwre,	//寄存器写不写 0表示不写
	//选择信号
	output reg ALUsrc,	//读立即数扩展还是寄存器中取值 0表示从寄存器中读取
	output reg RegDst,	//是I型信号写rt,是R型信号写rd 0表示读入rd
	output reg MemtoReg, //存储器到寄存器还是,(R型信号)ALU运算结果到寄存器 1表示读入运算结果到寄存器
	output reg Pcwre		//停机信号
);

always @(op or func)
begin
	//R型的性质	 RegDst|Menwre|Branch|ALUsrc|SExtend|PCWre=0 MemtoReg&RegWre=1
	jump=(op==6'b000010)?1:0;													//JUMP,为1跳
	Branch=(op==6'b000100||op==6'b000101)?1:0; 												//BEQ,为1的时候是分支指令
	
	Memwre=(op==6'b101011)?1:0;   											//为sw指令是为存字，此时写信号有效为1
	Memread=(op==6'b100011||op==6'b101010)?1:0;												//lw指令需要读存储器
	Regwre=(op==6'b000000||op==6'b100011||op==6'b001000||op==6'b101010)?1:0;		//lw指令和R型指令和addi需要写寄存器，1表示寄存器需要写
	
	ALUsrc=(op==6'b000000||op==6'b000100||op==6'b000101)?1:0;							//R型指令和beq指令，1表示从寄存器中读取，0表示立即数
	RegDst=(op==6'b000000)?0:1;												//R型指令，0表示写入寄存器11:15 rd,1表示写入寄存器16:20 rt
	MemtoReg=(op==6'b100011||op==6'b101010)?1:0;												//1表示此时是存储器中的值存入寄存器堆读数据端口中，0表示读取ALU运算结果至寄存器堆读数据端口中
	Pcwre=(op==6'b111111)?0:1;													//为0表示停机，此时操作码是6‘b111111，1表示不停机

	//R型指令
	if(op==6'b000000)
	begin
		case(func)
			6'b100000:
				ALUOp=5'b00000;//left			<< sll
			6'b100001:
				ALUOp=5'b00001;//ari right 	>> sra
			6'b100010:
				ALUOp=5'b00010;//logic right 	>>> srl
			6'b100011:
				ALUOp=5'b00011;//+
			6'b100100:
				ALUOp=5'b00100;//-
			6'b100101:
				ALUOp=5'b00101;//&
			6'b100110:
				ALUOp=5'b00110;//|
			6'b100111:
				ALUOp=5'b00111;//^
			6'b101000:
				ALUOp=5'b01000;//~|
			6'b101001:
				ALUOp=5'b01001;//slt
			6'b101010:
				ALUOp=5'b01010;//sltu
			6'b101011:
				ALUOp=5'b01011;//
			6'b101100:
				ALUOp=5'b01100;//
			6'b101101:
				ALUOp=5'b01101;// *
			6'b101110:
				ALUOp=5'b01110;// /
		endcase
	end
	
	else
	begin
		case(op)
		6'b000100:
			ALUOp=5'b00100; 				//BEQ,相等说明减法后为0，zero=1，且branch=1
		6'b000101:
			ALUOp=5'b01111;				//BNE,不相等后跳转
		6'b100011:
			ALUOp=5'b00011;				//lw,地址为寄存器的值和立即数扩展后相加，送入存储器取得值再送入rt
		6'b101011:
			ALUOp=5'b00011;				//sw,地址为寄存器的值和立即数扩展后相加，值为rt,一起送入存储器
		6'b001000:
			ALUOp=5'b00011;				//addi,rs+imm=rt
		endcase
	end
end
endmodule