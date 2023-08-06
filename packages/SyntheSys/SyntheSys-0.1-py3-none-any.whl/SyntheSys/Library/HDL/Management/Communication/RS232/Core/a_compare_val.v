module a_compare_val (
                     rst_n,
                     clk_ref,
                     enable,
                     comp_val,

                     data_valid,
                     data,
                            
                     flag,
                     error
                     );


input rst_n, clk_ref;
input enable;
input[17:0] comp_val;
input[17:0] data;
input data_valid; //output data_valid;
output error;
output flag;

wire rst_n, clk_ref;
wire enable;
wire[17:0] comp_val;
wire[17:0] data;
wire data_valid; //+++++++++Linlin 0210
reg flag, error;

wire compare;
reg[17:0] capt_data;
reg memo_dv;

assign compare = (capt_data == comp_val);

always @(posedge clk_ref or negedge rst_n)
if(!rst_n)
    begin
        flag      <= 1'b0;
        error     <= 1'b0;
        capt_data <= 'b0;
        memo_dv   <= 1'b0;
    end
else if(data_valid & enable & !flag & !error)
    begin
        flag      <= 1'b0;
        error     <= 1'b0;
        capt_data <= data;
        memo_dv   <= 1'b1;
    end
else if(memo_dv)
    begin
        flag      <= enable & compare;
        error     <= enable & !compare;
        capt_data <= capt_data;
        memo_dv   <= 1'b1;
    end
else
    begin
        flag      <= flag;
        error     <= error;
        capt_data <= capt_data;
        memo_dv   <= memo_dv;
    end
endmodule

