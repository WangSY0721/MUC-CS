library verilog;
use verilog.vl_types.all;
entity SignZeroExtend is
    port(
        immediate       : in     vl_logic_vector(15 downto 0);
        ExtSel          : in     vl_logic;
        extendImmediate : out    vl_logic_vector(31 downto 0)
    );
end SignZeroExtend;
