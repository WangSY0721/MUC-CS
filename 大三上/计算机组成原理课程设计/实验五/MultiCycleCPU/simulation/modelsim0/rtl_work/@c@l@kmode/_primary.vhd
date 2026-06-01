library verilog;
use verilog.vl_types.all;
entity CLKmode is
    port(
        CLK1            : in     vl_logic;
        CLK             : out    vl_logic
    );
end CLKmode;
