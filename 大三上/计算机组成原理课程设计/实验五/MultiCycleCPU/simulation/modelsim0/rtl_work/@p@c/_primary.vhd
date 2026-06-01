library verilog;
use verilog.vl_types.all;
entity PC is
    port(
        CLK             : in     vl_logic;
        Reset           : in     vl_logic;
        PCWre           : in     vl_logic;
        PCSrc           : in     vl_logic_vector(2 downto 0);
        nextPC          : in     vl_logic_vector(31 downto 0);
        curPC           : out    vl_logic_vector(31 downto 0)
    );
end PC;
