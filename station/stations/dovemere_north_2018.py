from station.lib import (
    AStation,
    AMetaStation,
    BuildingSymmetricalX,
    BuildingFull,
    Demo,
    AParentSprite,
    ALayout,
    AttrDict,
)
from station.lib.parameters import parameter_list, station_cb, station_code
from agrf.graphics.voxel import LazyVoxel
from .platforms import platform_ps, platform_width, platform_tiles


def quickload(name, symmetry, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
        config={"z_scale": 1.0},
    )
    sprite = symmetry.create_variants(v.spritesheet(zdiff=8, xdiff=platform_width, xspan=16 - platform_width))

    parent = AParentSprite(sprite, (16, 16 - platform_width, 32), (0, platform_width, 0))
    plat = platform_ps.cns_concrete_side_shelter_2.up(8)

    l = ALayout(None, [plat.T, parent], traversable)
    ret = symmetry.create_variants(symmetry.get_all_variants(l))
    entries.extend(symmetry.get_all_entries(ret))
    named_tiles[name] = ret


entries = []
named_tiles = AttrDict()
for name, symmetry, traversable in [
    ("escalator", BuildingFull, False),
    ("front_normal", BuildingSymmetricalX, False),
    ("front_gate", BuildingFull, False),
]:
    quickload(name, symmetry, traversable)

station_tiles = []
for i, entry in enumerate(entries):
    station_tiles.append(
        AStation(
            id=0x3000 + i,
            translation_name="BUILDING",
            layouts=[entry, entry.M],
            class_label=b"\xe9\xb8\xa0A",
            cargo_threshold=40,
            non_traversable_tiles=0b11,
            # general_flags=0x08, # FIXME: handle custom foundation later
            callbacks={"select_tile_layout": 0, **station_cb["E9B8A0A"]},
            extra_code=station_code["E9B8A0A"],
            enable_if=[parameter_list["E9B8A0A_ENABLE_MODULAR"]],
            doc_layout=entry,
        )
    )


plat = platform_tiles.cns_concrete_shelter_2
gate_T = named_tiles.front_gate.T.lower_tile()
gate = named_tiles.front_gate.lower_tile()
normal_T = named_tiles.front_normal.T.lower_tile()
normal = named_tiles.front_normal.lower_tile()
escalator_T = named_tiles.escalator.T.lower_tile()
escalator = named_tiles.escalator.lower_tile()

the_stations = AMetaStation(
    station_tiles,
    b"\xe9\xb8\xa0A",
    None,
    [
        Demo(
            [
                [escalator_T, normal_T, gate_T, gate_T.R, normal_T.R, escalator_T.R],
                [plat.T] * 6,
                [plat] * 6,
                [escalator, normal, gate, gate.R, normal.R, escalator.R],
            ],
            "Test",
        )
    ],
)
