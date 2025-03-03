from agrf.graphics.voxel import LazyVoxel
from station.lib import BuildingCylindrical

foundation = LazyVoxel(
    "foundation",
    prefix=".cache/render/station/dovemere_2018/foundation",
    voxel_getter=lambda path=f"station/voxels/dovemere_2018/foundation/foundation.vox": path,
    load_from="station/files/gorender.json",
)
foundation.in_place_subset(BuildingCylindrical.render_indices())
foundation.render()
