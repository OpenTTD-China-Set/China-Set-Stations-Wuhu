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
        return false
    from agrf.lib.building.default import empty_ground

    if l.ground_sprite is empty_ground:
        # Hack for various sloped tiles
        return True
    return isinstance(l.ground_sprite.sprite, DefaultGraphics) and l.ground_sprite.sprite.sprite_id in [
        1011,
        1032,
        1034,
    ]


@dataclass
class Demo(ProtoDemo):
    def infer_render_contexts(self):
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
                if self.render_contexts is not None:
                    rc = self.render_contexts[r][c]
                else:
                    rc = DEFAULT_RENDER_CONTEXT
                ret_row.append(
                    RenderContext(
                        climate=rc.climate or self.climate,
                        subclimate=rc.subclimate or self.subclimate,
                        rail_type=rc.rail_type or self.rail_type,
                        north_bufferstop=nb,
                        south_bufferstop=sb,
                    )
                )
            ret.append(ret_row)
        return ret
