library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_unsigned.all;
use IEEE.std_logic_arith.all;

-- use IEEE.numeric_std.all;

-------------------------------------------------------------------------------
entity Controller is
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
    RAM_DEP_din    : out STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0); -- 1+NBDEP+NBDEP*ADDRWIDTH
    RAM_DEP_wen    : out STD_LOGIC;
    RAM_DEP_wraddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
    RAM_DEP_rdaddr : out STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
    RAM_DEP_dout   : in  STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0)  -- 1+NBDEP+NBDEP*ADDRWIDTH 
    );
    
end Controller;

-------------------------------------------------------------------------------
architecture RTL of Controller is
  -----------------------------------------------------------------------------
  type FSM_STATE_IN  is (S_RESET_IN, S_CMD_WAIT, S_WRITE_RES_REQ, S_UPDATE_READ, S_UPDATE_WRITE, S_RAM_INIT);
  type FSM_STATE_OUT is (S_RESET_OUT, S_READ_RES_REQ, S_READ_DEP_REQ, S_TEST_IsExecuted, S_INC_ADDR, S_SEND_TASK, S_GOTO_START);
  
  signal S_IN_Current,  S_IN_Future  : FSM_STATE_IN  := S_RESET_IN;
  signal S_OUT_Current, S_OUT_future : FSM_STATE_OUT := S_RESET_OUT;
  
  signal RAM_RES_din_i    : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0);
  signal RAM_RES_wen_i    : STD_LOGIC;
  signal RAM_RES_wraddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_RES_rdaddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  
  signal RAM_DEP_din_i    : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0); -- 1+NBDEP+NBDEP*ADDRWIDTH 
  signal RAM_DEP_wen_i    : STD_LOGIC;
  signal RAM_DEP_wraddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  signal RAM_DEP_rdaddr_i : STD_LOGIC_VECTOR (ADDRWIDTH-1 downto 0);
  
  signal DataOut_i : STD_LOGIC_VECTOR (3*DATAWIDTH-1 downto 0);
  
  type TAB_ADDRDEP is array (natural range <>) of std_logic_vector(ADDRWIDTH-1  downto 0);
  signal AddrDep         : TAB_ADDRDEP(NBDEP-1 downto 0);
  signal IsExecuted      : std_logic;
  signal DependencyBits  : std_logic_vector(NBDEP-1  downto 0);
  signal Result          : std_logic_vector(DATAWIDTH-1  downto 0);
  signal ResAddress      : std_logic_vector(ADDRWIDTH-1  downto 0);
  
  constant DEPSATISFIED  : std_logic_vector(NBDEP-1  downto 0) := (others=>'1');
  
  signal AddressMax      : std_logic_vector(ADDRWIDTH-1 downto 0) := (others=>'0');
  signal CurDEP_RdAddr   : std_logic_vector(ADDRWIDTH-1 downto 0);
  signal CurRES_RdAddr   : std_logic_vector(ADDRWIDTH-1 downto 0);
  signal StartDEP_RdAddr : std_logic_vector(ADDRWIDTH-1 downto 0);
  signal NewRes_DepRdAddr   : std_logic_vector(ADDRWIDTH-1 downto 0);
  
  constant NULLDATA      : STD_LOGIC_VECTOR (DATAWIDTH-1 downto 0) := (others=>'0');
  
  -----------------------------------------------------------
  -- COMMAND VALUES :
  constant INIT_RAM    : natural := 1;
  constant TASK_RESULT : natural := 2;
  constant None        : natural := 0;
    
  signal Cmd           : std_logic_vector(DATAWIDTH-1  downto 0);
  signal RAMAddress_Rd : std_logic_vector(ADDRWIDTH-1 downto 0);
  signal Value         : std_logic_vector(DATAWIDTH-1 downto 0);
    
  type DepTable is array (natural range <>) of std_logic_vector(ADDRWIDTH-1 downto 0);
  signal RdDepAddr_Tab : DepTable(NBDEP-1 downto 0) := (others=>(others=>'0'));
  
  signal DEP_MASK : std_logic_vector(DATAWIDTH-1 downto 0);
  signal DEP_VECT : std_logic_vector(NBDEP-1 downto 0);
  
  signal DepBitSetting : std_logic := '0';
  
