//Description : Le module "RS232" a pour fonction de récuperer des données arrivant en série suivant le protocole de communication d'une liaison série asynchrone,
//				selon la norme RS232 et de transmettre reciproquement une données sur n bits à un poste de travail auquel est connecté le dit cable.




module a_RS232(
                   rst_n,
                   clk_ref, 
                   r_di, 
                   r_do,
                   
                   r_dv_o,
                   r_q,

                   data_i,
                   dv_i,
                   r_busy_o,

                   led_di_o,
                   led_sync_o
                   );

input rst_n, clk_ref;
input r_di;
 
output r_do;
output r_dv_o;
output[15:0] r_q;
output r_busy_o;

output led_sync_o, led_di_o;

input[15:0] data_i;
input dv_i;

wire rst_n, clk_ref;
wire r_di;

wire r_do;
wire r_dv_o;
wire[15:0] r_q;
wire r_busy_o;

wire[15:0] data_i;
wire dv_i;

wire led_sync_o, led_di_o;

// ############## DECLARATION DES SIGNAUX INTERNE #########
wire[15:0] data_send;
wire clk_rcpt, clk_send;
wire dv_demi;
wire[7:0] data_demi;
wire clk_rcpt_general;
wire error_p8, send_sync_o;
wire r_dv_int;
// ############# GENERATION DES HORLOGEs #####################
assign led_di_o = r_di;
assign r_dv_o = led_sync_o & r_dv_int;

a_clock_gen_rs232_prot8 u_clock_gen_rs232_prot8(
                                               .rst_n(rst_n),
                                               .clk_ref(clk_ref),
                                               .r_di(r_di),
                                               .dv_i(dv_i),
                                               
                                               .data_demi(data_demi),
                                               .dv_demi(dv_demi),
                                               .valeur_comp({8'd0,8'd83,8'd89,8'd83,8'd67,8'd65,8'd68,8'd65,8'd55}),
                                               .dv_data(r_dv_int),
                                               .data(r_q),
                                     
                                               .clk_rcpt(clk_rcpt),
                                               .clk_rcpt_general(clk_rcpt_general),
                                               .clk_send(clk_send),

                                               .error_p8(error_p8),
                                               .send_sync_o(send_sync_o),
                                               .sync_o(led_sync_o)
                                               );

// ############# RECEPTION DONNEE #####################
a_demux_serial_1v8 u_demux_serial_1v8_0(
                                       .rst_n((rst_n & !error_p8)), 
                                       .clk_ref(clk_ref), 
                                       .clk_rcpt(clk_rcpt), 
                                       .r_di(r_di), 
                        
                                       .r_dv_o(dv_demi), 
                                       .r_q(data_demi)
                                       );
                                       
a_demux_serial_1v16 u_demux_serial_1v16_0(
                                       .rst_n((rst_n & !error_p8)), 
                                       .clk_ref(clk_ref), 
                                       .clk_rcpt(clk_rcpt_general), 
                                       .r_di(r_di), 
                        
                                       .r_dv_o(r_dv_int), 
                                       .r_q(r_q)
                                       );

// ############# EMISSION ############################
assign data_send = send_sync_o ? 16'haaaa : data_i;

a_mux_serial_16v1 u_mux_serial_16v1_0(
                                   .rst_n((rst_n & !error_p8)), 
                                   .clk_ref(clk_ref), 
                                   .clk_send(clk_send), 
                                   .data_i(data_send), 
                                   .dv_i(dv_i | send_sync_o),
                        
                                   .r_do_o(r_do), 
                                   .r_busy_o(r_busy_o)
                                   );
endmodule
