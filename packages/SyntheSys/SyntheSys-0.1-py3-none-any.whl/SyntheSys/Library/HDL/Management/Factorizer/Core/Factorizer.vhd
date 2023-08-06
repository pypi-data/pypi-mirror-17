library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

-------------------------------------------------------------------------------
entity Factorizer is
  generic (
    DATAWIDTH : natural := 16;
    Payload   : natural := 3;
    Header    : std_logic_vector := (others=>'0');
    NBDEP     : natural := 2);
    
  port (
    Rst      : in std_logic;
    Clk      : in std_logic;
    
    -- External interface
    Debug_Idle  : out  std_logic;
    
    -- Network interface
    Rx       : in std_logic;-- Connected to NoC local TX
    AckRx    : out std_logic;-- Connected to NoC local AckTX 
    DataIn   : in std_logic_vector(DATAWIDTH-1 downto 0);-- Connected to NoC local DataOutLocal
    
    Tx       : out std_logic;-- Connected to NoC local RX
    AckTx    : in std_logic;-- Connected to NoC local AckRX
    DataOut  : out std_logic_vector(DATAWIDTH-1 downto 0));-- Connected to NoC local DataInLocal
    
end Factorizer;

-------------------------------------------------------------------------------
architecture RTL of Factorizer is

  constant ADDRWIDTH : natural := (DATAWIDTH-1-NBDEP)/NBDEP;
  -----------------------------------------------------------------------------
  component Controller
    generic (
      DATAWIDTH : natural := 32;
      ADDRWIDTH : natural := 10;
      NBDEP     : natural := 2
      );
    port (
      Rst      : in std_logic;
      Clk      : in std_logic;
      
      -- External interface
      Debug_Idle : out  std_logic;
      
      -- Control/Data interface
      InReq    : in  std_logic;
      OutReq   : out std_logic;
      Busy     : out std_logic;
      DataIn   : in  std_logic_vector(3*DATAWIDTH-1 downto 0);
      DataOut  : out std_logic_vector(3*DATAWIDTH-1 downto 0);
      
      -- DEPENDENCIES RAM interface
      RAM_RES_din    : out STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);
      RAM_RES_wen    : out STD_LOGIC;
      RAM_RES_wraddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
      RAM_RES_rdaddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
      RAM_RES_dout   : in  STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);   
      
      -- RESULTS RAM interface
      RAM_DEP_din    : out STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);
      RAM_DEP_wen    : out STD_LOGIC;
      RAM_DEP_wraddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
      RAM_DEP_rdaddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
      RAM_DEP_dout   : in  STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0)   
    );
  end component;
        
  -----------------------------------------------------------------------------
  component NetworkAdapter_HandShake_input
    generic (
      DataWidth : natural;
      Payload   : natural);
    port (
      Rst, Clk  : in  std_logic;
      Rx        : in  std_logic;
      AckRx     : out std_logic;
      DataIn    : in  std_logic_vector(DataWidth-1 downto 0);
      IP_Busy   : in  std_logic;
      IP_Req    : out std_logic;
      IP_DataIn : out std_logic_vector(Payload*DataWidth-1 downto 0));
  end component;
  
  signal IP_Busy   : std_logic;
  signal IP_Req    : std_logic;
  signal IP_DataIn : std_logic_vector(Payload*DataWidth-1 downto 0);  
  -----------------------------------------------------------------------------
  component NetworkAdapter_HandShake_output
    generic (
      DataWidth : natural;
      Payload   : natural;
      Header    : std_logic_vector);
    port (
      Rst, Clk     : in  std_logic;
      Tx           : out std_logic;
      AckTx        : in  std_logic;
      DataOut      : out std_logic_vector(DataWidth-1 downto 0);
      IP_DataValid : in  std_logic;
      IP_Wait      : out std_logic;
      IP_DataOut   : in  std_logic_vector(Payload*DataWidth-1 downto 0));
  end component;
  signal IP_DataValid : std_logic;
  signal IP_Wait      : std_logic;
  signal IP_DataOut   : std_logic_vector(Payload*DataWidth-1 downto 0);
  
  -----------------------------------------------------------------------------
  component a_sram_param
    generic (
      SIZE_ADDR_MEM : integer;
      SIZE_PORT_MEM : integer);
    port (
      din    : in  STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0);
      wen    : in  STD_LOGIC;
      wraddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0);
      rdaddr : in  STD_LOGIC_VECTOR (SIZE_ADDR_MEM-1 downto 0);
      clk    : in  STD_LOGIC;
      oclk   : in  STD_LOGIC;
      dout   : out STD_LOGIC_VECTOR (SIZE_PORT_MEM-1 downto 0));
  end component;
  
  -----------------------------------------------------------------------------
      -- DEPENDENCIES RAM interface
  signal RAM_RES_din_i    : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);
  signal RAM_RES_wen_i    : STD_LOGIC;
  signal RAM_RES_wraddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_RES_rdaddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_RES_dout_i   : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);   
      
      -- RESULTS RAM interface
  signal RAM_DEP_din_i    : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0); --1+NBDEP+NBDEP*ADDRWIDTH
  signal RAM_DEP_wen_i    : STD_LOGIC;
  signal RAM_DEP_wraddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_DEP_rdaddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_DEP_dout_i   : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0); -- 1+NBDEP+NBDEP*ADDRWIDTH
  
  
