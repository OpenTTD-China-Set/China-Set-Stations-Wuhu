import types
from station.lib import BuildingCylindrical, BuildingFull
from agrf.sprites import empty_alternatives


def make_empty_variant(w, h, x, y, offset=0, span=16):
    if offset == 0 and span == 16:
        empty_image = empty_alternatives(w, h, x, y)
        empty_image.squash = types.MethodType(lambda self, *args, empty_image=empty_image: self, empty_image)
        return BuildingCylindrical.create_variants([empty_image])
    deltas = [[-2, -1], [2, -1], [-2, -1], [2, -1], [2, 1], [-2, 1], [2, 1], [-2, 1]]
    offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [-2, -1], [2, -1], [-2, -1], [2, -1]]

    empty_images = []
    for i in range(8):
        x1 = x + deltas[i][0] * offset + offsets[i][0] * (16 - span)
        y1 = y + deltas[i][1] * offset + offsets[i][1] * (16 - span)

        empty_image = empty_alternatives(w, h, x1, y1)
        empty_image.squash = types.MethodType(lambda self, *args, empty_image=empty_image: self, empty_image)
        empty_images.append(empty_image)
    return BuildingFull.create_variants(empty_images)


empty_offset = (-31, -34)
empty_sprite = make_empty_variant(64, 68, *empty_offset)
