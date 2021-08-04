#!/usr/bin/csh

setenv PYTHONPATH `pwd`:$PYTHONPATH

# required by cocotb
setenv MODULE injector.wave_rerunner
setenv TESTCASE ''
setenv TOPLEVEL top 
setenv TOPLEVEL_LANG verilog


# command line from cocotb example
#/p/hdk/rtl/cad/x86-64_linux44/cadence/xcelium/21.05.a001/tools.lnx86/bin/irun -timescale 1ns/1ps \
  -licqueue -64 -nclibdirpath sim_build -plinowarn  -v93 -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap +access+rwc  /nfs/site/disks/aefody_wa/cocotb/packages/cocotb-master/examples/simple_dff/dff.sv

xrun +access+rwc -64 +define+COCOTB_SIM=1 -sv $WAVE_RERUNNER/examples/sv/simple_top.sv -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap
