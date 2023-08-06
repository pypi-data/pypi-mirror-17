
library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------
-- ENTITY: RS232 Handshake adapter
-------------------------------------------------------------------------------
entity PCIe_Riffa22_VC707 is
	GENERIC (
--		C_PCI_DATA_WIDTH : integer := 64;
--		C_NUM_LANES        : natural := 8;
		FlitWidth          : natural := 16
	);
	PORT (
		Clock               : IN std_logic;
		Reset               : IN std_logic;
		
		USER_CLK            : OUT std_logic;
		USER_RST            : OUT std_logic;
		
		-- PCIe FPGA pads
		PCI_EXP_TXP        : OUT std_logic_vector(8-1 downto 0);
		PCI_EXP_TXN        : OUT std_logic_vector(8-1 downto 0);
		PCI_EXP_RXP        : IN  std_logic_vector(8-1 downto 0);
		PCI_EXP_RXN        : IN  std_logic_vector(8-1 downto 0);

		LED                : OUT std_logic_vector(7 downto 0);
		PCIE_REFCLK_P      : IN  std_logic;
		PCIE_REFCLK_N      : IN  std_logic;
		PCIE_RESET_N       : IN  std_logic;
		
		-- Network interface
		Rx                 : IN  std_logic;    -- Connected to NoC local TX
		AckRx              : OUT std_logic;    -- Connected to NoC local AckTX
		DataIn             : IN  std_logic_vector(FlitWidth-1 downto 0); -- Connected to NoC local DataOutLocal

		Tx                 : OUT std_logic;    -- Connected to NoC local RX
		AckTx              : IN  std_logic;    -- Connected to NoC local AckRX
		DataOut            : OUT std_logic_vector(FlitWidth-1 downto 0)); -- Connected to NoC local DataInLocal 
		
end PCIe_Riffa22_VC707;


-------------------------------------------------------------------------------
-- ARCHITECTURE: Version 0
-------------------------------------------------------------------------------
architecture RTL of PCIe_Riffa22_VC707 is

	constant C_PCI_DATA_WIDTH : natural := 64;
	
	-- Network Rx interface 0
	signal CHNL0_RX_CLK_i        : std_logic := '0';
	signal CHNL0_RX_i            : std_logic := '0';
	signal CHNL0_RX_ACK_i        : std_logic := '0';
	signal CHNL0_RX_LAST_i       : std_logic := '0';-- not used
	signal CHNL0_RX_LEN_i        : std_logic_vector(31 downto 0) := (others=>'0');-- not used
	signal CHNL0_RX_OFF_i        : std_logic_vector(30 downto 0) := (others=>'0');-- not used
	signal CHNL0_RX_DATA_i       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal CHNL0_RX_DATA_VALID_i : std_logic := '0';
	signal CHNL0_RX_DATA_REN_i   : std_logic := '0';
	-- Network Tx interface 0
	signal CHNL0_TX_CLK_i        : std_logic := '0';
	signal CHNL0_TX_i            : std_logic := '0';
	signal CHNL0_TX_ACK_i        : std_logic := '0';
	signal CHNL0_TX_LAST_i       : std_logic := '0';-- not used
	signal CHNL0_TX_LEN_i        : std_logic_vector(31 downto 0) := (others=>'0');-- not used
	signal CHNL0_TX_OFF_i        : std_logic_vector(30 downto 0) := (others=>'0');-- not used
	signal CHNL0_TX_DATA_i       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal CHNL0_TX_DATA_VALID_i : std_logic := '0';
	signal CHNL0_TX_DATA_REN_i   : std_logic := '0';
	
	-- Network Rx interface 1
