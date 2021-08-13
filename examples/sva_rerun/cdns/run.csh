#!/usr/bin/csh

setenv PYTHONPATH ../:$PYTHONPATH

# required by cocotb
setenv MODULE test_dut
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

xrun +access+rwc -64 +define+COCOTB_SIM=1 -sv $WAVE_RERUNNER/examples/sv/very_simple_top.sv -loadvpi libcocotbvpi_ius.so:vlog_startup_routines_bootstrap -input vcd.tcl 