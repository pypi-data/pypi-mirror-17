library ieee;
use ieee.std_logic_1164.all;
--use ieee.std_logic_arith.all;
--use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
library std;
use std.textio.all;
library work;
use work.constant_definition.all;

--synthesis translate_off
--library ieee_proposed;
--use ieee_proposed.float_pkg.all;
--use work.float_tools.all;
--synthesis translate_on

entity BOPM_computation_unit_8_47 is

	-- computation block at step t, position k
	-- Vt,k[call]= max{d * St+1,k - K ; rp * Vt+1,k + r(1-p) * Vt+1,k-1 }
	-- Vt,k[put] = max{K - d * St+1,k ; rp * Vt+1,k + r(1-p) * Vt+1,k-1 }

	-- WARNING : some internal operators (flopoco generated) do not actually
	-- reset to a known state. The output of BOPM_computation_unit_8_47 is thus stable and
	-- meaningful only after [PIPELINE_LENGTH] clock cycles.
	PORT(
		--control signals
		CLK               : in  std_logic                    ;
		RST               : in  std_logic                    ;
		Enable            : in  std_logic                    ;
		Cmd               : in  std_logic                    ;
		--parameters (precomputed, option dependent)
		d_stim            : in  std_logic_vector(55 downto 0);
		K_min_stim        : in  std_logic_vector(55 downto 0);
		rp_stim           : in  std_logic_vector(55 downto 0);
		rp_min_stim       : in  std_logic_vector(55 downto 0);
		--tree values (k and k-1 values from t+1)
		S_k_stim          : in  std_logic_vector(55 downto 0);
		V_k_call_stim     : in  std_logic_vector(55 downto 0);
		V_k_min_call_stim : in  std_logic_vector(55 downto 0);
		V_k_put_stim      : in  std_logic_vector(55 downto 0);
		V_k_min_put_stim  : in  std_logic_vector(55 downto 0);
		--outputs
		S_k_trace         : out std_logic_vector(55 downto 0);
		V_k_call_trace    : out std_logic_vector(55 downto 0);
		V_k_put_trace     : out std_logic_vector(55 downto 0);
		-- valid_out         : out std_logic -- output is valid at the next clock cycle (1 cycle delay)

		Nc                : out std_logic                      -- Signal non utilise
		);

end BOPM_computation_unit_8_47;

architecture rtl of BOPM_computation_unit_8_47 is

	-----------------------------------------------------------------------------
	component FPCompare_OL
		port (
				  a      : in  std_logic_vector(31 downto 0);
				  b      : in  std_logic_vector(31 downto 0);
				  clk    : in  std_logic;
				  ce     : in  std_logic;
				  result : out std_logic);
	end component;

	component FPAdderDualPath_8_47_8_47_8_47400 
		port (
		clk : in  std_logic;
                Enable : in  std_logic;
-- OL           rst : in  std_logic;
		X        : in  std_logic_vector(8+47+2 downto 0);
		Y        : in  std_logic_vector(8+47+2 downto 0);
		R        : out std_logic_vector(8+47+2 downto 0);
                Nc       : out std_logic);
	end component;

	component FPMultiplier_8_47_8_47_8_47_uid2 
		port (
		ClkRef : in  std_logic;
                Enable : in  std_logic;
-- OL           rst : in  std_logic;
		X        : in  std_logic_vector(8+47+2 downto 0);
		Y        : in  std_logic_vector(8+47+2 downto 0);
		R        : out std_logic_vector(8+47+2 downto 0);
		Nc       : out std_logic
	);
	end component;
	-----------------------------------------------------------------------------
	--signals, flopoco format ("01"&Vector[FP, single precision])

-- OL	signal d_stim_f            : std_logic_vector(57 downto 0);
   signal d_stim_f            : std_logic_vector(55 downto 0);
	signal K_min_stim_f        : std_logic_vector(55 downto 0);
	signal rp_stim_f           : std_logic_vector(55 downto 0);
	signal rp_min_stim_f       : std_logic_vector(55 downto 0);
	signal S_k_stim_f          : std_logic_vector(55 downto 0);
	signal V_k_call_stim_f     : std_logic_vector(55 downto 0);
	signal V_k_min_call_stim_f : std_logic_vector(55 downto 0);
	signal V_k_put_stim_f      : std_logic_vector(55 downto 0);
	signal V_k_min_put_stim_f  : std_logic_vector(55 downto 0);

