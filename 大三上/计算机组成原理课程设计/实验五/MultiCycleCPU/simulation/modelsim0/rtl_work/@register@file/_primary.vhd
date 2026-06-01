library verilog;
use verilog.vl_types.all;
entity RegisterFile is
    port(
        CLK             : in     vl_logic;
        ReadReg1        : in     vl_logic_vector(4 downto 0);
        ReadReg2        : in     vl_logic_vector(4 downto 0);
        WriteData       : in     vl_logic_vector(31 downto 0);
        WriteReg        : in     vl_logic_vector(4 downto 0);
        RegWre          : in     vl_logic;
        ReadData1       : out    vl_logic_vector(31 downto 0);
        ReadData2       : out    vl_logic_vector(31 downto 0)
    );
end RegisterFile;
