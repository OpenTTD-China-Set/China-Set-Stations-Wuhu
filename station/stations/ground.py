from station.lib import BuildingCylindrical, BuildingSymmetricalX, AGroundSprite, AParentSprite, ALayout, AttrDict
from agrf.graphics.voxel import LazyVoxel
from station.lib.registers import Registers


def quickload(name, symmetry, width):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
    )

    sprite = symmetry.create_variants(v.spritesheet())

    if width == 16:
        gs = AGroundSprite(sprite, flags={"add": Registers.ZERO})
        ground_gs[name] = gs

    ps = AParentSprite(sprite, (width, 16, 0), (0, 0, 0), flags={"add": Registers.ZERO})
    ground_ps[name] = ps

    if width == 16:
        l = ALayout(gs, [], False)
        ground_tiles[name] = l

    return sprite


ground_gs = AttrDict()
ground_ps = AttrDict()
ground_tiles = AttrDict()

quickload("gray", BuildingCylindrical, 16)
quickload("gray_third", BuildingSymmetricalX, 5)