signal Nw_S_k_stim_f          : std_logic_vector(57 downto 0);
signal Nw_d_stim_f            : std_logic_vector(57 downto 0);
signal Nw_rp_stim_f           : std_logic_vector(57 downto 0);
signal Nw_V_k_call_stim_f     : std_logic_vector(57 downto 0);
signal Nw_rp_min_stim_f       : std_logic_vector(57 downto 0);
signal Nw_V_k_min_call_stim_f : std_logic_vector(57 downto 0);
signal Nw_V_k_put_stim_f      : std_logic_vector(57 downto 0); 
signal Nw_V_k_min_put_stim_f  : std_logic_vector(57 downto 0);
signal Nw_K_min_stim_f        : std_logic_vector(57 downto 0);

	signal S_k_temp        : std_logic_vector(57 downto 0);
	signal rp_V_k_call     : std_logic_vector(57 downto 0);
	signal rp_V_k_min_call : std_logic_vector(57 downto 0);
	signal rp_V_k_put      : std_logic_vector(57 downto 0);
	signal rp_V_k_min_put  : std_logic_vector(57 downto 0);
	signal S_k_delayed     : array_S_k;
	signal K_delayed       : array_K;

	-- FIX for "00" (zeroes out of multipliers)
	signal rp_V_k_call_fix     : std_logic_vector(57 downto 0);
	signal rp_V_k_min_call_fix : std_logic_vector(57 downto 0);
	signal rp_V_k_put_fix      : std_logic_vector(57 downto 0);
	signal rp_V_k_min_put_fix  : std_logic_vector(57 downto 0);
	-- END FIX

	signal exercise_value_call   : std_logic_vector(57 downto 0);
	signal exercise_value_put    : std_logic_vector(57 downto 0);
        signal exercise_value        : std_logic_vector(57 downto 0);
	signal binomial_value        : std_logic_vector(57 downto 0);
	signal binomial_value_call   : std_logic_vector(57 downto 0);
--	signal binomial_value_put    : std_logic_vector(57 downto 0);
	--delayed by ONE clock period : 
	signal exercise_value_call_d : std_logic_vector(57 downto 0);
--	signal exercise_value_put_d  : std_logic_vector(57 downto 0);
	signal binomial_value_call_d : std_logic_vector(57 downto 0);
--	signal binomial_value_put_d  : std_logic_vector(57 downto 0);

	signal exercise_value_call_d_d : std_logic_vector(57 downto 0);
--	signal exercise_value_put_d_d  : std_logic_vector(57 downto 0);
	signal binomial_value_call_d_d : std_logic_vector(57 downto 0);
--	signal binomial_value_put_d_d  : std_logic_vector(57 downto 0);

	signal valid_exercise_call : std_logic;
--	signal valid_exercise_put  : std_logic;
--	signal ce                  : std_logic := '1';
	--  signal counter             : std_logic_vector(4 downto 0);

	--synthesis translate_off
	--signal exercise_value_call_REAL : real;
	--signal binomial_value_call_REAL : real;
	--signal exercise_value_put_REAL  : real;
	--signal binomial_value_put_REAL  : real;
	--signal K_min_stim_f_REAL        : real;
	--signal S_k_temp_REAL            : real;
	--signal rp_V_k_put_REAL          : real;
	--signal rp_V_k_min_put_REAL      : real;
	--synthesis translate_on
	-- ### Declaration des signaux non connecte

-- OF
	signal Nc1, Nc2, Nc3, Nc4, Nc5      : std_logic;
        signal Nc10, Nc11, Nc12             : std_logic;
        signal NcA1, NcA2, NcA3, NcA4, NcA5 : std_logic;
 
        signal V_k_call_traceInt: std_logic_vector(55 downto 0) ;
        signal V_k_put_traceInt : std_logic_vector(55 downto 0) ;
        signal S_k_traceInt     : std_logic_vector(55 downto 0) ;

        signal K_min_stim_fInt     : std_logic_vector(55 downto 0) ;

        constant ZeroUn : STD_LOGIC_VECTOR(1 downto 0) := "01" ;
-------------------------------------------------------------------------------
begin  -- a_BOPM_computation_unit_8_47

	-------------------------------------------------------------------------------
	-- FIRST STAGE : Multipliers
	-------------------------------------------------------------------------------
	NcA1 <= Nc1 and Nc2 and Nc3 and Nc4 and Nc5 and Nc10 and Nc11 and Nc12;
        NcA2 <= binomial_value_call_d(56) and binomial_value_call_d(57);
