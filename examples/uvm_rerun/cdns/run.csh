#!/usr/bin/csh

# command line from cocotb example
#/p/hdk/rtl/cad/x86-64_linux44/cadence/xcelium/21.05.a001/tools.lnx86/bin/irun -timescale 1ns/1ps \
  -licqueue -64 -nclibdirpath sim_build -plinowarn  -v93 -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap +access+rwc  /nfs/site/disks/aefody_wa/cocotb/packages/cocotb-master/examples/simple_dff/dff.sv

#xrun +access+rwc -64 +define+COCOTB_SIM=1 -sv +UVM_VERBOSITY=UVM_HIGH +UVM_TESTNAME=codec_test +incdir+$UVM_HOME/src $UVM_HOME/src/uvm.sv  +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/vip +incdir+$WAVE_RERUNNER/examples/sv/integrated/codec/ +incdir+$WAVE_RERUNNER/examples/sv/integrated/apb  $WAVE_RERUNNER/examples/sv/integrated/codec/codec_pkg.sv $WAVE_RERUNNER/examples/sv/integrated/codec/tb_top.sv -loadvpi /nfs/site/disks/home_user/aefody/.local/lib/python3.7/site-packages/cocotb/libs/libcocotbvpi_ius.so:vlog_startup_routines_bootstrap -input vcd.tcl 

irun -access rw -64 -uvmnocdnsextra -uvmhome $UVM_HOME +UVM_VERBOSITY=UVM_LOW +UVM_TESTNAME=codec_test -quiet -incdir $WAVE_RERUNNER/examples/sv/integrated/codec/vip -incdir $WAVE_RERUNNER/examples/sv/integrated/codec/ -incdir $WAVE_RERUNNER/examples/sv/integrated/apb  $WAVE_RERUNNER/examples/sv/integrated/codec/codec_pkg.sv $WAVE_RERUNNER/examples/sv/integrated/codec/tb_top.sv -input vcd.tcl

#-uvmhome `ncroot`/tools/uvm-1.1 
