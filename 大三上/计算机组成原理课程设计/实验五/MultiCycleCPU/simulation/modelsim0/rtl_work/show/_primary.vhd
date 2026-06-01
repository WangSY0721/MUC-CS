library verilog;
use verilog.vl_types.all;
entity show is
    port(
        result          : in     vl_logic_vector(31 downto 0);
        whether_show    : in     vl_logic;
        out1            : out    vl_logic_vector(6 downto 0);
        out2            : out    vl_logic_vector(6 downto 0);
        out3            : out    vl_logic_vector(6 downto 0);
        out4            : out    vl_logic_vector(6 downto 0);
        out5            : out    vl_logic_vector(6 downto 0);
        out6            : out    vl_logic_vector(6 downto 0);
        out7            : out    vl_logic_vector(6 downto 0);
        out8            : out    vl_logic_vector(6 downto 0)
    );
end show;
