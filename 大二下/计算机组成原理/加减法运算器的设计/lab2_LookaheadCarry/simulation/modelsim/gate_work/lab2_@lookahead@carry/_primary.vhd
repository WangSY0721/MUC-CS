library verilog;
use verilog.vl_types.all;
entity lab2_LookaheadCarry is
    port(
        a               : in     vl_logic_vector(3 downto 0);
        b               : in     vl_logic_vector(3 downto 0);
        c0              : in     vl_logic;
        clk             : in     vl_logic;
        cclr            : in     vl_logic;
        carry_out       : out    vl_logic;
        sum             : out    vl_logic_vector(3 downto 0);
        overflow        : out    vl_logic
    );
end lab2_LookaheadCarry;
