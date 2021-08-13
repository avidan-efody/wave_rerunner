#!/usr/bin/csh

setenv PYTHONPATH `pwd`:$PYTHONPATH

# required by cocotb
setenv MODULE injector.wave_rerunner
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog

./simv +define+COCOTB_SIM=1  -full64 -ucli -do post_dump.cmd