begin

  Cmd      <= DataIn(2*DATAWIDTH+Cmd'length-1 downto 2*DATAWIDTH) when InReq='1' else Cmd;
  Value    <= DataIn(DATAWIDTH-1 downto 0) when InReq='1' else Value;
  
  -- RAM INITIALIZATION COMMAND
  RAMAddress_Rd <= DataIn(DATAWIDTH+ADDRWIDTH-1 downto DATAWIDTH) when InReq='1' else RAMAddress_Rd;
  
  -- STORE RESULTS COMMAND
  TaskDep: for i in 0 to NBDEP-1 generate
    RdDepAddr_Tab(i)  <= RAM_DEP_dout(i*ADDRWIDTH+ADDRWIDTH-1 downto i*ADDRWIDTH);
    DEP_VECT(i)       <= '1' when RdDepAddr_Tab(i)=ResAddress else '0';
  end generate;
  
  ResAddress <= RAMAddress_Rd when S_IN_Current=S_WRITE_RES_REQ else
                ResAddress; -- Save result address for dependency updates
  
  DEP_MASK <= '0' & DEP_VECT & NULLDATA(DATAWIDTH-1-NBDEP-1 downto 0);
  
  AddressMax <= RAMAddress_Rd when S_IN_Current=S_RAM_INIT else AddressMax;
  
  -----------------------------------------------------------------------------
  -- purpose: Assign current state with future state
  FSM_MEM: process (CLk, Rst)
  begin  -- process FSM_MEM
    if rising_edge(CLk) then  -- rising clock edge
      if Rst = '1' then                   -- asynchronous reset (active high)
        S_IN_Current  <= S_RESET_IN;
        S_OUT_Current <= S_RESET_OUT;
      else
        S_IN_Current  <= S_IN_Future;
        S_OUT_Current <= S_OUT_Future; 
      end if;
    end if;
  end process FSM_MEM;
 
  -----------------------------------------------------------------------------
  -- purpose: Assign future state from current state and inputs
  -- type   : combinational
  INCOMING_PROCESS: process (S_IN_Current, InReq, Cmd)
  begin  -- process INCOMING_PROCESS
    case S_IN_Current is
      ---------------------------------
      when S_RESET_IN => 
        S_IN_Future <= S_CMD_WAIT;
      
      ---------------------------------
      -- READY FOR CMD RECEIVING
      when S_CMD_WAIT =>
        if InReq='1' then
          if Cmd=TASK_RESULT then
            S_IN_Future <= S_WRITE_RES_REQ;
          elsif Cmd=INIT_RAM then
            S_IN_Future <= S_RAM_INIT;
          else
            S_IN_Future <= S_RESET_IN;
          end if;
        else
          S_IN_Future <= S_CMD_WAIT;
        end if;
        
      ---------------------------------
      -- WRITE REQUEST AT ADDRESS [IN DATAIN] (TASK NUMBER)
      when S_WRITE_RES_REQ =>
        S_IN_Future <= S_UPDATE_READ;
        
      ---------------------------------
      -- READ Dependency addresses for update
      when S_UPDATE_READ =>
        if DepBitSetting='0' then
          S_IN_Future <= S_CMD_WAIT; -- end of dependency update
        elsif DEP_MASK/=NULLDATA(NBDEP-1 downto 0) then
          S_IN_Future <= S_UPDATE_WRITE;
        else
          S_IN_Future <= S_UPDATE_READ;
        end if;
        
      ---------------------------------
      -- update DEPENDENCY BITS
      when S_UPDATE_WRITE =>
        S_IN_Future <= S_UPDATE_READ;
                  
      ---------------------------------
      -- WRITE RESULT
      when S_RAM_INIT =>
        S_IN_Future <= S_CMD_WAIT;
        
      ---------------------------------
      when others => null;
    end case;
    
  end process INCOMING_PROCESS;
 -----------------------------------------------------------------------------
-- OUTPUT ASSIGNMENTS
  Busy <= '1' when S_IN_Current/=S_CMD_WAIT else
          '0';
    
-------------------------------------------------------------------------------
 -- RESULTS RAM interface
  RAM_RES_wraddr_i <= RAMAddress_Rd when S_IN_Current=S_WRITE_RES_REQ else RAM_RES_wraddr_i;
  RAM_RES_wraddr   <= RAM_RES_wraddr_i;
  RAM_RES_wen_i    <= '1' when S_IN_Current=S_WRITE_RES_REQ else '0';
  RAM_RES_wen      <= RAM_RES_wen_i;
  RAM_RES_din_i    <= Value when S_IN_Current=S_WRITE_RES_REQ else RAM_RES_din_i;
  RAM_RES_din      <= RAM_RES_din_i;
  
-------------------------------------------------------------------------------
 -- RESULTS DEP interface
  RAM_DEP_wraddr_i <= RAMAddress_Rd when S_IN_Current=S_RAM_INIT else 
                      NewRes_DepRdAddr when S_IN_Current=S_UPDATE_READ or S_IN_Current=S_UPDATE_WRITE else
                      RAM_DEP_wraddr_i;
  RAM_DEP_wraddr   <= RAM_DEP_wraddr_i;
  RAM_DEP_wen_i    <= '1' when S_IN_Current=S_RAM_INIT or S_IN_Current=S_UPDATE_WRITE else '0';
  RAM_DEP_wen      <= RAM_DEP_wen_i;
  RAM_DEP_din_i    <= Value when S_IN_Current=S_RAM_INIT else 
                      (RAM_DEP_dout or DEP_MASK) when S_IN_Current=S_UPDATE_WRITE else  
                      RAM_DEP_din_i;
  RAM_DEP_din      <= RAM_DEP_din_i;
  
-------------------------------------------------------------------------------

  IsExecuted <= RAM_DEP_dout(RAM_DEP_dout'length-1);
  DependencyBits   <= RAM_DEP_dout(RAM_DEP_dout'length-3 downto RAM_DEP_dout'length-2-NBDEP);
  DepAddresses : for i in NBDEP-1 downto 0 generate
	  AddrDep(i) <= RAM_DEP_dout(RAM_DEP_dout'length-NBDEP-i*ADDRWIDTH-2 downto RAM_DEP_dout'length-NBDEP-i*ADDRWIDTH-1-ADDRWIDTH);
  end generate;
  Result <= RAM_DEP_dout(Result'length-1 downto 0);

  -----------------------------------------------------------------------------
  -- purpose: Assign future state from current state and inputs
  -- type   : combinational
  OUTCOMING_PROCESS: process (S_OUT_Current, IsExecuted, DependencyBits)
  begin  -- process OUTCOMING_PROCESS
    case S_OUT_Current is
      ---------------------------------
      -- Set current address to start point in RAM
      when S_RESET_OUT => 
        S_OUT_Future <= S_READ_DEP_REQ;
                
      ---------------------------------
      -- READ REQUEST FOR DEPENDENCIES TEST
      when S_READ_DEP_REQ =>
        S_OUT_Future <= S_TEST_IsExecuted;
      
      ---------------------------------
      -- READ FIRST ADDRESS IsExecuted / Dependency BIT
      when S_TEST_IsExecuted =>
        if IsExecuted='1' then
          S_OUT_Future <= S_INC_ADDR;
        elsif DependencyBits=DEPSATISFIED then
          S_OUT_Future <= S_SEND_TASK;
        else
          S_OUT_Future <= S_GOTO_START;
        end if;
        
      ---------------------------------
      -- INCREMENT DEPENDENCY RAM ADDRESS
      when S_INC_ADDR =>
        S_OUT_Future <= S_READ_DEP_REQ;
                
      ---------------------------------
      -- SEND TASK THROUGH NETWORK (DEPENDENCY DATA)
      when S_SEND_TASK =>
        -- PRIOR to dependency bit setting
        if DepBitSetting='1' then
          S_OUT_Future <= S_SEND_TASK; -- waiting for dep bit setting to end up
        else
          S_OUT_Future <= S_INC_ADDR;
        end if;
               
      ---------------------------------
      -- WRITE RESULT
      when S_GOTO_START =>
        S_OUT_Future <= S_READ_DEP_REQ;
        
      ---------------------------------
      when others => null;
    end case;
    
  end process OUTCOMING_PROCESS;
  
-------------------------------------------------------------------------------
-- OUTPUT ASSIGNMENTS
  RAM_RES_rdaddr   <= RAM_RES_rdaddr_i;
  RAM_RES_rdaddr_i <= RAMAddress_Rd when S_OUT_Current=S_READ_DEP_REQ else RAM_RES_rdaddr_i;
  
  RAM_DEP_rdaddr   <= RAM_DEP_rdaddr_i;
  RAM_DEP_rdaddr_i <= CurDEP_RdAddr when S_OUT_Current=S_READ_DEP_REQ and S_IN_Current/=S_UPDATE_WRITE else 
                      NewRes_DepRdAddr when S_IN_Current=S_UPDATE_WRITE else  
                      RAM_DEP_rdaddr_i;
  
  DataOut    <= DataOut_i;
  DataOut_i  <= RAM_RES_dout when S_OUT_Current=S_SEND_TASK else DataOut_i;
  
  --------------------------------------------------------------
  -- Increment/Reset CurDEP_RdAddr synchronized with FSM state
  IncDepAddr_RD : process(Clk)
  begin
    if rising_edge(Clk) then
    
      if Rst='1' then
        CurDEP_RdAddr <= (others=>'0');
        
      elsif S_OUT_Current=S_GOTO_START then
        CurDEP_RdAddr <= StartDEP_RdAddr;
        
      elsif S_OUT_Current=S_INC_ADDR then
        CurDEP_RdAddr <= CurDEP_RdAddr+1*(DATAWIDTH/8);
      
      end if;
    end if;
  
  end process;
  
  --------------------------------------------------------------
  StartDEP_RdAddr <= (others=>'0') when S_OUT_Current=S_RESET_OUT else
                     CurDEP_RdAddr when IsExecuted='1' else
                     StartDEP_RdAddr;
  --------------------------------------------------------------
  -- Increment/Reset NewRes_DepRdAddr synchronized with FSM state
  IncDepAddr_WR : process(Clk)
  begin
    if rising_edge(Clk) then
    
      if Rst='1' then
        NewRes_DepRdAddr <= StartDEP_RdAddr;
        
      elsif NewRes_DepRdAddr=AddressMax then
        NewRes_DepRdAddr <= StartDEP_RdAddr;
        
      elsif S_IN_Current=S_UPDATE_READ then
        NewRes_DepRdAddr <= NewRes_DepRdAddr+(DATAWIDTH/8);
      
      
      end if;
    end if;
  
  end process;
  --------------------------------------------------------------
  DepBitSetting <= '1' when S_IN_Current=S_UPDATE_WRITE or S_IN_Current=S_UPDATE_READ or S_IN_Current=S_WRITE_RES_REQ else '0';
-------------------------------------------------------------------------------
   
end RTL;