--	signal CHNL1_RX_CLK_i        : std_logic := '0';
	signal CHNL1_RX_i            : std_logic := '0';
	signal CHNL1_RX_ACK_i        : std_logic := '0';
	signal CHNL1_RX_LAST_i       : std_logic := '0';-- not used
	signal CHNL1_RX_LEN_i        : std_logic_vector(31 downto 0) := (others=>'0');-- not used
	signal CHNL1_RX_OFF_i        : std_logic_vector(30 downto 0) := (others=>'0');-- not used
	signal CHNL1_RX_DATA_i       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal CHNL1_RX_DATA_VALID_i : std_logic := '0';
	signal CHNL1_RX_DATA_REN_i   : std_logic := '0';
	-- Network Tx interface 1
--	signal CHNL1_TX_CLK_i        : std_logic := '0';
	signal CHNL1_TX_i            : std_logic := '0';
	signal CHNL1_TX_ACK_i        : std_logic := '0';
	signal CHNL1_TX_LAST_i       : std_logic := '0';-- not used
	signal CHNL1_TX_LEN_i        : std_logic_vector(31 downto 0) := (others=>'0');-- not used
	signal CHNL1_TX_OFF_i        : std_logic_vector(30 downto 0) := (others=>'0');-- not used
	signal CHNL1_TX_DATA_i       : std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0) := (others=>'0');
	signal CHNL1_TX_DATA_VALID_i : std_logic := '0';
	signal CHNL1_TX_DATA_REN_i   : std_logic := '0';
	
	signal USER_CLK_i        : std_logic := '0';
	signal USER_RST_i        : std_logic := '0';
	signal USER_PCIE_RST_i        : std_logic := '0';
	
	signal ConfigRegister_i     : std_logic_vector(FlitWidth-1 downto 0); 
	signal ConfigRegisterIdx_i  : natural := 0;
	
--	signal RiffaReset_i : std_logic := '0';
	
	COMPONENT VC707Gen1x8If64_DoubleChannel is
		GENERIC (
			-- Number of RIFFA Channels
			C_NUM_CHNL         : integer := 2;
			C_NUM_LANES        : integer := 8;
			C_PCI_DATA_WIDTH   : integer := 64;
			C_MAX_PAYLOAD_BYTES: integer := 256;
			C_LOG_NUM_TAGS     : integer := 5
		);
		PORT (
			-- PCIe FPGA pads
			PCI_EXP_TXP        : OUT std_logic_vector(C_NUM_LANES-1 downto 0);
			PCI_EXP_TXN        : OUT std_logic_vector(C_NUM_LANES-1 downto 0);
			PCI_EXP_RXP        : IN  std_logic_vector(C_NUM_LANES-1 downto 0);
			PCI_EXP_RXN        : IN  std_logic_vector(C_NUM_LANES-1 downto 0);
		
--			LED                : OUT std_logic_vector(3 downto 0);
			PCIE_REFCLK_P      : IN  std_logic;
			PCIE_REFCLK_N      : IN  std_logic;
			PCIE_RESET_N       : IN  std_logic;

			CLK                : IN  std_logic;
			RST                : OUT  std_logic;
			USER_CLK           : OUT  std_logic;
			
			-- Rx interface 0
--			CHNL0_RX_CLK        : IN  std_logic;
			CHNL0_RX            : OUT std_logic;
			CHNL0_RX_ACK        : IN  std_logic;
			CHNL0_RX_LAST       : OUT std_logic;
			CHNL0_RX_LEN        : OUT std_logic_vector(31 downto 0);
			CHNL0_RX_OFF        : OUT std_logic_vector(30 downto 0);
			CHNL0_RX_DATA       : OUT std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
			CHNL0_RX_DATA_VALID : OUT std_logic;
			CHNL0_RX_DATA_REN   : IN  std_logic;
			-- Tx interface 0
--			CHNL0_TX_CLK        : IN  std_logic;
			CHNL0_TX            : IN  std_logic;
			CHNL0_TX_ACK        : OUT std_logic;
			CHNL0_TX_LAST       : IN  std_logic;
			CHNL0_TX_LEN        : IN  std_logic_vector(31 downto 0);
			CHNL0_TX_OFF        : IN  std_logic_vector(30 downto 0);
			CHNL0_TX_DATA       : IN  std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
			CHNL0_TX_DATA_VALID : IN  std_logic;
			CHNL0_TX_DATA_REN   : OUT std_logic;
			
			-- Rx interface 1
--			CHNL1_RX_CLK        : IN  std_logic;
			CHNL1_RX            : OUT std_logic;
			CHNL1_RX_ACK        : IN  std_logic;
			CHNL1_RX_LAST       : OUT std_logic;
			CHNL1_RX_LEN        : OUT std_logic_vector(31 downto 0);
			CHNL1_RX_OFF        : OUT std_logic_vector(30 downto 0);
			CHNL1_RX_DATA       : OUT std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
			CHNL1_RX_DATA_VALID : OUT std_logic;
			CHNL1_RX_DATA_REN   : IN  std_logic;
			-- Tx interface 1
--			CHNL1_TX_CLK        : IN  std_logic;
			CHNL1_TX            : IN  std_logic;
			CHNL1_TX_ACK        : OUT std_logic;
			CHNL1_TX_LAST       : IN  std_logic;
			CHNL1_TX_LEN        : IN  std_logic_vector(31 downto 0);
			CHNL1_TX_OFF        : IN  std_logic_vector(30 downto 0);
			CHNL1_TX_DATA       : IN  std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
			CHNL1_TX_DATA_VALID : IN  std_logic;
			CHNL1_TX_DATA_REN   : OUT std_logic); -- Connected to NoC local DataInLocal 
		
	end COMPONENT VC707Gen1x8If64_DoubleChannel;
	
