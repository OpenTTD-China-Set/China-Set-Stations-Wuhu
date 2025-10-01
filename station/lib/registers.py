import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x10)
    RAIL_CONTINUATION_N = grf.Temp(0x11)
    RECOLOUR_OFFSET_2 = grf.Temp(0x20)


code = agrf_code
default_code = """
TEMP[0x10] = (rail_continuation & 0x1) == 0
TEMP[0x11] = (rail_continuation & 0x2) == 0
TEMP[0x20] = 0x30b
"""
