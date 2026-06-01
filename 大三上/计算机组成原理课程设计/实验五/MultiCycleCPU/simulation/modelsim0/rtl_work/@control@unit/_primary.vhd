library verilog;
use verilog.vl_types.all;
entity ControlUnit is
    generic(
        \IF\            : integer := 0;
        ID              : integer := 1;
        EXE             : integer := 2;
        MEM             : integer := 3;
        WB              : integer := 4;
        \HALT\          : integer := 5
    );
    port(
        CLK             : in     vl_logic;
        halt            : in     vl_logic;
        zero            : in     vl_logic;
        op              : in     vl_logic_vector(5 downto 0);
        funct           : in     vl_logic_vector(5 downto 0);
        whether_input   : out    vl_logic;
        whether_output  : out    vl_logic;
        PCWre           : out    vl_logic;
        ExtSel          : out    vl_logic;
        InsMemRW        : out    vl_logic;
        RegDst          : out    vl_logic;
        RegWre          : out    vl_logic;
        ALUSrcA         : out    vl_logic;
        ALUSrcB         : out    vl_logic;
        PCSrc           : out    vl_logic_vector(2 downto 0);
        ALUOp           : out    vl_logic_vector(4 downto 0);
        mRD             : out    vl_logic;
        mWR             : out    vl_logic;
        DBDataSrc       : out    vl_logic
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of \IF\ : constant is 1;
    attribute mti_svvh_generic_type of ID : constant is 1;
    attribute mti_svvh_generic_type of EXE : constant is 1;
    attribute mti_svvh_generic_type of MEM : constant is 1;
    attribute mti_svvh_generic_type of WB : constant is 1;
    attribute mti_svvh_generic_type of \HALT\ : constant is 1;
end ControlUnit;