--        NcA3 <= binomial_value_put_d(56) and binomial_value_put_d(57);
        NcA4 <= exercise_value_call_d(56) and exercise_value_call_d(57); 
--        NcA5 <= exercise_value_put_d(56) and exercise_value_put_d(57);
        Nc   <= NcA1 and NcA2 and NcA3 and NcA4 and NcA5;

Nw_S_k_stim_f          <= ZeroUn&S_k_stim_f         ;
Nw_d_stim_f            <= ZeroUn&d_stim_f           ;
Nw_rp_stim_f           <= ZeroUn&rp_stim_f          ;
Nw_V_k_call_stim_f     <= ZeroUn&V_k_call_stim_f    ;
Nw_rp_min_stim_f       <= ZeroUn&rp_min_stim_f      ;
Nw_V_k_min_call_stim_f <= ZeroUn&V_k_min_call_stim_f;
Nw_V_k_put_stim_f      <= ZeroUn&V_k_put_stim_f     ;
Nw_V_k_min_put_stim_f  <= ZeroUn&V_k_min_put_stim_f ;

	FPMultiplier_8_47_1 : FPMultiplier_8_47_8_47_8_47_uid2
	port map (
					ClkRef => CLK,
                                        Enable => Enable,
-- OL					rst => RST,
					X   => Nw_S_k_stim_f,
					Y   => Nw_d_stim_f,
					R   => S_k_temp,
					Nc  => Nc1);
--					R   => S_k_temp);

	FPMultiplier_8_47_2 : FPMultiplier_8_47_8_47_8_47_uid2
	port map (
					ClkRef => CLK,
                                        Enable => Enable,
-- OL					rst => RST,
					X   => Nw_rp_stim_f,
					Y   => Nw_V_k_call_stim_f,
					R   => rp_V_k_call,
					Nc  => Nc2);
--					R   => rp_V_k_call);

	FPMultiplier_8_47_3 : FPMultiplier_8_47_8_47_8_47_uid2
	port map (
					ClkRef => CLK,
                                        Enable => Enable,
-- OL 					rst => RST,
					X   => Nw_rp_min_stim_f,
					Y   => Nw_V_k_min_call_stim_f,
					R   => rp_V_k_min_call,
					Nc  => Nc3);
--					R   => rp_V_k_min_call);

--	FPMultiplier_8_47_4 : FPMultiplier_8_47_8_47_8_47_uid2    -- OF VOIR A SUPP
--	port map (
--					ClkRef => CLK,
--                                        Enable => Enable,
---- OL					rst => RST,
--					X   => Nw_rp_stim_f,
--					Y   => Nw_V_k_put_stim_f,
--					R   => rp_V_k_put,
--					Nc  => Nc4);
----					R   => rp_V_k_put);

--	FPMultiplier_8_47_5 : FPMultiplier_8_47_8_47_8_47_uid2    -- OF VOIR A SUPP
--	port map (
--					ClkRef => CLK,
--                                        Enable => Enable,
---- OL					rst => RST,
--					X   => Nw_rp_min_stim_f,
--					Y   => Nw_V_k_min_put_stim_f,
--					R   => rp_V_k_min_put,
--					Nc  => Nc5);
----					R   => rp_V_k_min_put);

	-- purpose: set the output from the multipliers stage right even if they have zeores as input(s)
	-- outouts: Inputs to adder stage

	rp_V_k_min_put_fix <= ZeroUn&"00000000000000000000000000000000000000000000000000000000" when
								 (rp_V_k_min_put(57 downto 56) = "00") else rp_V_k_min_put;

	rp_V_k_put_fix <=     ZeroUn&"00000000000000000000000000000000000000000000000000000000" when (rp_V_k_put(57
								 downto 56) = "00") else rp_V_k_put;

	rp_V_k_min_call_fix <= ZeroUn&"00000000000000000000000000000000000000000000000000000000" when
								  (rp_V_k_min_call(57 downto 56) = "00") else rp_V_k_min_call;

	rp_V_k_call_fix <=     ZeroUn&"00000000000000000000000000000000000000000000000000000000" when (rp_V_k_call(57
								  downto 56) = "00") else rp_V_k_call;

	-------------------------------------------------------------------------------
	-- SECOND STAGE : Adders/Substracters
	-------------------------------------------------------------------------------

