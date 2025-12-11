from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetricalY,
    BuildingSymmetrical,
    AParentSprite,
    ALayout,
    AChildSprite,
    AttrDict,
    Registers,
)
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from roadstop.lib import ARoadStop
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from ...misc import road_ground
from .roadstop_components import make_components, components
from ..roadstop_utils import named_layouts, make_road_stop, register_road_stop, named_parts

cnt = 0
WIDTH = 3
TOTAL_HEIGHT = 12
OVERPASS_HEIGHT = 11
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 9

JOGGLE_AMOUNT = 45 - 32 * 2**0.5


def make_road_stops():
    make_components()

    overpass = components[("road_stop", "overpass")]
    pillars = components[("road_stop", "pillars_with_bollards")]
    layout = ALayout(road_ground, [overpass, pillars], True, category=b"\xe8\x8a\x9cR")
    named_layouts[("overpass",)] = layout
    register_road_stop(layout, BuildingSymmetricalX, 0x8000)

    layout = ALayout(road_ground, [overpass, pillars, overpass.T, pillars.T], True, category=b"\xe8\x8a\x9c2")
    named_layouts[("double_overpass",)] = layout
    register_road_stop(layout, BuildingSymmetrical, 0x8002)

    overpass_bridge = components[("road_stop", "overpass_bridge_wide")]
    layout = ALayout(road_ground, [overpass_bridge, pillars, pillars.T], True, category=b"\xe8\x8a\x9c2")
    named_layouts[("overpass_bridge",)] = layout
    register_road_stop(layout, BuildingSymmetrical, 0x8003)

    overpass_bridge_half = components[("road_stop", "overpass_bridge_half")]
    layout = ALayout(road_ground, [overpass_bridge_half, pillars, pillars.T], True, category=b"\xe8\x8a\x9c2")
    named_layouts[("overpass_bridge_half",)] = layout
    register_road_stop(layout, BuildingSymmetricalY, 0x8004)

    overpass_bridge_narrow = components[("road_stop", "overpass_bridge_narrow")]
    layout = ALayout(road_ground, [overpass_bridge_narrow, pillars, pillars.T], True, category=b"\xe8\x8a\x9c2")
    named_layouts[("overpass_bridge_narrow",)] = layout
    register_road_stop(layout, BuildingSymmetrical, 0x8006)

    overpass_long = components[("road_stop", "overpass_long")]
    pillar_corner = components[("road_stop", "pillar_corner")]
    four_pillars = [
        pillar_corner.T.R,
        pillar_corner.T.R.move(4, 0),
        pillar_corner.T.R.move(8, 0),
        pillar_corner.T.R.move(12, 0),
    ]
    layout = ALayout(road_ground, [overpass_long, pillars] + four_pillars, True, category=b"\xe8\x8a\x9cR")
    named_layouts[("overpass_long",)] = layout
    register_road_stop(layout, BuildingSymmetricalX, 0x8007)

    overpass_long_narrow = components[("road_stop", "overpass_long_narrow")]
    layout = ALayout(road_ground, [overpass_long_narrow, pillars, pillar_corner.T.R], True, category=b"\xe8\x8a\x9cR")
    named_layouts[("stair_narrow",)] = layout
    register_road_stop(layout, BuildingFull, 0x8009)

    extender_onesided = components[("road_stop", "stair_extender_onesided")]
    overpass_half_stair = components[("road_stop", "overpass_half_stair")]
    entrance = components[("road_stop", "underground_entrance")]
    three_pillars = [pillar_corner.T.R, pillar_corner.T.R.move(4, 0), pillar_corner.T.R.move(8, 0)]
    layout = ALayout(
        road_ground,
        [overpass_half_stair, extender_onesided.move(-8, 8), pillars, entrance.move(4, 8, -16)] + three_pillars,
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_wide",)] = layout
    register_road_stop(layout, BuildingFull, 0x8104)

    layout = ALayout(
        road_ground,
        [overpass_half_stair, extender_onesided.move(-8, 8), pillars] + three_pillars,
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_wide_simple",)] = layout
    register_road_stop(layout, BuildingFull, 0x8108)

    extender = components[("road_stop", "stair_extender")]
    overpass_stair = components[("road_stop", "overpass_stair")]
    layout = ALayout(
        road_ground,
        [overpass_stair, extender.move(0, 8), extender.move(0, 8).R, pillars],
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_extender",)] = layout
    register_road_stop(layout, BuildingSymmetricalX, 0x8110)

    layout = ALayout(
        road_ground,
        [
            overpass_stair,
            extender_onesided.move(0, 8),
            extender_onesided.move(0, 8).R,
            pillars,
            entrance.move(12, 8, -16),
            entrance.R.move(-12, 8, -16),
        ],
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_extender_narrow",)] = layout
    register_road_stop(layout, BuildingSymmetricalX, 0x8112)

    layout = ALayout(
        road_ground,
        [overpass_stair, extender_onesided.move(0, 8), extender_onesided.move(0, 8).R, pillars],
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_extender_narrow_simple")] = layout
    register_road_stop(layout, BuildingSymmetricalX, 0x8114)

    layout = ALayout(
        road_ground,
        [overpass_stair, extender_onesided.move(0, 8), extender.move(0, 8).R, pillars, entrance.move(12, 8, -16)],
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_extender_onesided",)] = layout
    register_road_stop(layout, BuildingFull, 0x8118)

    layout = ALayout(
        road_ground,
        [overpass_stair, extender_onesided.move(0, 8), extender.move(0, 8).R, pillars],
        True,
        category=b"\xe8\x8a\x9cS",
    )
    named_layouts[("stair_extender_onesided_simple",)] = layout
    register_road_stop(layout, BuildingFull, 0x811C)

    make_road_stop(
        "stair_end",
        BuildingFull,
        0x8120,
        ((16, EXTENDED_WIDTH, TOTAL_HEIGHT), (0, WIDTH - EXTENDED_WIDTH, 0)),
        ((16, 16 - WIDTH * 2, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
        ((16, EXTENDED_WIDTH, TOTAL_HEIGHT), (0, 16 - WIDTH, 0)),
        True,
        16,
        joggle=JOGGLE_AMOUNT * 2,
        category=b"S",
    )
