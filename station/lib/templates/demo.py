import grf
from station.lib import ALayout, AParentSprite, LayoutSprite, Demo, Registers, add_night_masks


class FingerprintAlternativeSprites(grf.AlternativeSprites):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def get_fingerprint(self):
        return {f"{s.scale}_{s.bpp}": s.get_fingerprint() for s in self.sprites}


def make_demo(switch, w, h, preswitch=None, *, layouts):
    demo = Demo(switch.demo(w, h, preswitch))
    for i, var in enumerate([demo, demo.M]):
        sprite = FingerprintAlternativeSprites(
            *[
                LayoutSprite(
                    var,
                    64 * scale,
                    64 * scale,
                    xofs=(1 - i % 2 * 2) * int((w - h) / (w + h + 1) * 32 * scale),
                    yofs=0,
                    scale=scale,
                    bpp=bpp,
                    crop=False,
                )
                for scale in [1, 2]
                for bpp in [32]
            ]
        )
        layout = ALayout(
            None,
            [AParentSprite(sprite, (16, 16, 48), (0, 0, 0), flags={"add_palette": Registers.RECOLOUR_OFFSET})],
            False,
            category=b"\xe8\x8a\x9cA",
        )
        layout = add_night_masks(layout)
        layouts.append(layout)
        if i == 0:
            ret = layout
    return ret
