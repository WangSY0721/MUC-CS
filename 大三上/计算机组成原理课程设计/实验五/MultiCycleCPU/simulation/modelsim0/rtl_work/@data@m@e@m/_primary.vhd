library verilog;
use verilog.vl_types.all;
entity DataMEM is
    port(
        mRD             : in     vl_logic;
        mWR             : in     vl_logic;
        CLK             : in     vl_logic;
        DBDataSrc       : in     vl_logic;
        DAddr           : in     vl_logic_vector(31 downto 0);
        DataIn          : in     vl_logic_vector(31 downto 0);
        DataOut         : out    vl_logic_vector(31 downto 0);
        DB              : out    vl_logic_vector(31 downto 0)
    );
end DataMEM;
