import grf
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
from station.stations.misc import track, default
from station.stations.platform_lib.ground import pillar_base_merged, pillar
from station.stations.platform_lib.data import sunken_ground


def quickload(name, symmetry, traversable):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
        config={"z_scale": 1.0},
    )
    sprite = symmetry.create_variants(v.spritesheet(zdiff=8, xdiff=platform_width, xspan=16 - platform_width))

    parent = AParentSprite(sprite, (16, 16 - platform_width, 32), (0, platform_width, 0))
    plat = platform_ps.cns_concrete_solid_shelter_2.up(8)

    l = ALayout(None, [plat.T, pillar.T, parent], traversable, notes=["pit"])
    l.foundation = pillar_base_merged.T
    ret = symmetry.create_variants(symmetry.get_all_variants(l))
    entries.extend(symmetry.get_all_entries(ret))
    named_tiles[name] = ret


entries = []
named_tiles = AttrDict()
for name, symmetry, traversable in [
    ("escalator_1", BuildingFull, False),
    ("escalator_2", BuildingFull, False),
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
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(default=entry, purchase=0),
                **station_cb["E9B8A0A"],
            },
            general_flags=0b10000,
            make_foundation=True,
            extra_code=station_code["E9B8A0A"],
            enable_if=[parameter_list["E9B8A0A_ENABLE_MODULAR"]],
            doc_layout=entry,
        )
    )


plat = platform_tiles.cns_concrete_supported2_shelter_2
elev1 = platform_tiles.cns_concrete_elevated_shelter_2.T
elev2 = platform_tiles.cns_concrete_elevated2_shelter_2.T
gate = named_tiles.front_gate
normal = named_tiles.escalator_2
escalator = named_tiles.escalator_1

the_stations = AMetaStation(
    station_tiles,
    b"\xe9\xb8\xa0A",
    None,
    [
        Demo(
            [
                [default] * 12,
                [
                    default,
                    elev2.T,
                    elev2.T,
                    escalator.T,
                    normal.T,
                    gate.T,
                    gate.T.R,
                    normal.T.R,
                    escalator.T.R,
                    elev2.T,
                    elev2.T,
                    default,
                ],
                [track] + [plat.T] * 10 + [track],
                [track] * 12,
                [track] * 12,
                [track] + [plat] * 10 + [track],
                [default, elev2, elev2, escalator, normal, gate, gate.R, normal.R, escalator.R, elev2, elev2, default],
                [default] * 12,
            ],
            "Test",
            altitude=[[0] * 13] * 2 + [[1] * 13] + [[1] + [2] * 11 + [1]] * 3 + [[1] * 13] + [[0] * 13] * 2,
        ),
        Demo(
            [
                [default] * 12,
                [
                    default,
                    elev1.T,
                    elev2.T,
                    escalator.T,
                    normal.T,
                    gate.T,
                    gate.T.R,
                    normal.T.R,
                    escalator.T.R,
                    elev2.T,
                    elev1.T,
                    default,
                ],
                [track] + [plat.T] * 10 + [track],
                [track] * 12,
                [track] * 12,
                [track] + [plat] * 10 + [track],
                [default, elev1, elev2, escalator, normal, gate, gate.R, normal.R, escalator.R, elev2, elev1, default],
                [default] * 12,
            ],
            "Test 2",
            altitude=[[0] * 13]
            + [[1] * 2 + [0] * 9 + [1] * 2]
            + [[1] * 13]
            + [[1] + [2] * 11 + [1]] * 3
            + [[1] * 13]
            + [[1] * 2 + [0] * 9 + [1] * 2]
            + [[0] * 13],
        ),
        Demo(
            [
                [default] * 12,
                [
                    sunken_ground,
                    elev2.T,
                    elev2.T,
                    escalator.T,
                    normal.T,
                    gate.T,
                    gate.T.R,
                    normal.T.R,
                    escalator.T.R,
                    elev2.T,
                    elev2.T,
                    sunken_ground,
                ],
                [track] + [plat.T] * 10 + [track],
                [track] * 12,
                [track] * 12,
                [track] + [plat] * 10 + [track],
                [
                    sunken_ground,
                    elev2,
                    elev2,
                    escalator,
                    normal,
                    gate,
                    gate.R,
                    normal.R,
                    escalator.R,
                    elev2,
                    elev2,
                    sunken_ground,
                ],
                [default] * 12,
            ],
            "Test 3",
            altitude=[[0] * 13] * 2 + [[1] * 13] + [[1] + [2] * 11 + [1]] * 3 + [[1] * 13] + [[0] * 13] * 2,
        ),
    ],
)
