from agrf.global_cache import make_switch
from dataclasses import dataclass
from typing import List
from station.lib import AParentSprite
from station.lib.registers import Registers


@dataclass
class FoundationSwitch:
    foundations: List
    my_elevation: int

    def make_sprite(self, slope_type, render_context):
        if render_context.sw_shareground:
            print(
                render_context.nw_wall
                + 3 * render_context.ne_wall
                + 9 * render_context.n_wall
                + 27 * render_context.sw_shareground
                + 54 * render_context.se_shareground
            )

        return self.foundations[
            render_context.nw_wall
            + 3 * render_context.ne_wall
            + 9 * render_context.n_wall
            + 27 * render_context.sw_shareground
            + 54 * render_context.se_shareground
        ].make_sprite(slope_type, render_context)

    def add_to_layout(self, l, m=False):
        return self.to_switch(ground=True, m=m).fmap(
            lambda x: l
            + AParentSprite(
                x.convert_foundation_to_ground(), (16, 16, 0), (0, 0, 0), flags={"dodraw": Registers.NOSLOPE}
            )
        )

    def convert_foundation_to_ground(self):
        return self.foundations[26].convert_foundation_to_ground()

    def to_switch(self, ground=False, m=False):
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
            return f"(var(0x6b, param={offset}, shift=0, and=0xffff) == 0x7ffc)"

        def is_sunken_ground_2(offset):
            return f"(var(0x6b, param={offset}, shift=0, and=0xffff) == 0x7ffd)"

        def tile_elevation(offset):
            return f"(var(0x67, param={offset}, shift=16, and=0xff) + (var(0x67, param={offset}, shift=0, and=0xff) + 15) / 16)"

        ELEVLIST = [
            (is_supported_1, -1),
            (is_supported_2, -2),
            (is_elevated, -1),
            (is_wuhu_north, -1),
            (is_sunken_ground, -1),
            (is_sunken_ground_2, -2),
        ]

        def relative_elevation_unbounded(offset):
            tile_elevation_delta = "(" + "+".join(f"({pred(offset)} * ({coeff}))" for pred, coeff in ELEVLIST) + ")"
            return f"(({is_same_newgrf(offset)} * ({tile_elevation_delta} + {tile_elevation(offset)} - {tile_elevation(0x0)})) - ({self.my_elevation}))"

        def relative_elevation(offset):
            return f"min(max({relative_elevation_unbounded(offset)}, 0), 2)"

        def share_ground(offset):
            return f"({relative_elevation_unbounded(offset)} == 0)"

        if ground:
            coeff1 = "1"
            coeff2 = "3"
        else:
            coeff1 = "(1 + extra_callback_info2 % 2 * 2)"
            coeff2 = "(3 - extra_callback_info2 % 2 * 2)"

        def permute(i, m):
            if not m:
                return i
            a, b, c, d, e = i % 3, i // 3 % 3, i // 9 % 3, i // 27 % 2, i // 54
            return a * 3 + b + c * 9 + d * 54 + e * 27

        return make_switch(
            ranges={i: self.foundations[permute(i, m)] for i in range(1, 108)},
            default=self.foundations[0],
            code=f"{coeff1} * {relative_elevation(0xf0)} + {coeff2} * {relative_elevation(0x0f)} + 9 * {relative_elevation(0xff)} + 27 * {share_ground(0x01)} + 54 * {share_ground(0x10)}",
        )
