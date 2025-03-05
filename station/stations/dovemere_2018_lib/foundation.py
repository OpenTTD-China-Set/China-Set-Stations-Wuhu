from agrf.graphics.voxel import LazyVoxel
from station.lib import BuildingSymmetrical

v = LazyVoxel(
    "foundation",
    prefix=".cache/render/station/dovemere_2018/foundation",
    voxel_getter=lambda path=f"station/voxels/dovemere_2018/foundation/foundation.vox": path,
    load_from="station/files/gorender.json",
)
v.in_place_subset(BuildingSymmetrical.render_indices())
foundation = BuildingSymmetrical.create_variants(v.spritesheet())
