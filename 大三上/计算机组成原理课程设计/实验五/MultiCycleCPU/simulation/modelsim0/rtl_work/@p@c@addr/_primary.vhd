library verilog;
use verilog.vl_types.all;
entity PCAddr is
    port(
        CLK             : in     vl_logic;
        PCSrc           : in     vl_logic_vector(2 downto 0);
        immediate       : in     vl_logic_vector(31 downto 0);
        addr            : in     vl_logic_vector(25 downto 0);
        curPC           : in     vl_logic_vector(31 downto 0);
        nextPC          : out    vl_logic_vector(31 downto 0)
    );
end PCAddr;
