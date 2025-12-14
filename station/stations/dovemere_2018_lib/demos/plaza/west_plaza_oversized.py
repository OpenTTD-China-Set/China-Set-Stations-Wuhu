from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize(group="west_plaza")

station = h_merge([[[cns], [default]], semitraversable.demo_1(14, 22)[20:], [[cns], [default]]], [[], []])

# Road Stops
roadstops = [
    [stair_end]
    + [overpass] * 4
    + [stair_narrow, stair_extender_onesided]
    + [stair_extender] * 2
    + [stair_extender_onesided.R, stair_narrow.R]
    + [overpass] * 4
    + [stair_end.R]
]

# Objects
west_square = [
    [center]
    + [center_lawn_edge] * 4
    + [offcenter_A_decorated_lawn, center, center, center, center, offcenter_A_decorated_lawn.R]
    + [center_lawn_edge] * 4
    + [center],
    [center] * 4
    + [
        center_tree_formation,
        offcenter_A_lightposts,
        center,
        center,
        center,
        center,
        offcenter_A_lightposts.R,
        center_tree_formation.R,
    ]
    + [center] * 4,
    [center] * 4
    + [
        center_tree_formation,
        offcenter_A_lightposts,
        center,
        topiary_2024a_corner,
        center,
        center,
        offcenter_A_lightposts.R,
        center_tree_formation.R,
    ]
    + [center] * 4,
    [center_lawn_edge.T] * 4
    + [
        center_split_lawn,
        offcenter_B_decorated,
        center,
        center,
        center,
        center,
        offcenter_B_decorated.R,
        center_split_lawn.R,
    ]
    + [center_lawn_edge.T] * 4,
]


west_plaza_oversized = Demo(
    station + roadstops + west_square,
    "West plaza (16×4)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 17] * 2 + [[0] * 17] * 6,
)
