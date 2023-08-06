//##  DEMUS POUR STIMULI
//#                  __     
//#                 /  |   
//#                /   |   
//#               |    |    
//#stimu_i --/--> |    | --/--> r_o  (Vers In DUT)
//#        64     |    |  128 
//#               |    |     
//#                \   | 
//#                 \__| 
//#                  /\
//#                  ||
//#                   3
//                   ||
//#//            -------------
//     rst_n -->| Decode      |----> r_incr_o (Vers Ctrl_Stimuli --> in dmx_sgnl_i)
//#  clk_ref -->| r_cpt_demux |
//#              -------------
//#

module a_dmx_stim_64x64  (
                         rst_n,
                         clk_ref,
                         run_i,
                         stimu_i,
                         start_verif_i,
                         egal_clk_ref_i,
//### Signaux Optimisation
                         stop_i,
                         r_dv_o,

//### Signaux Out vers DUT et Ctrl_Stimu
                         r_incr_o,
                         r_o
                         );

input rst_n, clk_ref, run_i;
input[63:0] stimu_i;
input stop_i;
input start_verif_i;
input egal_clk_ref_i;

output r_incr_o;
output[63:0]  r_o;
output r_dv_o;

wire rst_n, clk_ref, run_i;
wire[63:0] stimu_i;
wire start_verif_i;
wire stop_i;
wire egal_clk_ref_i;

reg[63:0]  r_o;
reg  r_incr_o;
reg r_dv_o;

//###################### DECLARATION SIGNAUX INTERNE ################
reg[2:0] r_cpt_demus;
reg r_start_capture;
//##### DEMUX ###############
wire declenche_verif;
wire declenche_verif_diff_un;

assign declenche_verif_diff_un = ((run_i || r_incr_o || r_start_capture) & !egal_clk_ref_i);
assign declenche_verif = (declenche_verif_diff_un  || (egal_clk_ref_i & start_verif_i)) & !stop_i; 

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
            begin 
                r_cpt_demus <= 3'b0;
                r_incr_o <= 1'b0;
            end
     else if(declenche_verif)
            begin 
                r_cpt_demus <= 3'b001;
                r_incr_o <= !r_incr_o || egal_clk_ref_i;
            end
       else if(stop_i)
            begin 
                r_cpt_demus <= r_cpt_demus;
                r_incr_o <= 1'b0; 
            end
       else
            begin 
                r_cpt_demus <= 3'b0;
                r_incr_o <= 1'b0;
            end

always @(posedge clk_ref or negedge rst_n)

		if(!rst_n)
			begin 
				r_start_capture <= 1'b0;
				r_o <= 'b0;
				r_dv_o <= 1'b0;
			end
		else
			begin
				case({stop_i,r_cpt_demus})
								4'b0001  : begin
												  r_start_capture <= 1'b0;
												  r_o <= stimu_i;
												  r_dv_o <= 1'b1;
												end
								default   : begin
												  r_start_capture <= 1'b0;
												  r_o <= r_o;
												  r_dv_o <= 1'b0;
												end

				endcase
			end
			
			
			
endmodule
