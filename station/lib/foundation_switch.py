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