Nw_K_min_stim_f <= ZeroUn&K_min_stim_f ;

	FPAdderDualPath_8_47_1 : FPAdderDualPath_8_47_8_47_8_47400
	port map (
					clk => CLK,
                                        Enable => Enable,
-- OL					rst => RST,
					X   => S_k_temp,
					Y   => Nw_K_min_stim_f,
					R   => exercise_value_call,
                                        Nc  => Nc10
				);

	FPAdderDualPath_8_47_2 : FPAdderDualPath_8_47_8_47_8_47400
	port map (
					clk => CLK,
                                        Enable => Enable,
-- OL					rst => RST,
					X   => rp_V_k_call_fix,
					Y   => rp_V_k_min_call_fix,
--					R   => binomial_value_call,
					R   => binomial_value,
                                        Nc  => Nc11);

--	FPAdderDualPath_8_47_3 : FPAdderDualPath_8_47_8_47_8_47400 -- OF VOIR A SUPP
--	port map (
--					clk => CLK,
--                                        Enable => Enable,
---- OL					rst => RST,
--					X   => rp_V_k_put_fix,
--					Y   => rp_V_k_min_put_fix,
--					R   => binomial_value_put,
--                                        Nc  => Nc12);


	exercise_value_put <= (exercise_value_call(57 downto 56) & not(exercise_value_call(55)) & exercise_value_call(54 downto 0));

exercise_value <= exercise_value_call when Cmd = '1' else exercise_value_put;

	-------------------------------------------------------------------------------
	-- THIRD STAGE : Comparators
	-------------------------------------------------------------------------------

	FPCompare_1 : FPCompare_OL
	port map (
--					a      => exercise_value_call(55 downto 24),
					a      => exercise_value(55 downto 24),
--					b      => binomial_value_call(55 downto 24),
					b      => binomial_value(55 downto 24),
					clk    => CLK,
					ce     => Enable,
					result => valid_exercise_call
				);

--	FPCompare_2 : FPCompare_OL
--	port map (
--					a      => exercise_value_put(55 downto 24),
--					b      => binomial_value_put(55 downto 24),
--					clk    => CLK,
--					ce     => Enable,
--					result => valid_exercise_put
--				);

	-- purpose: Set the inputs of the computation unit at "00...0" when RST is set to high
	-- type   : sequential
	-- inputs : CLK, RST, *_stim
	-- outputs: *stim__f
	reset_sig : process (CLK, RST) --,K_delayed)
	begin  -- process reset_sig
		if RST = '1' then                   -- asynchronous reset (active HIGH)
                  d_stim_f            <= (55 downto 0 => '0');
--                  K_min_stim_fInt        <= K_delayed(DELAY_K-1);
                  K_min_stim_fInt     <= (others => '0');
                  rp_stim_f           <= (55 downto 0 => '0');
                  rp_min_stim_f       <= (55 downto 0 => '0');
                  S_k_stim_f          <= (55 downto 0 => '0');
                  V_k_call_stim_f     <= (55 downto 0 => '0');
                  V_k_min_call_stim_f <= (55 downto 0 => '0');
                   V_k_put_stim_f      <= (55 downto 0 => '0');
                  V_k_min_put_stim_f  <= (55 downto 0 => '0');

		elsif CLK'event and CLK = '1' then  -- rising clock edge
                  if(Enable='1') then
														-- Flopoco signals update
-- OL			d_stim_f            <= ZeroUn&d_stim;
                        d_stim_f            <= d_stim(55 downto 0) ;
--OL 			K_min_stim_f        <= ZeroUn&K_delayed(DELAY_K-1);
                        K_min_stim_fInt        <= K_delayed(DELAY_K-1);
--OL			rp_stim_f           <= ZeroUn&rp_stim;
                        rp_stim_f           <= rp_stim(55 downto 0);
-- OL			rp_min_stim_f       <= ZeroUn&rp_min_stim;
                   rp_min_stim_f       <= rp_min_stim(55 downto 0);
-- OL			S_k_stim_f          <= ZeroUn&S_k_stim;
                  S_k_stim_f          <= S_k_stim(55 downto 0) ;
-- OL 			V_k_call_stim_f     <= ZeroUn&V_k_call_stim;
                  V_k_call_stim_f     <= V_k_call_stim(55 downto 0);
-- OL			V_k_min_call_stim_f <= ZeroUn&V_k_min_call_stim;
                   V_k_min_call_stim_f <= V_k_min_call_stim(55 downto 0);
-- OL			V_k_put_stim_f      <= ZeroUn&V_k_put_stim;
                  V_k_put_stim_f      <= V_k_put_stim(55 downto 0) ;
