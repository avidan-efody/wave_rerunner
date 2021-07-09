#!/usr/bin/csh

# required by cocotb
setenv MODULE test_dut
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

vcs -top top  +acc+1 +vpi -P pli.tab +define+COCOTB_SIM=1 -sverilog -timescale=1ns/1ps -full64 -debug -debug_access -kdb -load libcocotbvpi_vcs.so simple_top.sv

./simv +define+COCOTB_SIM=1 -full64 -ucli -do dump.cmd
