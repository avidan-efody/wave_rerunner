

from wave.reader_base import ReaderBase, ScopeNotFound

class ShmReader(ReaderBase):
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):
        # initialize indago server, open shm here


    def extract_values_from_wave(self, replay_blocks, excluded_sigs = [], inputs_only=True):
        # if replay_blocks contains "top.block", "top.other_block" 
        # and top.block has signal x, and top.other_block has signal y
        # return a hash {"top.block.x" : [(0, 'x'), (50,'1')], "top.other_block.y: [(0, 'z'), (20, '1')]}"}