from dataclasses import dataclass
from agrf.lib.building.layout import RenderContext as ProtoRenderContext, ALayout, DefaultGraphics
from agrf.lib.building.demo import Demo as ProtoDemo, DEFAULT_RENDER_CONTEXT
from .registers import Registers


@dataclass(frozen=True)
class RenderContext(ProtoRenderContext):
    north_bufferstop: bool = True
    south_bufferstop: bool = True
    nw_wall: int = 0
    ne_wall: int = 0
    n_wall: int = 0
    sw_shareground: int = 0
    se_shareground: int = 0

    def dodraw(self, register):
        if register is Registers.RAIL_CONTINUATION_N:
            return self.north_bufferstop
        if register is Registers.RAIL_CONTINUATION_S:
            return self.south_bufferstop
        return True


def is_1012(l):
    if not isinstance(l, ALayout):
        return False
    from agrf.lib.building.default import empty_ground

    if l.ground_sprite is empty_ground:
        # Hack for various sloped tiles
        return True
    return isinstance(l.ground_sprite.sprite, DefaultGraphics) and l.ground_sprite.sprite.sprite_id in [
        1012,
        1031,
        1033,
    ]


def is_1011(l):
    if not isinstance(l, ALayout):
        return False
    from agrf.lib.building.default import empty_ground

    if l.ground_sprite is empty_ground:
        # Hack for various sloped tiles
        return True
    return isinstance(l.ground_sprite.sprite, DefaultGraphics) and l.ground_sprite.sprite.sprite_id in [
        1011,
        1032,
        1034,
    ]


def is_pit(l):
    return "pit" in l.notes


@dataclass
class Demo(ProtoDemo):
    def infer_render_contexts(self):
        proto_ret = super().infer_render_contexts()

        R = len(self.tiles)
        C = len(self.tiles[0])

        ret = []
        for r, row in enumerate(self.tiles):
            ret_row = []
            for c, l in enumerate(row):
                nb = sb = True
                if is_1012(l):
                    if c + 1 < C and is_1012(row[c + 1]):
                        nb = False
                    if c - 1 >= 0 and is_1012(row[c - 1]):
                        sb = False
                elif is_1011(l):
                    if r + 1 < R and is_1011(self.tiles[r + 1][c]):
                        sb = False
                    if r - 1 >= 0 and is_1011(self.tiles[r - 1][c]):
                        nb = False
                if r - 1 >= 0 and is_pit(self.tiles[r - 1][c]):
                    nw_wall = 0
                else:
                    nw_wall = 2
                if c + 1 < C and is_pit(self.tiles[r][c + 1]):
                    ne_wall = 0
                else:
                    ne_wall = 2
                if r - 1 >= 0 and c + 1 < len(row) and is_pit(self.tiles[r - 1][c + 1]):
                    n_wall = 0
                else:
                    n_wall = 2
                if c - 1 >= 0 and is_pit(self.tiles[r][c - 1]):
                    sw_shareground = 1
                else:
                    sw_shareground = 0
                if r + 1 < R and is_pit(self.tiles[r + 1][c]):
                    se_shareground = 1
                else:
                    se_shareground = 0
                ret_row.append(
                    RenderContext(
                        **vars(proto_ret[r][c]),
                        north_bufferstop=nb,
                        south_bufferstop=sb,
                        nw_wall=nw_wall,
                        ne_wall=ne_wall,
                        n_wall=n_wall,
                        sw_shareground=sw_shareground,
                        se_shareground=se_shareground,
                    )
                )
            ret.append(ret_row)
        return ret
