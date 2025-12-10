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
object_layouts.globalize()

station = h_merge([[[cns], [default]], semitraversable.demo_1(14, 22)[20:], [[cns], [default]]], [[], []])

# Road Stops
stair_end = stair_end
overpass = overpass
stair = stair_narrow
stair_extender = stair_extender
stair_extender_onesided = stair_extender_onesided
roadstops = [
    [stair_end]
    + [overpass] * 4
    + [stair, stair_extender_onesided]
    + [stair_extender] * 2
    + [stair_extender_onesided.R, stair.R]
    + [overpass] * 4
    + [stair_end.R]
]

# Objects
center_ground = west_plaza_center
offcenter_A = west_plaza_offcenter_A_decorated_lawn
lightposts = west_plaza_offcenter_A_lightposts
flower = west_plaza_topiary_2024a_corner
offcenter_B = west_plaza_offcenter_B_decorated
edge = west_plaza_center_lawn_edge
trees = west_plaza_center_tree_formation
split_lawn = west_plaza_center_split_lawn
west_square = [
    [center_ground]
    + [edge] * 4
    + [offcenter_A, center_ground, center_ground, center_ground, center_ground, offcenter_A.R]
    + [edge] * 4
    + [center_ground],
    [center_ground] * 4
    + [trees, lightposts, center_ground, center_ground, center_ground, center_ground, lightposts.R, trees]
    + [center_ground] * 4,
    [center_ground] * 4
    + [trees, lightposts, center_ground, flower, center_ground, center_ground, lightposts.R, trees]
    + [center_ground] * 4,
    [edge.T] * 4
    + [split_lawn, offcenter_B, center_ground, center_ground, center_ground, center_ground, offcenter_B.R, split_lawn.R]
    + [edge.T] * 4,
]


west_plaza_oversized = Demo(
    station + roadstops + west_square,
    "West plaza (16×4)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 17] * 2 + [[0] * 17] * 6,
)
