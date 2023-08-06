module a_calcul_freq (
                     rst_n,
                     clk_ref,
                     r_di,
                     valeur_comp,
                     val_div,
                            
                     div_freq_rec,
                     flag_first
                     );


input rst_n, clk_ref;
input r_di;
input[7:0] valeur_comp;
input[3:0] val_div;
output flag_first;
output[11:0] div_freq_rec;

wire rst_n, clk_ref;
wire[7:0] valeur_comp;
wire[3:0] val_div;
wire r_di;

reg[3:0] r_cpt_div_freq;
reg[11:0] div_freq_rec;
reg flag_first, flag_enable;
reg memo_flag_en;


    
always @(posedge clk_ref or negedge rst_n)
if(!rst_n)
    begin
        r_cpt_div_freq <= 4'b0;
        div_freq_rec   <= 12'd0;
        flag_first     <= 1'b0;
        memo_flag_en   <= 1'b0;
        flag_enable    <= 1'b1;
    end
else if((r_cpt_div_freq == val_div) && (!flag_first))
    begin
        r_cpt_div_freq <= 4'b0;
        div_freq_rec   <= div_freq_rec + 1'b1;
        flag_first     <= 1'b0;
        memo_flag_en   <= 1'b1;
        flag_enable    <= r_di;
    end
else if(!flag_enable)
    begin
        r_cpt_div_freq <= r_cpt_div_freq + 1'b1;
        div_freq_rec   <= div_freq_rec;
        flag_first     <= flag_first;
        memo_flag_en   <= 1'b1;
        flag_enable    <= r_di;
    end
else if(flag_enable && memo_flag_en)
    begin
        r_cpt_div_freq <= r_cpt_div_freq;
        div_freq_rec   <= div_freq_rec;
        flag_first     <= 1'b1;
        memo_flag_en   <= 1'b1;
        flag_enable    <= 1'b1;
    end
else
    begin
        r_cpt_div_freq <= r_cpt_div_freq;
        div_freq_rec   <= div_freq_rec;
        flag_first     <= flag_first;
        memo_flag_en   <= flag_first ? 1'b1 : 1'b0;
        flag_enable    <= r_di;
    end

endmodule
