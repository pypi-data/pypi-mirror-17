`define LENGTH_RAM_TRACE 13                 
`define PROF_RAM_TRACE 8192
`define FULL_RAM_TRACE 13'b1_1111_1111_0111  // Max -10

//##  OPTIMISATION TRACE
//#
//#                  ---
//#                 | R |     ---
//#                 | E |    | C |
//#data_user_i[X]-->| G |----| O |                 
//#              |  | 1 |    | M |                 |
//#              |  |[X]|    | P |        --       |
//#              |   ---     | A |       |  \      |
//#              |           | R |-------|a  \_____| r_comp_capt_o
//#              |   ---     | A |    ---|n  /
//#              |  | R |    | T |   |   |d /
//#              |  | E |    | E |   |    --
//#              -->| G |----| U |   |
//#                 | 2 |    | R |   |
//#                 |[X]|     ---    |
//#                  ---             |
//#     capt_i ----------------------
//#  
//
//
module a_opti_trace_48v64 (
                           rst_n,
                           clk_ref,
                         
                           run_verif_i,
                           egal_un_i,
                           deux_clk_ref_i,
                           capt_i,
                           data_user_i,

                           r_comp_capt_o,
                           r_data_o
                           );

input rst_n, clk_ref, capt_i, run_verif_i;
input[47:0] data_user_i;
input egal_un_i, deux_clk_ref_i;

output r_comp_capt_o;
output[63:0] r_data_o;

wire rst_n, clk_ref, capt_i, run_verif_i;
wire[47:0] data_user_i;
wire egal_un_i, deux_clk_ref_i;

reg r_comp_capt_o;
reg[63:0] r_data_o;

//###################### DECLARATION SIGNAUX INTERNE ################
reg[47:0] r_comp_data;
reg[47:0] r_next_data;
reg[14:0] r_cpt_val;
wire same_sig;
reg[2:0] r_step;
reg r_demarre;
reg r_eq;

reg r_stop_trce;
wire[7:0] etape;
wire max_compteur;
wire calcul_int, calcul_int_bis;
reg first_data;
reg r_run_verif;
reg[4:0] r_capt_egal;
wire capt_int;

assign same_sig = (r_comp_data == r_next_data);
assign max_compteur = (r_cpt_val == 15'h3fff);

assign capt_int = egal_un_i ? r_capt_egal[2] : deux_clk_ref_i ? r_capt_egal[0] : capt_i;

assign calcul_int = capt_int && r_demarre && r_run_verif;
assign calcul_int_bis = capt_int && r_run_verif && first_data;

assign etape[0] = capt_int && !r_demarre && !first_data;

assign etape[1] = (r_step == 3'b000) && (calcul_int || calcul_int_bis);
assign etape[2] = (r_step == 3'b001) && calcul_int;
assign etape[3] = (r_step == 3'b010) && calcul_int;
assign etape[4] = (r_step == 3'b011) && calcul_int;

assign etape[5] = r_demarre && !r_run_verif;
assign etape[6] = !r_demarre && r_stop_trce && !r_run_verif;
assign etape[7] = !r_demarre && !r_run_verif && (r_step == 3'b001);

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
              begin 
                      r_run_verif <= 1'b0;
                      r_capt_egal <= 1'b0;
              end
   else    
              begin 
                      r_run_verif <= run_verif_i;
                      r_capt_egal <= {r_capt_egal[3:0],capt_i};
              end

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
              begin 
                      first_data <= 1'b1;
              end
   else if(first_data)
              begin 
                      first_data <= first_data;
              end
   else
              begin 
                      first_data <= r_demarre;
              end

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= 1'b0;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= 1'b0;
                      r_comp_data <= 48'b0;
                      r_next_data <= 48'b0;
                      r_step <= 3'b0;
                      r_cpt_val <= 15'b1;
                      r_data_o <= 64'b0;
              end
     else if(etape[0])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= 1'b1;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= 1'b0;
                      r_comp_data <= 48'b0;
                      r_next_data <= 48'b0;
                      r_step <= 3'b0;
                      r_cpt_val <= 15'b1;
                      r_data_o <= 64'b0;
              end
     else if(etape[1])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= 1'b1;
                      r_comp_capt_o <= 1'b1;
                      r_eq <= 1'b0;
                      r_comp_data <= 48'b0;
                      r_next_data <= 48'b0;
                      r_step <= 3'b001;
                      r_cpt_val <= 15'b1;
                      r_data_o <= {data_user_i,r_cpt_val,r_eq};
              end
     else if(etape[2])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= r_demarre;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= r_eq;
                      r_comp_data <= data_user_i;
                      r_next_data <= 48'b0;
                      r_step <= 3'b010;
                      r_cpt_val <= r_cpt_val;
                      r_data_o <= {r_comp_data,r_cpt_val,r_eq};
              end
       else if(etape[3])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= r_demarre;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= r_eq;
                      r_comp_data <= r_comp_data;
                      r_next_data <= data_user_i;
                      r_step <= 3'b011;
                      r_cpt_val <= r_cpt_val;
                      r_data_o <= {r_comp_data,r_cpt_val,r_eq};
              end
       else if(etape[4])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= r_demarre;
                      r_comp_capt_o <= !same_sig || max_compteur;
                      r_eq <= same_sig && !max_compteur;
                      r_comp_data <= (same_sig && !max_compteur) ? r_comp_data : r_next_data;
                      r_next_data <= data_user_i;
                      r_step <= 3'b011;
                      r_cpt_val <= (same_sig && !max_compteur) ? r_cpt_val + 1'b1 : 15'b1;
                      r_data_o <= {r_comp_data,r_cpt_val,r_eq};
              end
            else if(etape[5])
              begin 
                      r_stop_trce <= !r_comp_capt_o;
                      r_demarre <= r_comp_capt_o;
                      r_comp_capt_o <= !r_comp_capt_o;
                      r_eq <= r_comp_capt_o ? 1'b0 : r_eq;
                      r_comp_data <= r_comp_data;
                      r_next_data <= r_next_data;
                      r_step <= 3'b0;
                      r_cpt_val <= r_comp_capt_o ? 15'b1 : r_cpt_val;
                      r_data_o <= {r_comp_data,r_cpt_val,r_eq};
              end
            else if(etape[6])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= 1'b0;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= 1'b0;
                      r_comp_data <= 48'b0;
                      r_next_data <= 48'b0;
                      r_step <= 3'b001;
                      r_cpt_val <= 15'b1;
                      r_data_o <= {r_next_data,r_cpt_val,r_eq};
              end
               else if(etape[7])
              begin 
                      r_stop_trce <= 1'b0;
                      r_demarre <= 1'b0;
                      r_comp_capt_o <= 1'b1;
                      r_eq <= 1'b0;
                      r_comp_data <= 48'b0;
                      r_next_data <= 48'b0;
                      r_step <= 3'b0;
                      r_cpt_val <= 15'b1;
                      r_data_o <= {r_data_o[63:16],r_cpt_val,r_eq};
              end
            else 
              begin 
                      r_stop_trce <= r_stop_trce;
                      r_demarre <= r_demarre;
                      r_comp_capt_o <= 1'b0;
                      r_eq <= r_eq;
                      r_comp_data <= r_comp_data;
                      r_next_data <= r_next_data;
                      r_step <= r_step;
                      r_cpt_val <= r_cpt_val;
                      r_data_o <= r_data_o;
              end

              
endmodule
