`timescale 1ns/1ps
//Control Unit
module ControlUnit(
input CLK,
input halt,
input zero,		//ALU运算结果是否为0,为0时候为1
input [5:0] op,	//指令的操作码
input [5:0] funct,
output reg input_number,//是否取输入数据，为1取数
output reg output_number,//是否显示的信号量，为1时候显示
output reg PCWre,		//PC是否更改的信号量,为0时候不更改，否则可以更改
output reg ExtSel,		//立即数扩展的信号量，为时候为扩展，否则为符号扩展
output reg InstMemRW,	//指令寄存器的状态操作符，为0的时候写指令寄存器，否则为读指令寄存器
output reg RegDst,		//与寄存器组寄存器的地址，为0的时候地址来自rt,为1的时候地址来自rd
output reg RegWre,		//奇存器组写使能，为1的时候可写
output reg ALUSrcA,		//控制ALU数据A的选择端的输入，为0的时候，来自寄存器堆data1输出，为1的时候来自移位数sa
output reg ALUSrcB,		//控制ALU数据B的选择端的输入，为0的时候，来自寄存器堆data2输出，为1时候来自扩展过的立即数
output reg [2:0]PCSrc, //获取 下一个pc的地址的数据选择器的选择端输入
output reg [4:0]ALUOp, //ALU 8种运算功能选择(000-111)
output reg MemRead,  //数据存储器读控制信号,为0读
output reg MemWrite,  //数据存储器写控制信号，为0写
output reg DBDataSrc //数据保存的选择端 ,为0来自ALU运算结果的输出，为1来自数据寄存器(Data MEM)的输出
);
initial begin
	InstMemRW = 1;
	PCWre = 1;
	MemRead= 0;
	MemWrite= 0;
   DBDataSrc = 0;
	input_number = 0;
	output_number = 0;
end




parameter IF=0, ID = 1, EXE = 2,MEM=3,WB=4;
reg [2:0]state,next_state;//000:if 001:ID 010:exe 011:mem 100:wb 101:HALT	  
initial begin
	  state <= IF;
end
always @(posedge CLK) 
		begin
			state <= next_state;
		end
always @(state or op or funct or halt)
 begin
		case(state)
			IF: //if
				begin
						next_state <= ID;
				end
				
			ID: //id
				begin
					case(op)
						6'b000010:
							begin
								next_state <= IF;						// j
							end
						default: 
							begin
								next_state <= EXE;						// 其他
							end
					endcase
				end
				
			EXE: //exe
				begin
					case (op)
						6'b101011: // lw
							begin
								next_state <=MEM;			 	
							end
						6'b100011: // sw
							begin
								next_state <= MEM;				
							end	
						2'h08:
							begin
								next_state <= IF;
							end
						2'h23://beq bltz
							begin
								next_state <= IF;
							end
						default:
							begin
								next_state <= WB; 					//all else(not connected with dm)
							end
					endcase
				end
			
			MEM://mem
				begin
					if(op == 6'b101011)//lw 
						begin
							next_state <= WB;												
						end
					else //sw
						begin
							next_state <= IF;						
						end			
				end
				
			WB: //wb
				begin
					next_state <=IF;	  
				end
		endcase
	end		
		
			
		
	//	
	always@(op or zero or funct )
	begin	
		if(op==6'b000001) output_number = 1;
		if(op==6'b000011) input_number = 1;
		PCWre = (op==6'b111111) ? 0 : 1; //halt
		ALUSrcB = (op == 6'b001000||op==6'b100011||op==6'b101011)? 1 : 0;//ImmorBtoALU
		ALUSrcA = ((op == 6'b000000&&funct==6'b000000)||(op == 6'b000000&&funct==6'b0000010)||(op == 6'b000000&&funct==6'b010011))? 1 : 0;//SaorAtoALU
	   DBDataSrc = (op == 6'b100011)? 1 : 0;//MemALUtoReg
	   RegWre = (op == 6'b101011||op==6'b000101||op==6'b000101||op==6'b101011)? 0 : 1;//Regwrite
		MemWrite = (op == 6'b100011) ? 1 : 0;  //sw
    	MemRead = (op == 6'b101011) ? 1 : 0;  //lw
		ExtSel = (op == 6'b000000)? 0 : 1;//Extend
	   RegDst = (op == 6'b000000)? 1 : 0;//rdrtwrite
	end
	always @(op or zero or funct or halt)
	 begin
		 if (op == 6'b000101 && zero==0) 	PCSrc=1;//bne
		 else if(halt)		PCSrc=3;//中断
		 else if (op == 6'b000010) 	PCSrc=2;//j
		 else if (op ==6'b111110) 	PCSrc=4;//关中断回原指令
		 else  PCSrc=0;
	 end

	 always @(op or funct or ALUOp)
	 begin
	 if (op == 6'b000000&&funct==6'b100000)   ALUOp=1;   		//add
	 else if (op == 6'b000000&&funct==6'b100100)   ALUOp=2;  //&
	 else if (op == 6'b000000&&funct==6'b100111)   ALUOp=3;  //nor
	 else if (op == 6'b000000&&funct==6'b100101)   ALUOp=4;	//or
	 else if (op == 6'b000000&&funct==6'b101010)   ALUOp=5;	//slt
	 else if (op == 6'b000000&&funct==6'b000000)   ALUOp=6;	//sll
	 else if (op == 6'b000000&&funct==6'b000010)   ALUOp=7;	//srl
	 else if (op == 6'b000000&&funct==6'b100010)   ALUOp=8;	//sub	
	 else if (op == 6'b000000&&funct==6'b011010)   ALUOp=9;	//div
	 else if (op == 6'b000000&&funct==6'b010000)   ALUOp=10;	//mfhi
	 else if (op == 6'b000000&&funct==6'b010010)   ALUOp=11;	//mflo
	 else if (op == 6'b000000&&funct==6'b011000)   ALUOp=12;	//mult
	 else if (op == 6'b000000&&funct==6'b000011)   ALUOp=13;	//sra
	 else if (op == 6'b000000&&funct==6'b010101)   ALUOp=21;//ddu
	 else if (op == 6'b000000&&funct==6'b011010)   ALUOp=22;//or
	 else if (op == 6'b001000)   ALUOp=14;							//addi
	 else if (op == 6'b000101)   ALUOp=15;							//bne
	 else if (op == 6'b100011)   ALUOp=16;							//lw
	 else if (op == 6'b101011)   ALUOp=17;							//sw
	 else if (op == 6'b110011)   ALUOp=18;//中断，全亮
	 else if (op == 2'h08)   ALUOp=23;							//bltz
	 else if (op == 2'h05)   ALUOp=24;							//bgez
	 else if (op == 2'h23)   ALUOp=25;							//beq
	 else if (op == 2'h2b)   ALUOp=26;							//slti
	 else if (op == 6'h01)   ALUOp=27;//ori
	 end
endmodule
