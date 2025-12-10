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

station = h_merge([[[cns], [default]], semitraversable.demo_1(4, 6)[4:], [[cns], [default]]], [[], []])

# Road Stops
roadstops = [[stair_end, overpass, stair_wide, stair_wide.R, overpass, stair_end.R]]

# Objects
center_ground = west_plaza_center
offcenter_A = west_plaza_offcenter_A_decorated
flower = west_plaza_topiary_2024a_half_horizontal
offcenter_B = west_plaza_offcenter_B_decorated
split_lawn = west_plaza_center_split_lawn
west_square = [
    [center_ground, offcenter_A, center_ground, center_ground, offcenter_A.R, center_ground],
    [split_lawn, offcenter_B, flower, center_ground, offcenter_B.R, split_lawn.R],
]


west_plaza_4 = Demo(
    station + roadstops + west_square,
    "West plaza (6×2)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 7] * 2 + [[0] * 7] * 4,
)
