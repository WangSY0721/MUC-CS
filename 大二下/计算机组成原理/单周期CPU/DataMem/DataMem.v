module DataMem(
	input Wren,
	input Read,
	input [31:0] DAddr,
	input [31:0] Data,
	output reg [31:0] Mout
);

reg [7:0] Ram[0:31];

integer i;
initial
begin
	for(i=0;i<32;i=i+1)
		Ram[i]<=0;
end

always@(DAddr or Wren or Read or Data)
begin
	//lw
	if(Read)
	begin
		Mout[7:0]=Ram[DAddr+3];
		Mout[15:8]=Ram[DAddr+2];
		Mout[23:16]=Ram[DAddr+1];
		Mout[31:24]=Ram[DAddr];
	end
	
	//sw
	if(Wren)
	begin
		Ram[DAddr+3]=Data[7:0];
		Ram[DAddr+2]=Data[15:8];
		Ram[DAddr+1]=Data[23:16];
		Ram[DAddr]=Data[31:24];
	end
end
endmodule 