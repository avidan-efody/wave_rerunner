# move to pytest
from wave.reader_base import ReaderBase

import pytest

class MockReader(ReaderBase):
    def __init__(self, replay_block, wave_file, excluded_sigs, inputs_only):
        super().__init__(replay_block, wave_file, excluded_sigs, inputs_only)

    def extract_values_from_wave(self, replay_block, excluded_sigs, inputs_only):
    	return {'top.block_i.clk': [(0, '0'), (10, '1'), (20, '0')], 'top.block_i.din': [(0, 'X'), (20, '0'), (40, '1')]}

def test_get_next_event():
    data = MockReader("fake", "fake", [], False)

    next_time = data.get_next_event(5)
    assert next_time == 10

    next_time = data.get_next_event(20)
    assert next_time == 40

    next_time = data.get_next_event(40)
    assert next_time == None 

def test_get_values_at():
    data = MockReader("fake", "fake", [], False)

    signal_values = data.get_values_at(10)

    assert signal_values['top.block_i.din'] == 'X'