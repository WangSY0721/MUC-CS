library verilog;
use verilog.vl_types.all;
entity lab2_4 is
    port(
        overflow        : out    vl_logic;
        c0              : in     vl_logic;
        clock           : in     vl_logic;
        cclr            : in     vl_logic;
        a               : in     vl_logic_vector(63 downto 0);
        b               : in     vl_logic_vector(63 downto 0);
        sum             : out    vl_logic_vector(63 downto 0)
    );
end lab2_4;
