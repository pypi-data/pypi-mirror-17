
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
--USE ieee.std_logic_unsigned.ALL;

ENTITY fifo IS

GENERIC (
	largeur    : integer;
	profondeur : integer);

PORT(
	IsFull    : OUT std_logic;
	IsEmpty   : OUT std_logic;
	clock_in  : IN std_logic;
	clock_out : IN std_logic;
	reset     : IN std_logic;
	data_in   : IN std_logic_vector(largeur-1 DOWNTO 0);
	wr        : IN std_logic;
	rd        : IN std_logic;
	ack_rd    : OUT std_logic;
	ack_wr    : OUT std_logic;
	data_out  : OUT std_logic_vector(largeur-1 DOWNTO 0) := (others=>'0'));
END fifo;

ARCHITECTURE RTL OF fifo IS

	TYPE tableau IS ARRAY(profondeur-1 DOWNTO 0) OF std_logic_vector(largeur-1 DOWNTO 0);
	SUBTYPE int IS natural RANGE 0 TO profondeur;
	SIGNAL fif      : tableau := (others=> (others=>'0'));
	SIGNAL pt_write : int := 0;
	SIGNAL pt_read  : int := 0;
	SIGNAL empty    : std_logic;
	SIGNAL full     : std_logic;

BEGIN 

	IsFull  <= full;
	IsEmpty <= empty; 

	empty  <= '1' WHEN (pt_read = pt_write) ELSE '0';
	full   <= '1' WHEN (pt_read = pt_write+1) ELSE '1' WHEN (pt_write = profondeur-1 AND pt_read = 0) ELSE '0';
	ack_wr <= '1' WHEN (empty ='1') ELSE '0';
	ack_rd <= '1' WHEN (full ='1') ELSE '0';

	PROCESS(clock_in) 
	BEGIN
		IF RISING_EDGE(clock_in) THEN
			IF (reset='1') THEN
				pt_write <= 0;  
			ELSIF (full='0' AND wr='1') THEN
				fif(pt_write) <= data_in;
				pt_write      <= pt_write + 1;
				IF(pt_write = profondeur-1) THEN
					pt_write <= 0;
				END IF;
			END IF;
		END IF;
	END PROCESS;

	PROCESS(clock_out)
	BEGIN
		IF RISING_EDGE(clock_out) THEN
			IF (reset='1') THEN
				pt_read <= 0;
			ELSIF (rd='1' AND empty ='0') THEN
				data_out <= fif(pt_read);
				pt_read  <= pt_read+1;
				IF (pt_read = profondeur-1) THEN
					pt_read <= 0;
				END IF;
			END IF;
		END IF;
	END PROCESS;

END RTL;
