library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_arith.all;
use IEEE.std_logic_unsigned.all;

------------------------------------------------------------------------------
-- ENTITY
------------------------------------------------------------------------------
entity fifo_out_diff is 
  generic ( inbitt: natural; outbitt: natural; mode: natural; nb_mot: natural);   --mode=0 decodage/1 codage                                  
  port (
    rst         : in  std_logic :='0'; --reset globale 0 off/1 on
    
    clk_in      : in  std_logic;  -- l'horloge d'écriture
    clk_out     : in  std_logic;  -- l'horloge de lecture
    
    wr          : in  std_logic;  -- control by AU
    r           : in  std_logic;
    empty       : out std_logic;  -- etat of FIFOs(or VC)
    full        : out std_logic;  -- etat of FIFOs(or VC)
    
    data_en     : in  std_logic_vector (inbitt-1 downto 0);
    data_sort   : out std_logic_vector (outbitt-1 downto 0);
    led         : out std_logic_vector (7 downto 0)					
    );
end fifo_out_diff;

-------------------------------------------------------------------------------
-- ARCHITECTURE
-------------------------------------------------------------------------------
architecture archi_fifo_out of fifo_out_diff is
  
  constant taille_fifo: integer := inbitt; --,outbitt);
  constant nb_flit: natural := nb_mot; --:= nb_data(conv_integer(data_in(inbitt-5 downto inbitt-6)));
  
  constant chfifo: integer :=nb_mot; -- :=nombremot(inbitt,outbitt); -- inbitt >= outbitt
  constant chfifo_o: integer :=nb_mot; --:=nombremot(outbitt,inbitt); --inbitt <= outbitt
  constant depth: integer := nb_mot;--calculnb_mot(nb_flit,chfifo_o); --prodondeur de fifo
  
  type memory_vc is array (integer range 0 to depth-1) of std_logic_vector (taille_fifo downto 0);
  
  signal mem : memory_vc := (others => (others=>'0'));
  
  signal pointer_w : integer range 0 to depth-1;--pointeur de lecture
  signal pointer_r : integer range 0 to depth-1;--pointeur de lecture
  signal ff,ffp,fuly,w: std_logic;
  signal emy: std_logic :='1';
  signal ee, eep : std_logic :='1';
  
--		type entete is array (natural range <>) of std_logic_vector (outbitt downto 0); 
--		signal header: entete (0 to chfifo-1):=(others=> (others=>'0'));		
  
  signal nbmot: natural:=1;
  
--		type typedatain is (headerin,datain);
--		type typedataout is (headerout,dataout);
--		signal etat_in: typedatain;
--		signal etat_out: typedataout;
  
  signal data_in  : std_logic_vector (inbitt downto 0);
  signal data_out : std_logic_vector (outbitt downto 0);
  
  --type modeNA is (codage,decodage);
  --signal typeNA : modeNA;
  
  
begin
     
     led(6 downto 0) <= mem(0)(6 downto 0);
       led(7) <= emy;
     
     data_in <= '0' & data_en;
     data_sort <= data_out (outbitt-1 downto 0);-- when emy='0' else (others=>'X');
     
     empty <= emy;
     emy <= '1' when pointer_r = pointer_w and ee ='1'
            else '0';
     full <= fuly;
     fuly <= '1' when (ff='1' and pointer_w=pointer_r and emy='0') 
             else '0';
     
     w <= '1' when fuly='1' else wr;
     
     --etat_in <= headerin when data_in(inbitt)='1' else datain;
     
--			 etat_in <= datain;
     
     
     ecriture:   process (clk_in,rst)
       variable nbmot_in : natural;
       variable cmpflit  : natural;
     begin
       if (rst ='0') then
         pointer_w <= 0; 
         ff<='0';
         nbmot_in := chfifo_o;
         cmpflit  := 1;
         
