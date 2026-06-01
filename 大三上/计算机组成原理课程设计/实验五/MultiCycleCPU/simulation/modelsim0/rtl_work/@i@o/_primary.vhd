library verilog;
use verilog.vl_types.all;
entity IO is
    port(
        x               : in     vl_logic_vector(3 downto 0);
        whether_input   : in     vl_logic;
        whether_output  : in     vl_logic;
        InPut           : out    vl_logic_vector(3 downto 0);
        whether_show    : out    vl_logic
    );
end IO;
