import grf
from agrf.lib.building.registers import Registers as AGRFRegisters


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x10)
    RAIL_CONTINUATION_N = grf.Temp(0x11)
