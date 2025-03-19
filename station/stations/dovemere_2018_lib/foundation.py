from agrf.graphics.voxel import LazyVoxel
from station.lib import BuildingSymmetrical, BuildingCylindrical, AttrDict

named_foundations = AttrDict(schema=("name",))


def register(name, sym):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/foundation",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/foundation/{name}.vox": path,
        load_from="station/files/gorender.json",
        config={"z_scale": 1.0},
    )
    v.in_place_subset(sym.render_indices())
    named_foundations[name] = sym.create_variants(v.spritesheet())


register("foundation", BuildingSymmetrical)
register("four_sides", BuildingCylindrical)

named_foundations.populate()
