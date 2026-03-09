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
