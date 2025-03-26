from station.lib import BuildingCylindrical, BuildingSymmetricalX, AGroundSprite, ALayout, AttrDict
from agrf.graphics.voxel import LazyVoxel
from station.lib.registers import Registers


def quickload(name, symmetry, parts=None):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
    )

    if parts is None:
        parts = []

    for i in range(2 ** len(parts)):
        subtype = "_".join([parts[j] for j in range(len(parts)) if (i & (2**j)) == 0])
        v2 = v.discard_layers(tuple(parts[j] for j in range(len(parts)) if (i & (2**j)) > 0), subtype)

        sprite = symmetry.create_variants(v2.spritesheet())
        named_images[(name, subtype)] = sprite
        ps = AGroundSprite(sprite, flags={"add": Registers.ZERO})
        named_ps[(name, subtype)] = ps
        l = ALayout(ps, [], False)
        named_tiles[(name, subtype)] = l
    return sprite


named_images = AttrDict(schema=("name", "subtype"))
named_ps = AttrDict(schema=("name", "subtype"))
named_tiles = AttrDict(schema=("name", "subtype"))

quickload("gray", BuildingCylindrical, ["top", "right"])
quickload("gray_third", BuildingSymmetricalX)

named_images.populate()
named_ps.populate()
named_tiles.populate()
