import grf
from dataclasses import replace
from station.lib.registers import Registers
from agrf.lib.building.layout import (
    ALayout,
    NewGeneralSprite,
    AChildSprite,
    OffsetPosition,
    DefaultGraphics,
    NewGraphics,
)
from agrf.graphics.sprites.blend import BlendSprite
from agrf.graphics.misc import SCALE_TO_ZOOM


class AlphaBlendedSprites(grf.AlternativeSprites):
    def __init__(self, alts):
        sprites = []
        for scale in [1, 2, 4]:
            for bpp in [32]:
                if (s := alts[0].get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)) is not None:
                    for i in range(1, 10):
                        t = alts[i].get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)
                        # FIXME nobody renders for me :(
                        alts[i].voxel.render()
                        assert t is not None
                        s = BlendSprite(s, t)
                    sprites.append(s)

        super().__init__(*sprites)
        self.alts = alts

    def squash(self, ratio):
        return AlphaBlendedSprites([x.squash(ratio) for x in self.alts])

    def get_fingerprint(self):
        return {"alts": [x.get_fingerprint() for x in self.alts], "name": "alpha-blend"}


CACHE = {}


def blend_childsprites(cs):
    if id(cs[0]) in CACHE:
        return CACHE[id(cs[0].sprite)]
    sym = cs[0].sprite.symmetry

    sprites = []
    for i in sym.render_indices():
        sprites.append(AlphaBlendedSprites([sym.symmetry_item(x.sprite, i).sprite for x in cs]))

    rep = cs[0]
    CACHE[id(cs[0].sprite)] = AChildSprite(
        sym.create_variants(sprites),
        offset=rep.position.offset,
        flags=rep.flags,
        recolour=rep.sprite.recolour,
        palette=rep.sprite.palette,
    )
    return CACHE[id(cs[0].sprite)]