-- OL			V_k_min_put_stim_f  <= ZeroUn&V_k_min_put_stim;
                   V_k_min_put_stim_f  <= V_k_min_put_stim(55 downto 0) ;
                  end if;
		end if;
	end process reset_sig;

K_min_stim_f <= K_min_stim_fInt(55 downto 0);

	-- purpose: select the right value for V_k_call_trace depending on valid_exercise_call
	-- outouts: V_k_call_trace
	tracing_call : process (valid_exercise_call, exercise_value_call_d_d, binomial_value_call_d_d)
	begin  -- process tracing_call
		if valid_exercise_call = '1' then
			V_k_call_traceInt <= exercise_value_call_d_d(55 downto 0);
		else
			V_k_call_traceInt <= binomial_value_call_d_d(55 downto 0);
		end if;
	end process tracing_call;

	-- purpose: select the right value for V_k_put_trace depending on valid_exercise_put
	-- outouts: V_k_put_trace
--	tracing_put : process (valid_exercise_put, exercise_value_put_d_d, binomial_value_put_d_d)
--	begin  -- process tracing_put
--		if valid_exercise_put = '1' then
--			V_k_put_traceInt <= exercise_value_put_d_d(55 downto 0);
--		else
--			V_k_put_traceInt <= binomial_value_put_d_d(55 downto 0);
--		end if;
--	end process tracing_put;

	-- purpose: Delay S_k_trace by DELAY_S_K clock cycles
	-- type   : sequential
	-- inputs : CLK, RST, S_k_temp
	-- outputs: S_k_trace
	delay_S_k_proc : process (CLK, RST)
	begin  -- process delay_S_k_proc
		if CLK'event and CLK = '1' then     -- rising clock edge
                  if(Enable='1') then
			--RST clocked, only insert a full 00...0 in the pipeline
			S_k_delayed(0) <= S_k_temp(55 downto 0);
			S_k_traceInt      <= S_k_delayed(DELAY_S_K -1);
			for INDEX in 1 to DELAY_S_K -1 loop
				S_k_delayed(INDEX) <= S_k_delayed(INDEX -1);
			end loop;  -- INDEX
                  end if;
		end if;
	end process delay_S_k_proc;

	-- purpose: Delay K_stim by DELAY_K clock cycles (and *_d by one clock signal
	-- as a bonus)
	-- type   : sequential
	-- inputs : CLK, RST, K_min_stim
	-- outputs: K_delayed
	delay_K_proc : process (CLK, RST)
	begin  -- process delay_K_proc
              if RST = '1' then                 -- synchronous reset (active HIGH)
				K_delayed(0) <= (others => '0');
				for INDEX in 1 to DELAY_K -1 loop
--				K_delayed(INDEX) <= K_delayed(INDEX -1);
				K_delayed(INDEX) <= (others => '0');
				end loop;  -- INDEX
		elsif CLK'event and CLK = '1' then     -- rising clock edge
--if(RST = '1') then
--				K_delayed(0) <= (others => '0');
--				for INDEX in 1 to DELAY_K -1 loop
--					K_delayed(INDEX) <= K_delayed(INDEX -1);
--				end loop;  -- INDEX

                 if(Enable='1') then 
				K_delayed(0) <= K_min_stim;

				for INDEX in 1 to DELAY_K -1 loop
					K_delayed(INDEX) <= K_delayed(INDEX-1);
				end loop;  -- INDEX

--			exercise_value_call_d <= exercise_value_call;
			exercise_value_call_d <= exercise_value;
--			exercise_value_put_d  <= exercise_value_put;
--			binomial_value_call_d <= binomial_value_call;
			binomial_value_call_d <= binomial_value;
--			binomial_value_put_d  <= binomial_value_put;

			exercise_value_call_d_d <= exercise_value_call_d;
--			exercise_value_put_d_d  <= exercise_value_put_d;
			binomial_value_call_d_d <= binomial_value_call_d;
--			binomial_value_put_d_d  <= binomial_value_put_d;
                
                 end if;
	end if;
	end process delay_K_proc;

S_k_trace      <= S_k_traceInt     (55 downto 0)          ;-- & "000000000000000000000000";
--V_k_put_trace  <= V_k_put_traceInt (55 downto 0)   ;-- & "000000000000000000000000";
V_k_put_trace  <= V_k_call_traceInt(55 downto 0) ;
V_k_call_trace <= V_k_call_traceInt(55 downto 0) ;-- & "000000000000000000000000";

end rtl;
