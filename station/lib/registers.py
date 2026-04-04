import grf
from agrf.lib.building.registers import Registers as AGRFRegisters

DEFAULT_CODE = """
TEMP[0x10] = (rail_continuation & 0x1) == 0
TEMP[0x11] = (rail_continuation & 0x2) == 0
"""


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x10)
    RAIL_CONTINUATION_N = grf.Temp(0x11)
