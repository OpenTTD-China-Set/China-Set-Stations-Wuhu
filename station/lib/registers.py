import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x20)
    RAIL_CONTINUATION_N = grf.Temp(0x21)


code = (
    agrf_code
    + """
TEMP[0x20] = (rail_continuation & 0x1) == 0
TEMP[0x21] = (rail_continuation & 0x2) == 0
"""
)
