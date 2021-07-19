# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import cocotb

from cocotb.triggers import Timer

from wave.fsdb_reader import FsdbReader

from injector.cocotb_injector import CocotbInjector

@cocotb.test()
async def test_empty(dut):
    """ doesn't do anything. workaround for COCOTB_SIM define not working? """
    print("starting replay")

    data = FsdbReader("top.block_i", "novas.fsdb")
    print(data.signal_values)
    injector = CocotbInjector(dut)

    sim_time = 0;

    while (True):
        values = data.get_values_at(sim_time)
        injector.inject_values(values)
        previous_time = sim_time
        sim_time = data.get_next_event(sim_time)
        if sim_time == None:
        	break
        await Timer(sim_time - previous_time)