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

station = h_merge([[[cns], [default]], semitraversable.demo_1(5, 7)[5:], [[cns], [default]]], [[], []])

# Not-road-stops
center_ground = west_plaza_center
overpass = west_plaza_center_overpass_low
staircase = west_plaza_center_staircase_low_3
not_roadstops = [[center_ground, overpass, overpass, staircase, overpass, overpass, center_ground]]

# Objects
offcenter_A = west_plaza_offcenter_A_decorated_lawn
flower = west_plaza_topiary_2024a_half
offcenter_B = west_plaza_offcenter_B_decorated
edge = west_plaza_center_lawn
edge_2 = west_plaza_center_toilet_lawn
split_lawn = west_plaza_center_split_lawn
west_square = [
    [center_ground, edge, offcenter_A, center_ground, offcenter_A.R, edge.R, center_ground],
    [edge_2.T, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, edge_2.T.R],
]


west_plaza_slopeless = Demo(
    station + not_roadstops + west_square,
    "West plaza (default, 7×2, no slope)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)
