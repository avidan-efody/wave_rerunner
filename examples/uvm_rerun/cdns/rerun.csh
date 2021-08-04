#!/usr/bin/csh

setenv PYTHONPATH `pwd`:$PYTHONPATH

# required by cocotb
setenv MODULE injector.wave_rerunner
setenv TESTCASE ''
setenv TOPLEVEL post_uvm_top 
setenv TOPLEVEL_LANG verilog


# command line from cocotb example
#/p/hdk/rtl/cad/x86-64_linux44/cadence/xcelium/21.05.a001/tools.lnx86/bin/irun -timescale 1ns/1ps \
  -licqueue -64 -nclibdirpath sim_build -plinowarn  -v93 -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap +access+rwc  /nfs/site/disks/aefody_wa/cocotb/packages/cocotb-master/examples/simple_dff/dff.sv

irun -access rw -64 -uvmnocdnsextra -uvmhome $UVM_HOME +UVM_VERBOSITY=UVM_HIGH +UVM_TESTNAME=post_uvm_test -quiet -incdir $WAVE_RERUNNER/examples/sv/integrated/codec/vip -incdir $WAVE_RERUNNER/examples/sv/integrated/codec/ -incdir $WAVE_RERUNNER/examples/sv/integrated/apb  $WAVE_RERUNNER/examples/sv/integrated/codec/codec_pkg.sv $WAVE_RERUNNER/examples/sv/integrated/codec/post_uvm/post_uvm_top.sv -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap -l post_uvm.log

#-uvmhome /p/hdk/rtl/cad/x86-64_linux44/cadence/xcelium/21.05.a001/tools/methodology/UVM/CDNS-1.2/

