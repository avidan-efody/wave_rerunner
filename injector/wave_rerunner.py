# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
import os

import cocotb

from cocotb.triggers import Timer

from wave.reader import read_wave

from injector.cocotb_injector import CocotbInjector, CocotbDesignExplorer

from rerun_args.customize import *

@cocotb.test()
async def test_empty(dut):
    print("starting replay")

    # gets signals that cocotb can inject in relevant scopes
    design_explorer = CocotbDesignExplorer(dut)

    # get data from relevant wavefiles for the above signals
    data = read_wave(list(design_explorer.basic_sigs.keys()))

    # injects data on the signals
    injector = CocotbInjector(design_explorer)

    end_time = None
    if hasattr(Arguments, 'end_time'):
        end_time = Arguments.end_time

    sim_time = 0;

    while (True):
        values = data.get_values_at(sim_time)
        injector.inject_values(values)
        previous_time = sim_time
        sim_time = data.get_next_event(sim_time)
        if (sim_time == None) or ((end_time != None) and (sim_time >= end_time)): 
        	break
        await Timer(sim_time - previous_time)