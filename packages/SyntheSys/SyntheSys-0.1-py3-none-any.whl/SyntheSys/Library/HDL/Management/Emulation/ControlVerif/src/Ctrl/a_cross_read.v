//Description : Le module "cross_read" a pour fonction de piloter le module de communication (cf. module RS232) afin d'envoyer des données par l'intermédiaire de 
//				la liaison série au poste de travail. Toute requête concernant l'envoi de données passe par ce module qui interroge l'interface RS232 de son état  
//				(libre ou occupé) et agit en conséquence : "attente" ou "transmission de la donnée".




module a_cross_read(
                 memoire_stimuli_i,
                 data_i_16data_i,
                 data_valid_i,
                
                 ctrl_trace_i,
                 data_trace_i,
                 dv_trace_i,

                 ctrl_clk_user_i,
                 data_clk_user_i,
                 dv_clk_user_i,
                 
                 ctrl_nbr_cycle_i,
                 data_nbr_cycle_i,
                 dv_nbr_cycle_i,

                 data_station_o,
                 data_v_station_o
                 );
                 
input memoire_stimuli_i, data_valid_i;
input[15:0] data_i_16data_i;
input ctrl_trace_i, dv_trace_i;
input[15:0] data_trace_i;
input ctrl_clk_user_i, dv_clk_user_i;
input[15:0] data_clk_user_i;
input ctrl_nbr_cycle_i, dv_nbr_cycle_i;
input[15:0] data_nbr_cycle_i;

output data_v_station_o;
output[15:0] data_station_o;

wire memoire_stimuli_i, data_valid_i;
wire[15:0] data_i_16data_i;
wire ctrl_trace_i, dv_trace_i;
wire[15:0] data_trace_i;
wire ctrl_clk_user_i, dv_clk_user_i;
wire[15:0] data_clk_user_i;
wire ctrl_nbr_cycle_i, dv_nbr_cycle_i;
wire[15:0] data_nbr_cycle_i;

reg data_v_station_o;
reg[15:0] data_station_o;


always @(memoire_stimuli_i or data_i_16data_i or data_valid_i or
         ctrl_trace_i or data_trace_i or dv_trace_i or
         ctrl_clk_user_i or data_clk_user_i or dv_clk_user_i or
         ctrl_nbr_cycle_i or data_nbr_cycle_i or dv_nbr_cycle_i
        )
     case({memoire_stimuli_i,ctrl_trace_i,ctrl_clk_user_i,ctrl_nbr_cycle_i})
             
             4'b1000 :  begin 
                         data_station_o <= data_i_16data_i;
                         data_v_station_o <= data_valid_i;
                       end

             4'b0100 :  begin 
                         data_station_o <= data_trace_i;
                         data_v_station_o <= dv_trace_i;
                       end
             4'b0010 :  begin 
                         data_station_o <= data_clk_user_i;
                         data_v_station_o <= dv_clk_user_i;
                       end
             4'b0001 :  begin 
                         data_station_o <= data_nbr_cycle_i;
                         data_v_station_o <= dv_nbr_cycle_i;
                       end
             default : begin 
                         data_station_o <= 16'b0;
                         data_v_station_o <= 1'b0;
                       end
      endcase
endmodule

