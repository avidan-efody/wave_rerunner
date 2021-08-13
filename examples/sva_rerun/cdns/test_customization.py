from rerun_types.types import *

class Arguments:
	wavefile = "my_vcd.vcd"
	replay_block = "top.block_i"
	sigs_directions = [rerun_direction.input]
	excluded_sigs = []