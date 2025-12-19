from agrf.magic import Switch
from dataclasses import dataclass
from typing import List


@dataclass
class FoundationSwitch:
    # For now, it's just (None, top, right, top-right)
    foundations: List

    def make_sprite(self, slope_type, render_context):
        return self.foundations[int(render_context.nw_pit == 0) + 2 * int(render_context.ne_pit == 0)].make_sprite(
            slope_type, render_context
        )

    def convert_foundation_to_ground(self):
        return self.foundations[3].convert_foundation_to_ground()

    def to_switch(self):
        def is_same_newgrf(offset):
            return f"(var(0x68, param={offset}, shift=0, and=0x300) == 0x100)"

        def is_supported_1(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xf03e) == 0x7024)"

        def is_supported_2(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xf03e) == 0x7026)"

        def is_elevated(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xf03e) == 0x702c)"

        def is_wuhu_north(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xf000) == 0x3000)"

        def is_sunken_ground(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xfffe) == 0x7ffc)"

        def is_pit(offset):
            return f"(({is_supported_1(offset)} + {is_supported_2(offset)} + {is_elevated(offset)} + {is_wuhu_north(offset)} + {is_sunken_ground(offset)}) >= 1)"

        return Switch(
            ranges={i: self.foundations[i] for i in range(3)},
            default=self.foundations[3],
            code=f"(1 - ({is_same_newgrf(0xf0)} * {is_pit(0xf0)}))"
            + f"+ 2 * (1 - ({is_same_newgrf(0x0f)} * {is_pit(0x0f)}))",
        )
