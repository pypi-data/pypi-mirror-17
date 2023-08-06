//Description : Le module "set_verification" a pour fonction de stocker le nombre de cycle de vérification et de générer un signal de contrôle
//				maintenu à un niveau logique 1 pendant toute la phase de vérification. Il configure ainsi tous les modules concernés en mode 
//				"verification" du DUT avant le lancement officiel par l'instruction "start_verification".



//###### SET_VERIFICATION #########

module a_set_verification(
                       rst_n,
                       clk_ref,
                       clk_user,
                       r_w_i,
                       busy_i,
                       select_module_i,
                       dv_i,
                       data_i,
                       egal_clk_ref_i,
                       deux_clk_ref_i,

                       r_data_nbr_cyc_o,
                       r_dv_nbr_cyc_o,
                       run_verif_o
                       );



input rst_n, clk_ref, clk_user;
input r_w_i;
input select_module_i;
input busy_i;
input dv_i;
input[15:0] data_i;
input egal_clk_ref_i;
input deux_clk_ref_i;

output[15:0] r_data_nbr_cyc_o;
output r_dv_nbr_cyc_o;
output run_verif_o;

wire rst_n, clk_ref, clk_user;
wire r_w_i;
wire select_module_i;
wire busy_i;
wire dv_i;
wire[15:0] data_i;
wire egal_clk_ref_i;
wire deux_clk_ref_i;

reg[15:0] r_data_nbr_cyc_o;
reg r_dv_nbr_cyc_o;
reg run_verif_o;

//#### DECLARATION DES SIGNAUX INTERNE ###########
reg r_start;
reg[31:0] r_data_load;
reg[1:0] r_cpt_step;
reg[31:0] r_compteur_step;
wire stop_verif;
wire[15:0] data_i_un;
wire[15:0] data_i_deux;

assign data_i_un = data_i + 2'b10;
assign data_i_deux = data_i + 1'b1;

assign stop_verif = (r_compteur_step == r_data_load);

always @(posedge clk_ref or negedge rst_n)
   if(!rst_n)
       begin
           r_data_load <= 32'b0;
           r_start <= 1'b0;
           r_cpt_step <= 2'b0;
           r_compteur_step <= 32'b0;
           run_verif_o <= 1'b0;
           r_dv_nbr_cyc_o <= 1'b0;
           r_data_nbr_cyc_o <= 16'h0;
       end
   else if(select_module_i && !r_start && r_w_i)
       begin
           r_data_load <= r_data_load; //Chgmnt
           r_start <= 1'b1;
           r_cpt_step <= 2'b0;
           r_compteur_step <= 32'b0;
           run_verif_o <= 1'b0;
           r_dv_nbr_cyc_o <= 1'b0;
           r_data_nbr_cyc_o <= r_data_load[15:0];
       end
   else if(r_start && clk_user)
       begin
           r_data_load <= r_data_load;
           r_start <= stop_verif ? 1'b0 : 1'b1;
           r_cpt_step <= stop_verif ? 2'b0 : r_cpt_step;
           r_compteur_step <= stop_verif ? 32'b0 : (r_compteur_step + 1'b1);
           run_verif_o <= stop_verif ? 1'b0 : 1'b1;
           r_dv_nbr_cyc_o <= 1'b0;
           r_data_nbr_cyc_o <= r_data_load[15:0];
       end
// ECRITURE DU NBR DE CYCLE QUE L'ON VEUX
   else if(select_module_i && r_start && dv_i && r_w_i)
       begin
        case({deux_clk_ref_i,egal_clk_ref_i})
           2'b01 : r_data_load <= (r_cpt_step == 2'b00) ? {r_data_load[31:16],data_i_un} : {data_i,r_data_load[15:0]};
           2'b10 : r_data_load <= (r_cpt_step == 2'b00) ? {r_data_load[31:16],data_i_deux} : {data_i,r_data_load[15:0]};
           default : r_data_load <= (r_cpt_step == 2'b00) ? {r_data_load[31:16],data_i} : {data_i,r_data_load[15:0]};
        endcase
           r_start <= 1'b1;
           r_cpt_step <= (r_cpt_step==2'b01) ? 2'b0 : r_cpt_step + 1'b1;
           r_compteur_step <= 32'b0;
           run_verif_o <= 1'b1;
           r_dv_nbr_cyc_o <= 1'b0;
           r_data_nbr_cyc_o <= r_data_load[15:0];
       end
// RE-LECTURE DU NBR DE CYCLE PROGRAMME
   else if(select_module_i && !r_w_i && !busy_i && !r_dv_nbr_cyc_o)
       begin
           r_data_load <= r_data_load;
           r_start <= r_start;
           r_cpt_step <= r_cpt_step;
           r_compteur_step <= r_compteur_step;
           run_verif_o <= run_verif_o;
           r_dv_nbr_cyc_o <= 1'b1;
           r_data_nbr_cyc_o <= r_data_nbr_cyc_o;
       end
   else if(select_module_i && !r_w_i && r_dv_nbr_cyc_o)
       begin
           r_data_load <= r_data_load;
           r_start <= r_start;
           r_cpt_step <= r_cpt_step;
           r_compteur_step <= r_compteur_step;
           run_verif_o <= run_verif_o;
           r_dv_nbr_cyc_o <= 1'b0;
           r_data_nbr_cyc_o <= r_data_load[31:16];
       end
endmodule
