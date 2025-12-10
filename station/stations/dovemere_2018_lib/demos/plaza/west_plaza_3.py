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

station = h_merge([[[cns], [default]], semitraversable.demo_1(3, 6)[4:], [[cns], [default]]], [[], []])

# Road Stops
roadstops = [[stair_end, stair_narrow, stair_extender_narrow, stair_narrow.R, stair_end.R]]

# Objects
center_ground = west_plaza_center
offcenter_A = west_plaza_offcenter_A_decorated
flower = west_plaza_topiary_2024a_half
offcenter_B = west_plaza_offcenter_B
west_square = [
    [center_ground, offcenter_A, center_ground, offcenter_A.R, center_ground],
    [center_ground, offcenter_B, flower, offcenter_B.R, center_ground],
]


west_plaza_3 = Demo(
    station + roadstops + west_square,
    "West plaza (5×2)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 6] * 2 + [[0] * 6] * 4,
)
