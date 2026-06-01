library verilog;
use verilog.vl_types.all;
entity MultiCycleCPU is
    port(
        CLK1            : in     vl_logic;
        Reset           : in     vl_logic;
        en              : in     vl_logic;
        halt            : in     vl_logic;
        x               : in     vl_logic_vector(3 downto 0);
        result          : out    vl_logic_vector(31 downto 0);
        out1            : out    vl_logic_vector(6 downto 0);
        out2            : out    vl_logic_vector(6 downto 0);
        out3            : out    vl_logic_vector(6 downto 0);
        out4            : out    vl_logic_vector(6 downto 0);
        out5            : out    vl_logic_vector(6 downto 0);
        out6            : out    vl_logic_vector(6 downto 0);
        out7            : out    vl_logic_vector(6 downto 0);
        out8            : out    vl_logic_vector(6 downto 0)
    );
end MultiCycleCPU;