--					 bit1: for j in 0 to chfifo-1 loop
--					       header(j)(outbitt) <= '1';						   
--					 end loop bit1;
         
       elsif (clk_in'event and clk_in='1') then
         ffp <=ff;
         
         if mode=1 then -- process codage
----					     if etat_in = headerin then	
--                             if w = '0' then 					 
--					             if inbitt > outbitt then
--					                 datainheader: for i in 0 to (chfifo-1) loop
--											     header(i)(outbitt-1 downto 0) <= data_in ((outbitt*(chfifo-i)-1) downto outbitt*(chfifo-i-1));
--											     end loop datainheader;
--							         ff <= '1';
--							     elsif inbitt = outbitt then
--						         header(chfifo-1) <= data_in;
--							     else header(chfifo-1)(outbitt-1 downto (outbitt-outbitt/chfifo_o)) <= data_in(inbitt-1 downto 0);
--								 header(chfifo-1)((outbitt-outbitt/chfifo_o)-1 downto 0) <= (others=>'0');
--							     end if;
--						     end if;
           
--					     els
           if w = '0' then
             if inbitt >= outbitt then
               mem(pointer_w) <= data_in;
               ff<='1'; 
               if pointer_w >= depth-1 then
                 pointer_w <= 0;
               else 
                 pointer_w <= pointer_w + 1;
               end if;
             else 
               mem(pointer_w)(inbitt*nbmot_in-1 downto inbitt*(nbmot_in-1)) <= data_in(inbitt-1 downto 0);
               
               if cmpflit >= nb_flit then
                 nbmot_in := chfifo_o;
                 cmpflit := 1;
                 pointer_w <= 0;   
                 ff<='1';
                 
               else cmpflit := cmpflit + 1;
                    if nbmot_in <= 1 then
                      nbmot_in := chfifo_o;
                      
                      if pointer_w >= depth-1 then
                        pointer_w <= 0; 
                      else pointer_w <= pointer_w+1; 
                           ff<='1';
                      end if;
                      
                    else 
                      nbmot_in := nbmot_in -1;
                    end if;
               end if;
             end if;
           elsif (ffp='1' and ee='1') then  					
             ff<='0';   	           
           end if;
           
--					 elsif etat_in = headerin then	
--					     nbmot_in := nb_flit;
--						 pointer_w <= 0;
--				         else mem(pointer_w)(inbitt*nbmot_in-1 downto inbitt*(nbmot_in-1)) <= data_in(inbitt-1 downto 0);
--						     if nbmot_in <= 1 then
--							 nbmot_in := nb_flit;
--							 ff<='1';
--							 else nbmot_in := nbmot_in - 1;							 
--							 end if;
         end if;
       end if;    
     end process;			
     
     data_out <= mem(pointer_r);
     
--		 data_out <= mem(pointer_r-1) when pointer_r >=1
--		             else mem(depth-1); -- when emy='0' else data_out;
     --header(nbmot-1) when etat_out = headerout else
     --(outbitt*(chfifo-nbmot + 1)-1 downto outbitt*(chfifo-nbmot));
     
     lecture:  process (clk_out,rst)
     begin   
       if (rst ='0') then
         pointer_r <= 0 ; 
         nbmot <= 1;
         ee<='1';
--			 etat_out <= dataout;
         
       elsif (clk_out'event and clk_out='1') then
         eep <= ee; 
         if mode=1 then -- process codage
           if r ='0' and emy='0' then 
             ee<='1';
             
             
--				     case etat_out is 
--					 when headerout =>   if inbitt <= outbitt then
--										 nbmot <= 1;
--										 etat_out <= dataout;
--										 else nbmot <= nbmot+1;
--											 if nbmot >= chfifo then
--											 nbmot <= 1;
--											 etat_out <= dataout;
--											 end if; 
--										 end if;	
             
             if inbitt <= outbitt then
               nbmot <= chfifo;
               if pointer_r >= depth-1 then
                 pointer_r <= 0;
--									etat_out <=dataout;
               else pointer_r <= pointer_r + 1;
                    if pointer_r=pointer_w and ffp='0' then
                      if pointer_r = 0 then
                        pointer_r <= depth-1;
                      else 
                        pointer_r <= pointer_r-1;
                      end if;
                    end if;
               end if;
               
             else nbmot <= nbmot +1; 
                  if nbmot >= chfifo then
                    nbmot <= 1;
                    
                    if pointer_r >= depth-1 then
                      pointer_r <= 0;
--										etat_out <=dataout;
                    else pointer_r <= pointer_r + 1;
                         if pointer_r=pointer_w and ffp='0' then
                           if pointer_r = 0 then
                             pointer_r <= depth-1;
                           else 
                             pointer_r <= pointer_r-1;
                           end if;
                         end if;
                    end if;
                    
                  end if;
             end if;
--					 end case;
           elsif (eep='1' and ff='1') then 
             ee<='0'; 
           end if;
         else 
           pointer_r <= 0;
--			 etat_out <= dataout;
         end if;
       end if;
     end process;
     
end archi_fifo_out;            
