from agrf.lib.building.station import AStation as _AStation

RAIL_CONTINUATION_CODE = """
TEMP[0x10] = (rail_continuation & 0x1) == 0
TEMP[0x11] = (rail_continuation & 0x2) == 0
"""


class AStation(_AStation):
    def __init__(self, *args, **kwargs):
        extra_code = kwargs.pop("extra_code", "")
        super().__init__(*args, extra_code=RAIL_CONTINUATION_CODE + extra_code, **kwargs)
