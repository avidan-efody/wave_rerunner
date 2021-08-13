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