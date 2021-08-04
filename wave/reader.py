import cocotb

test_arguments_exist = True

try:
    from test_customization import Arguments
except:
    test_arguments_exist = False


def read_argument(name, optional=False):
    if name in cocotb.plusargs:
        return cocotb.plusargs[name]
    elif hasattr(Arguments,name):
        return getattr(Arguments,name)

    if not optional:
        raise ValueError("Argument ", name, " is required and must be provided via plusarg or a test_cusomization.py file on path")
    else:
        return None

def read_wave():
    # get file postfix check if supported
    
    wavefile = read_argument('wavefile')
    wave_type = wavefile.split('.')[-1]

    supported_wave_formats = ['vcd', 'fsdb']

    if wave_type not in supported_wave_formats:
        raise ValueError("Wavefile type: ", wave_type, " is currently not supported. Supported formats are: ", supported_wave_formats)

    replay_block = read_argument('replay_block')

    # optional args
    inputs_only = read_argument('inputs_only')
    excluded_sigs = read_argument('excluded_sigs')

    data = None

    if wave_type == 'vcd':
        from wave.vcd_reader import VcdReader
        data = VcdReader(replay_block, wavefile, excluded_sigs, inputs_only)
    elif wave_type == 'fsdb':
        from wave.fsdb_reader import FsdbReader
        data = FsdbReader(replay_block, wavefile, excluded_sigs, inputs_only)

    return data     
