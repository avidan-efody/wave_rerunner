# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge


@cocotb.test()
async def test_dut(dut):
    """ test our simple DUT """
    print("starting test")

    i = 0

    while i<100:
        i = i+1
        dut.din <= random.randint(0,1)
        await FallingEdge(dut.clk)
