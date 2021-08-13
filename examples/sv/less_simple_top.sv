// This file is public domain, it can be freely copied without restrictions.
// SPDX-License-Identifier: CC0-1.0

`timescale 1us/1us

typedef struct packed {
  logic [17-1:0] instr;
  logic [10-1:0] addr;
} instr_packet_s;

module top();
  logic clk = 0;
  logic din,dout;

  // These signals are here to test cocotb GPI

  

  // struct
  instr_packet_s inst;

  // struct array
  instr_packet_s inst_arr[1:0];

  // unpacked
  logic en[3:0];

  // arrays
  logic [5:0] v1;
  logic [1:0] v2 [5:0];
  logic v3[3:1][2:0];
  
  block block_i(clk, din, dout, inst, inst_arr, en);

  initial begin
    forever begin
      #10 clk <= ~clk;
    end
  end

  initial
    #2 inst.addr = 5;

endmodule

module block (
  input logic clk, din,
  output logic dout,

  // only here to test cocotb GPI
  input instr_packet_s inst_in,
  input instr_packet_s inst_arr_in[1:0],
  input logic en_in[3:0]
);

  logic en[3:0];

  reg [10:0] ctr = 0;

  always @(posedge clk) begin
    ctr <= ctr + 1;

    if (ctr !== 40)
      dout <= din;
  end

  assert property(@(negedge clk) din == dout);

endmodule