begin

  -----------------------------------------------------------------------------
  Controller_1 : Controller
    generic map (
      DATAWIDTH => DATAWIDTH,
      ADDRWIDTH => ADDRWIDTH,
      NBDEP     => NBDEP
      )
    port map (
      Rst      => Rst,
      Clk      => Clk,
      
      -- External interface
      Debug_Idle  => Debug_Idle,
      
      -- Control/Data interface
      InReq     => IP_Req,
      OutReq    => IP_DataValid,
      Busy      => IP_Busy,
      DataIn    => IP_DataIn,
      DataOut   => IP_DataOut,
      
      -- DEPENDENCIES RAM interface
      RAM_RES_din     => RAM_RES_din_i,
      RAM_RES_wen     => RAM_RES_wen_i,
      RAM_RES_wraddr  => RAM_RES_wraddr_i,
      RAM_RES_rdaddr  => RAM_RES_rdaddr_i,
      RAM_RES_dout    => RAM_RES_dout_i, 
      
      -- RESULTS RAM interface
      RAM_DEP_din     => RAM_DEP_din_i,
      RAM_DEP_wen     => RAM_DEP_wen_i,
      RAM_DEP_wraddr  => RAM_DEP_wraddr_i,
      RAM_DEP_rdaddr  => RAM_DEP_rdaddr_i,
      RAM_DEP_dout    => RAM_DEP_dout_i
    );
  -----------------------------------------------------------------------------
  a_sram_param_results : a_sram_param
    generic map (
      SIZE_ADDR_MEM => ADDRWIDTH,
      SIZE_PORT_MEM => DATAWIDTH)
    port map (
      din    => RAM_RES_din_i,
      wen    => RAM_RES_wen_i,
      wraddr => RAM_RES_WrAddr_i,
      rdaddr => RAM_RES_RdAddr_i,
      clk    => Clk,
      oclk   => Clk,
      dout   => RAM_RES_dout_i);
      
  -----------------------------------------------------------------------------
  a_sram_param_dependencies : a_sram_param
    generic map (
      SIZE_ADDR_MEM => ADDRWIDTH,
      SIZE_PORT_MEM => DATAWIDTH)
    port map (
      din    => RAM_DEP_din_i,
      wen    => RAM_DEP_wen_i,
      wraddr => RAM_DEP_WrAddr_i,
      rdaddr => RAM_DEP_RdAddr_i,
      clk    => Clk,
      oclk   => Clk,
      dout   => RAM_DEP_dout_i);
      
 -----------------------------------------------------------------------------

  --IP_DataIn_i <= IP_DataIn when IP_Req='1' else IP_DataIn_i;
  --IP_Busy     <= '1' when IP_Wait='1' else '0';
   
  -----------------------------------------------------------------------------
  NetworkAdapter_HandShake_input_1: NetworkAdapter_HandShake_input
    generic map (
      DataWidth => DATAWIDTH,
      Payload   => Payload)
    port map (
      Rst       => Rst,
      Clk       => Clk,
      Rx        => Rx,
      AckRx     => AckRx,
      DataIn    => DataIn,
      IP_Busy   => IP_Busy,
      IP_Req    => IP_Req,
      IP_DataIn => IP_DataIn);
      
  -----------------------------------------------------------------------------
  NetworkAdapter_HandShake_output_1: NetworkAdapter_HandShake_output
    generic map (
      DataWidth    => DATAWIDTH,
      Payload      => Payload,
      Header       => Header)
    port map (
      Rst          => Rst,
      Clk          => Clk,
      Tx           => Tx,
      AckTx        => AckTx,
      DataOut      => DataOut,
      IP_DataValid => IP_DataValid,
      IP_Wait      => IP_Wait,
      IP_DataOut   => IP_DataOut);

  -----------------------------------------------------------------------------
  
end RTL;

