library verilog;
use verilog.vl_types.all;
entity lab2_3 is
    port(
        carry_out3      : out    vl_logic;
        c0              : in     vl_logic;
        clock           : in     vl_logic;
        cclr            : in     vl_logic;
        a               : in     vl_logic_vector(31 downto 0);
        b               : in     vl_logic_vector(31 downto 0);
        \out\           : out    vl_logic_vector(31 downto 0)
    );
end lab2_3;
