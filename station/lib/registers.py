import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x10)
    RAIL_CONTINUATION_N = grf.Temp(0x11)
    NEEDS_ESCALATOR_S = grf.Temp(0x12)
    NEEDS_ESCALATOR_N = grf.Temp(0x13)


code = (
    agrf_code
    + """
TEMP[0x10] = (rail_continuation & 0x1) == 0
TEMP[0x11] = (rail_continuation & 0x2) == 0
TEMP[0x12] = var(0x68, param=0x10, shift=0, and=0x300) == 0x100
TEMP[0x13] = var(0x68, param=0xF0, shift=0, and=0x300) == 0x100
"""
)
