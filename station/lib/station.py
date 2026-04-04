from agrf.lib.building.station import AStation as _AStation

from .registers import DEFAULT_CODE


class AStation(_AStation):
    def __init__(self, *args, **kwargs):
        extra_code = kwargs.pop("extra_code", "")
        super().__init__(*args, extra_code=DEFAULT_CODE + extra_code, **kwargs)
