//Description : Le module "rst_block" a pour fonction d'initialiser tous les modules du système d'accélération de vérification.  


module a_rst_block (
                   clk_ref,
                   rst_n_i,

                   init_rst_n_o
                   );

input clk_ref, rst_n_i;
output init_rst_n_o;

wire clk_ref, rst_n_i;
reg init_rst_n_int, start_cell;
wire init_rst_n_o;

assign init_rst_n_o = init_rst_n_int & !rst_n_i;

always @(posedge clk_ref)
  if(init_rst_n_int && start_cell)
      begin 
         init_rst_n_int <= 1'b1;
         start_cell <= 1'b1;
      end
  else if(!init_rst_n_int)
      begin 
         start_cell <= 1'b1;
         init_rst_n_int <= 1'b1;
      end
  else
      begin 
         init_rst_n_int <= 1'b0;
         start_cell <= 1'b0;
      end

endmodule