--	COMPONENT chnl_tester is
--		GENERIC (
--			-- Number of RIFFA Channels
--			C_PCI_DATA_WIDTH   : integer := 64);
--		PORT (
--			CLK                : IN  std_logic;
--			RST                : IN  std_logic;
--			
--			-- Rx interface 0
--			CHNL_RX_CLK        : OUT  std_logic;
--			CHNL_RX            : IN std_logic;
--			CHNL_RX_ACK        : OUT  std_logic;
--			CHNL_RX_LAST       : IN std_logic;
--			CHNL_RX_LEN        : IN std_logic_vector(31 downto 0);
--			CHNL_RX_OFF        : IN std_logic_vector(30 downto 0);
--			CHNL_RX_DATA       : IN std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
--			CHNL_RX_DATA_VALID : IN std_logic;
--			CHNL_RX_DATA_REN   : OUT  std_logic;
--			-- Tx interface 0
--			CHNL_TX_CLK        : OUT  std_logic;
--			CHNL_TX            : OUT  std_logic;
--			CHNL_TX_ACK        : IN std_logic;
--			CHNL_TX_LAST       : OUT  std_logic;
--			CHNL_TX_LEN        : OUT  std_logic_vector(31 downto 0);
--			CHNL_TX_OFF        : OUT  std_logic_vector(30 downto 0);
--			CHNL_TX_DATA       : OUT  std_logic_vector(C_PCI_DATA_WIDTH-1 downto 0);
--			CHNL_TX_DATA_VALID : OUT  std_logic;
--			CHNL_TX_DATA_REN   : IN std_logic); -- Connected to NoC local DataInLocal 
--	end COMPONENT chnl_tester;

