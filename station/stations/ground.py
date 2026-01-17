from station.lib import BuildingCylindrical, BuildingSymmetricalX, AGroundSprite, ALayout, AttrDict
from agrf.graphics.voxel import LazyVoxel
from station.lib.registers import Registers


def quickload(name, symmetry):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
    )
    v.config["z_scale"] = 1.0

    v.render()
    sprite = symmetry.create_variants(v.spritesheet())
    named_images[(name, "")] = sprite
    ps = AGroundSprite(sprite, flags={"add": Registers.ZERO})
    named_ps[(name, "")] = ps
    l = ALayout(ps, [], False)
    named_tiles[(name, "")] = l
    return sprite


named_images = AttrDict(schema=("name", "subtype"))
named_ps = AttrDict(schema=("name", "subtype"))
named_tiles = AttrDict(schema=("name", "subtype"))

quickload("gray", BuildingCylindrical)
quickload("gray_box", BuildingCylindrical)
quickload("gray_third", BuildingSymmetricalX)

named_images.populate()
named_ps.populate()
named_tiles.populate()
