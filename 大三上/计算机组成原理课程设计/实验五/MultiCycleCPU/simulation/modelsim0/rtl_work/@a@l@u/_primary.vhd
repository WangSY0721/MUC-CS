library verilog;
use verilog.vl_types.all;
entity ALU is
    port(
        CLK             : in     vl_logic;
        CLK1            : in     vl_logic;
        ALUSrcA         : in     vl_logic;
        ALUSrcB         : in     vl_logic;
        ReadData1       : in     vl_logic_vector(31 downto 0);
        ReadData2       : in     vl_logic_vector(31 downto 0);
        sa              : in     vl_logic_vector(4 downto 0);
        extend          : in     vl_logic_vector(31 downto 0);
        ALUOp           : in     vl_logic_vector(4 downto 0);
        zero            : out    vl_logic;
        result          : out    vl_logic_vector(31 downto 0)
    );
end ALU;
