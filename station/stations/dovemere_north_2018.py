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
    AGroundSprite,
)
from station.lib.parameters import parameter_list, station_cb, station_code
from agrf.graphics.voxel import LazyVoxel
from .platforms import platform_ps, platform_width, platform_tiles
from station.stations.misc import track, default
from station.stations.platform_lib.ground import (
    pillar_base_merged,
    pillar,
    pillar_base_underground_gs,
    empty_base_merged,
    empty_base_underground_gs,
    merge_ground,
)
from station.stations.platform_lib.data import sunken_ground

entries = []
named_tiles = AttrDict(schema=("part", "platform", "shelter"))
height = 25


def quickload(name, symmetry, traversable):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
        config={"z_scale": 1.0},
    )
    vg = v.mask_clip_away("station/voxels/foundation/masks/above_ground.vox", "under_ground")
    v = v.mask_clip_away("station/voxels/foundation/masks/ground_level.vox", "above_ground")
    vgsprite = symmetry.create_variants(vg.spritesheet())
    sprite = symmetry.create_variants(v.spritesheet(zdiff=8, xdiff=platform_width, xspan=16 - platform_width))

    vg_merged = merge_ground(vgsprite)
    vg_gs = AGroundSprite(vg_merged.symmetry_fmap(lambda y: y.convert_foundation_to_ground()))
    parent = AParentSprite(sprite, (16, 16 - platform_width, height), (0, platform_width, 0))

    for platform_type in ["", "concrete", "brick"]:
        for shelter_type in ["", "shelter_1", "shelter_2"]:
            if name == "escalator_1" and platform_type == "":
                continue
            if platform_type == "" and shelter_type != "":
                continue

            components = [parent]
            foundation = empty_base_merged
            foundation_gs = empty_base_underground_gs
            if platform_type != "":
                plat = platform_ps[
                    ("cns", platform_type, "solid", shelter_type, "" if shelter_type == "" else "combining")
                ].up(8)
                components.append(pillar.T)
                components.append(plat.T)
                foundation = pillar_base_merged.T
                foundation_gs = pillar_base_underground_gs.T
            foundation = vg_merged
            foundation_gs = vg_gs

            l = ALayout(None, components, traversable, notes=["pit"])
            l2 = ALayout(foundation_gs, components, traversable, notes=["pit"])
            l.foundation = foundation
            ret = symmetry.create_variants(symmetry.get_all_variants(l))
            ret.purchase = l2
            ret.T.purchase = l2.T
            ret.M.purchase = l2.M
            ret.T.M.purchase = l2.T.M
            ret.R.purchase = l2.R
            ret.T.R.purchase = l2.T.R
            ret.R.M.purchase = l2.R.M
            ret.T.R.M.purchase = l2.T.R.M
            entries.extend(symmetry.get_all_entries(ret))
            named_tiles[(name, platform_type, shelter_type)] = ret


for name, symmetry, traversable in [
    ("escalator_1", BuildingFull, False),
    ("escalator_2", BuildingFull, False),
    ("front_gate", BuildingFull, False),
]:
    quickload(name, symmetry, traversable)

station_tiles = []
for i, entry in enumerate(entries):
    new_entry = entry.foundation.add_to_layout(entry)
    new_entry_M = entry.foundation.M.add_to_layout(entry.M, m=True)

    layouts = [entry.purchase, entry.purchase.M, new_entry.default, new_entry_M.default]
    for x, y in zip(new_entry._ranges, new_entry_M._ranges):
        layouts.append(x.ref)
        layouts.append(y.ref)
    sprite_layout = grf.DualCallback(default=new_entry.to_index(layouts), purchase=0)
    foundation_object = entry.foundation
    doc_layout = entry + AParentSprite(entry.foundation.convert_foundation_to_ground(), (16, 16, 0), (0, 0, 0))
    station_tiles.append(
        AStation(
            id=0x3000 + i,
            translation_name="BUILDING",
            layouts=layouts,
            class_label=b"\xe9\xb8\xa0A",
            cargo_threshold=40,
            non_traversable_tiles=0b11,
            callbacks={"select_tile_layout": 0, "select_sprite_layout": sprite_layout, **station_cb["E9B8A0A"]},
            general_flags=0b10000,
            make_foundation=False,
            foundation_object=foundation_object,
            extra_code=station_code["E9B8A0A"],
            enable_if=[parameter_list["E9B8A0A_ENABLE_MODULAR"]],
            doc_layout=doc_layout,
        )
    )


named_tiles.populate()
plat = platform_tiles.cns_concrete_supported2_shelter_2
platx = platform_tiles.cns_concrete_supported2
elev1 = platform_tiles.cns_concrete_elevated_shelter_2.T
elev2 = platform_tiles.cns_concrete_elevated2_shelter_2.T
elev2x = platform_tiles.cns_concrete_elevated2.T
gate = named_tiles.front_gate_concrete_shelter_2
normal = named_tiles.escalator_2_concrete_shelter_2
escalator = named_tiles.escalator_1_concrete_shelter_2
gatex = named_tiles.front_gate_concrete
normalx = named_tiles.escalator_2_concrete
escalatorx = named_tiles.escalator_1_concrete
gatey = named_tiles.front_gate
normaly = named_tiles.escalator_2

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
                    elev2x.T,
                    elev2x.T,
                    escalatorx.T,
                    normalx.T,
                    gatex.T,
                    gatex.T.R,
                    normalx.T.R,
                    escalatorx.T.R,
                    elev2x.T,
                    elev2x.T,
                    default,
                ],
                [track] + [platx.T] * 10 + [track],
                [track] * 12,
                [track] * 12,
                [track] + [platx] * 10 + [track],
                [
                    default,
                    elev2x,
                    elev2x,
                    escalatorx,
                    normalx,
                    gatex,
                    gatex.R,
                    normalx.R,
                    escalatorx.R,
                    elev2x,
                    elev2x,
                    default,
                ],
                [default] * 12,
            ],
            "Wuhubei (without shelters)",
            altitude=[[0] * 13] * 2 + [[1] * 13] + [[1] + [2] * 11 + [1]] * 3 + [[1] * 13] + [[0] * 13] * 2,
        ),
        Demo(
            [
                [default] * 12,
                [
                    default,
                    elev2x.T,
                    elev2x.T,
                    escalatorx.T,
                    normaly.T,
                    gatey.T,
                    gatey.T.R,
                    normaly.T.R,
                    escalatorx.T.R,
                    elev2x.T,
                    elev2x.T,
                    default,
                ],
                [track] + [platx.T] * 3 + [track] * 4 + [platx.T] * 3 + [track],
                [track] + [platx] * 3 + [track] * 4 + [platx] * 3 + [track],
                [
                    default,
                    elev2x,
                    elev2x,
                    escalatorx,
                    normaly,
                    gatey,
                    gatey.R,
                    normaly.R,
                    escalatorx.R,
                    elev2x,
                    elev2x,
                    default,
                ],
                [default] * 12,
            ],
            "Wuhubei (minimal platform)",
            altitude=[[0] * 13] * 2 + [[1] * 13] + [[1] + [2] * 11 + [1]] * 1 + [[1] * 13] + [[0] * 13] * 2,
        ),
        Demo(
            [
                [default] * 12,
                [
                    default,
                    elev1.T,
                    elev2.T,
                    escalatorx.T,
                    normalx.T,
                    gatex.T,
                    gatex.T.R,
                    normalx.T.R,
                    escalatorx.T.R,
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
