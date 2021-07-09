# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import random
import cocotb

from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

from pynpi import npisys
from pynpi import waveform

from functools import reduce

# wait delay instead of FallingEdge, binstr object?

class WaveData:
    def __init__(self, replay_block, wave_file):     
        self.replay_block = replay_block

        self.signal_values = self.extract_values_from_wave(self.replay_block)

    def extract_values_from_wave(self, replay_block):
    	pass

class SnpsWave(WaveData):
    def __init__(self, replay_block, wave_file):
        npisys.init(["anything"])

        self.fsdb = waveform.open("novas.fsdb")

        if not self.fsdb:
            print("Error. Failed to open file")

        super().__init__(replay_block, wave_file)

    def extract_values_from_wave(self, replay_block):
        scope = self.fsdb.scope_by_name(replay_block)

        signal_values = {}

        for sig in scope.sig_list():
            if sig.direction() == waveform.DirType_e.DirInput:
                print("extracting values for: ", sig.full_name())
                signal_values[sig.full_name()] = waveform.sig_hdl_value_between(sig,0,self.fsdb.max_time(),waveform.VctFormat_e.DecStrVal)

        return signal_values


class Injector:
    def __init__(self, dut, signal_values):
        self.coco_dut = dut
        self.signal_values = signal_values
        self.signal_changes = self.extract_events(self.signal_values)

    def extract_events(self, signal_values):
        all_changes = []

        for sig_name, sig_values in signal_values.items():
            all_changes.extend(sig_values)

        change_times = sorted(list(set([change[0] for change in all_changes])))

        return change_times

    def get_next_event(self, sim_time):
        next_time = next((change_time for change_time in self.signal_changes if change_time > sim_time), None)
        return next_time

    def get_values_at(self, sim_time):
        current_values = {}
        for sig_name, sig_values in self.signal_values.items():
            current_values[sig_name] = next((sig_value[1] for sig_value in sig_values[::-1] if sig_value[0] <= sim_time), None)

        return current_values  

    def get_cocotb_sig(self,sig_name):
         return reduce(getattr, sig_name.split('.')[1:], self.coco_dut)

    def inject_values(self, values):
        for sig_name, value in values.items():
            coco_sig = self.get_cocotb_sig(sig_name)
            coco_sig <= BinaryValue(value)

@cocotb.test()
async def test_empty(dut):
    """ doesn't do anything. workaround for COCOTB_SIM define not working? """
    print("starting replay")

    data = SnpsWave("top.block_i", "novas.fsdb")
    print(data.signal_values)
    injector = Injector(dut, data.signal_values)

    sim_time = 0;

    while (True):
        values = injector.get_values_at(sim_time)
        #print("time", sim_time, " values: ", values)
        injector.inject_values(values)
        previous_time = sim_time
        sim_time = injector.get_next_event(sim_time)
        if sim_time == None:
        	break
        await Timer(sim_time - previous_time)

# unit test
def test_injector():
    signal_values = {'top.block_i.clk': [(0, '0'), (10, '1'), (20, '0')], 'top.block_i.din': [(0, 'X'), (20, '0'), (40, '1')]}

    injector = Injector(signal_values)

    print(injector.get_next_event(5))
    print(injector.get_next_event(20))    
    print(injector.get_next_event(40)) 

    print(injector.get_values_at(10))

if __name__ == "__main__":
	test_injector()