import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code


class Registers(AGRFRegisters):
    RAIL_CONTINUATION_S = grf.Temp(0x10)
    RAIL_CONTINUATION_N = grf.Temp(0x11)
    NIGHTGFX = grf.Temp(0x20)
    SNOW_NIGHTGFX = grf.Temp(0x21)
    RAIL_CONTINUATION_S_NIGHTGFX = grf.Temp(0x22)
    RAIL_CONTINUATION_N_NIGHTGFX = grf.Temp(0x23)


night = f"var(0x7F, param=15, shift=0, and=0x7)"

code = f"""
TEMP[0x20] = (({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)
""" + agrf_code
default_code = f"""
TEMP[0x10] = (rail_continuation & 0x1) == 0
TEMP[0x11] = (rail_continuation & 0x2) == 0
TEMP[0x21] = ((({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)) * ((terrain_type & 0x4) == 0x4)
TEMP[0x22] = ((({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)) * ((rail_continuation & 0x1) == 0)
TEMP[0x23] = ((({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)) * ((rail_continuation & 0x2) == 0)
"""
