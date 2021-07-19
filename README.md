# wave rerunner
 
This repo contains:
- python packages that read wave files in various formats (fsdb, shm, wlf, vcd) into python data structure.
- python packages to inject data from the python data structures back into a design (via cocotb or plain vpi)
- examples showing how these capabilities could be applied to common verification tasks:
-- replaying SVA assertions from wave, for fast development cycle of assertions
-- replaying UVM monitors, checkers, coverage from wave, for fast developement cycle of coverage/checkers
-- batch searching of wave files and extraction of signal level coverage data from wave

## pre-requisites

- cocotb (currently required for injecting anything back)
- rerunning SVA/UVM requires commercial simulator

## running the examples

### SVA rerun

- cd examples/snps/setup
- source sourceme.snps
- cd ../../sva_rerun
- ./run.csh 
- ./rerun.csh
