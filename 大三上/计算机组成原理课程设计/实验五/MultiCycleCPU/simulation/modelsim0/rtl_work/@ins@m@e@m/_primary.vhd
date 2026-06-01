library verilog;
use verilog.vl_types.all;
entity InsMEM is
    port(
        IAddr           : in     vl_logic_vector(31 downto 0);
        InsMemRW        : in     vl_logic;
        CLK             : in     vl_logic;
        InPut           : in     vl_logic_vector(3 downto 0);
        whether_input   : in     vl_logic;
        IDataOut        : out    vl_logic_vector(31 downto 0)
    );
end InsMEM;
