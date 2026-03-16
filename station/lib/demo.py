from dataclasses import dataclass
from agrf.lib.building.layout import RenderContext as ProtoRenderContext, ALayout, DefaultGraphics
from agrf.lib.building.demo import Demo as ProtoDemo, DEFAULT_RENDER_CONTEXT
from .registers import Registers


@dataclass(frozen=True)
class RenderContext(ProtoRenderContext):
    north_bufferstop: bool = True
    south_bufferstop: bool = True

    def dodraw(self, register):
        if register is Registers.RAIL_CONTINUATION_N:
            return self.north_bufferstop
        if register is Registers.RAIL_CONTINUATION_S:
            return self.south_bufferstop
        if register is Registers.NIGHTGFX:
            return False
        if register is Registers.SNOW_NIGHTGFX:
            return False
        if register is Registers.RAIL_CONTINUATION_S_NIGHTGFX:
            return False
        if register is Registers.RAIL_CONTINUATION_N_NIGHTGFX:
            return False
        return True


def is_1012(l):
    return (
        isinstance(l, ALayout)
        and isinstance(l.ground_sprite.sprite, DefaultGraphics)
        and l.ground_sprite.sprite.sprite_id == 1012
    )


def is_1011(l):
    return (
        isinstance(l, ALayout)
        and isinstance(l.ground_sprite.sprite, DefaultGraphics)
        and l.ground_sprite.sprite.sprite_id == 1011
    )


@dataclass
class Demo(ProtoDemo):
    def infer_render_contexts(self):
        proto_ret = super().infer_render_contexts()

        ret = []
        for r, row in enumerate(self.tiles):
            ret_row = []
            for c, l in enumerate(row):
                nb = sb = True
                if is_1012(l):
                    if c + 1 < len(row) and is_1012(row[c + 1]):
                        nb = False
                    if c - 1 >= 0 and is_1012(row[c - 1]):
                        sb = False
                elif is_1011(l):
                    if r + 1 < len(self.tiles) and is_1011(self.tiles[r + 1][c]):
                        sb = False
                    if r - 1 >= 0 and is_1011(self.tiles[r - 1][c]):
                        nb = False
                ret_row.append(RenderContext(**vars(proto_ret[r][c]), north_bufferstop=nb, south_bufferstop=sb))
            ret.append(ret_row)
        return ret