begin  -- v0

	PCIe_Endpoint : VC707Gen1x8If64_DoubleChannel
		GENERIC MAP(
			-- Number of RIFFA Channels
			C_NUM_CHNL          =>  2,
			-- Number of PCIe Lanes
			C_NUM_LANES         =>  8,
			-- Settings from Vivado IP Generator
			C_PCI_DATA_WIDTH    => C_PCI_DATA_WIDTH,
			C_MAX_PAYLOAD_BYTES => 256,
			C_LOG_NUM_TAGS      => 8)
	
		PORT MAP(
			PCI_EXP_TXP        => PCI_EXP_TXP,
			PCI_EXP_TXN        => PCI_EXP_TXN,
			PCI_EXP_RXP        => PCI_EXP_RXP,
			PCI_EXP_RXN        => PCI_EXP_RXN,

--			LED                => open,
			PCIE_REFCLK_P      => PCIE_REFCLK_P,
			PCIE_REFCLK_N      => PCIE_REFCLK_N,
			PCIE_RESET_N       => PCIE_RESET_N,

			CLK                => Clock,
			RST                => USER_RST_i,
			USER_CLK           => USER_CLK_i,
			-- Rx interface 0
--			CHNL0_RX_CLK        => CHNL0_RX_CLK_i, 
			CHNL0_RX            => CHNL0_RX_i, 
			CHNL0_RX_ACK        => CHNL0_RX_ACK_i, 
			CHNL0_RX_LAST       => CHNL0_RX_LAST_i,
			CHNL0_RX_LEN        => CHNL0_RX_LEN_i,
			CHNL0_RX_OFF        => CHNL0_RX_OFF_i,
			CHNL0_RX_DATA       => CHNL0_RX_DATA_i, 
			CHNL0_RX_DATA_VALID => CHNL0_RX_DATA_VALID_i, 
			CHNL0_RX_DATA_REN   => CHNL0_RX_DATA_REN_i,
			-- Tx interface 0
--			CHNL0_TX_CLK        => CHNL0_TX_CLK_i, 
			CHNL0_TX            => CHNL0_TX_i, 
			CHNL0_TX_ACK        => CHNL0_TX_ACK_i, 
			CHNL0_TX_LAST       => CHNL0_TX_LAST_i,
			CHNL0_TX_LEN        => CHNL0_TX_LEN_i,
			CHNL0_TX_OFF        => CHNL0_TX_OFF_i,
			CHNL0_TX_DATA       => CHNL0_TX_DATA_i, 
			CHNL0_TX_DATA_VALID => CHNL0_TX_DATA_VALID_i,
			CHNL0_TX_DATA_REN   => CHNL0_TX_DATA_REN_i,
			
			-- Rx interface 1
--			CHNL1_RX_CLK        => CHNL1_RX_CLK_i, 
			CHNL1_RX            => CHNL1_RX_i, 
			CHNL1_RX_ACK        => CHNL1_RX_ACK_i, 
			CHNL1_RX_LAST       => CHNL1_RX_LAST_i,
			CHNL1_RX_LEN        => CHNL1_RX_LEN_i,
			CHNL1_RX_OFF        => CHNL1_RX_OFF_i,
			CHNL1_RX_DATA       => CHNL1_RX_DATA_i, 
			CHNL1_RX_DATA_VALID => CHNL1_RX_DATA_VALID_i, 
			CHNL1_RX_DATA_REN   => CHNL1_RX_DATA_REN_i,
			
			-- Tx interface 1
--			CHNL1_TX_CLK        => CHNL1_TX_CLK_i, 
			CHNL1_TX            => CHNL1_TX_i, 
			CHNL1_TX_ACK        => CHNL1_TX_ACK_i, 
			CHNL1_TX_LAST       => CHNL1_TX_LAST_i,
			CHNL1_TX_LEN        => CHNL1_TX_LEN_i,
			CHNL1_TX_OFF        => CHNL1_TX_OFF_i,
			CHNL1_TX_DATA       => CHNL1_TX_DATA_i, 
			CHNL1_TX_DATA_VALID => CHNL1_TX_DATA_VALID_i,
			CHNL1_TX_DATA_REN   => CHNL1_TX_DATA_REN_i);
	
	-----------------------------------------------------------------
	USER_PCIE_RST_i <= USER_RST_i and Reset;
	
	USER_RST <= USER_PCIE_RST_i;
	USER_CLK <= USER_CLK_i;

	-----------------------------------------------------------------
	RiffaToHS : entity work.RiffaToHS
		GENERIC MAP(
			C_PCI_DATA_WIDTH => C_PCI_DATA_WIDTH,
			FlitWidth        => FlitWidth,
			NBREG            => 16)
		PORT MAP(
			LED                => LED, --(7 downto 4)
		
			CLK                => USER_CLK_i,
			RST                => USER_PCIE_RST_i,
			-- Rx interface
--			CHNL_RX_CLK        => CHNL0_RX_CLK_i, 
			CHNL_RX            => CHNL0_RX_i, 
			CHNL_RX_ACK        => CHNL0_RX_ACK_i, 
			CHNL_RX_LAST       => CHNL0_RX_LAST_i, 
			CHNL_RX_LEN        => CHNL0_RX_LEN_i, 
			CHNL_RX_OFF        => CHNL0_RX_OFF_i, 
			CHNL_RX_DATA       => CHNL0_RX_DATA_i, 
			CHNL_RX_DATA_VALID => CHNL0_RX_DATA_VALID_i, 
			CHNL_RX_DATA_REN   => CHNL0_RX_DATA_REN_i,
			-- Tx interface
--			CHNL_TX_CLK        => CHNL0_TX_CLK_i, 
			CHNL_TX            => CHNL0_TX_i, 
			CHNL_TX_ACK        => CHNL0_TX_ACK_i, 
			CHNL_TX_LAST       => CHNL0_TX_LAST_i, 
			CHNL_TX_LEN        => CHNL0_TX_LEN_i, 
			CHNL_TX_OFF        => CHNL0_TX_OFF_i, 
			CHNL_TX_DATA       => CHNL0_TX_DATA_i, 
			CHNL_TX_DATA_VALID => CHNL0_TX_DATA_VALID_i,
			CHNL_TX_DATA_REN   => CHNL0_TX_DATA_REN_i,
			
			ConfigRegister     => ConfigRegister_i,
			ConfigRegisterIdx  => ConfigRegisterIdx_i,
			
			-- Network interface
			DataOut            => DataOut,
			Tx                 => Tx,
			AckTx              => AckTx,
		
			DataIn             => DataIn,
			Rx                 => Rx,
			AckRx              => AckRx);


	ConfigCtrl : entity work.PCIeConfigCtrl
		GENERIC MAP(
			C_PCI_DATA_WIDTH => C_PCI_DATA_WIDTH,
			FlitWidth        => FlitWidth,
			NBREG            => 16)
		PORT MAP(
			LED                => open, --(7 downto 4)
			
			CLK                => USER_CLK_i,
			RST                => Reset,
			-- Rx interface
--			CHNL_RX_CLK        => CHNL1_RX_CLK_i, 
			CHNL_RX            => CHNL1_RX_i, 
			CHNL_RX_ACK        => CHNL1_RX_ACK_i, 
			CHNL_RX_LAST       => CHNL1_RX_LAST_i,  
			CHNL_RX_LEN        => CHNL1_RX_LEN_i,  
			CHNL_RX_OFF        => CHNL1_RX_OFF_i, 
			CHNL_RX_DATA       => CHNL1_RX_DATA_i, 
			CHNL_RX_DATA_VALID => CHNL1_RX_DATA_VALID_i, 
			CHNL_RX_DATA_REN   => CHNL1_RX_DATA_REN_i,
			-- Tx interface
--			CHNL_TX_CLK        => CHNL1_TX_CLK_i, 
			CHNL_TX            => CHNL1_TX_i, 
			CHNL_TX_ACK        => CHNL1_TX_ACK_i, 
			CHNL_TX_LAST       => CHNL1_TX_LAST_i, 
			CHNL_TX_LEN        => CHNL1_TX_LEN_i,  
			CHNL_TX_OFF        => CHNL1_TX_OFF_i, 
			CHNL_TX_DATA       => CHNL1_TX_DATA_i, 
			CHNL_TX_DATA_VALID => CHNL1_TX_DATA_VALID_i,
			CHNL_TX_DATA_REN   => CHNL1_TX_DATA_REN_i,
			
			ConfigRegister     => ConfigRegister_i,
			ConfigRegisterIdx  => ConfigRegisterIdx_i);


end RTL;


























