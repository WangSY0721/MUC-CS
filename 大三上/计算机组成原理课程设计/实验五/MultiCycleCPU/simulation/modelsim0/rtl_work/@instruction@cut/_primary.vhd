library verilog;
use verilog.vl_types.all;
entity InstructionCut is
    port(
        instruction     : in     vl_logic_vector(31 downto 0);
        op              : out    vl_logic_vector(5 downto 0);
        rs              : out    vl_logic_vector(4 downto 0);
        rt              : out    vl_logic_vector(4 downto 0);
        rd              : out    vl_logic_vector(4 downto 0);
        sa              : out    vl_logic_vector(4 downto 0);
        funct           : out    vl_logic_vector(5 downto 0);
        immediate       : out    vl_logic_vector(15 downto 0);
        addr            : out    vl_logic_vector(25 downto 0)
    );
end InstructionCut;
