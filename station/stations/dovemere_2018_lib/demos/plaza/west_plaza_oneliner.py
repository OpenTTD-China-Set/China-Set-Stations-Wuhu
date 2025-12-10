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

# Road Stops
roadstops = [[stair_end, overpass, stair_narrow, stair_extender_narrow, stair_narrow.R, overpass, stair_end.R]]

# Objects
center_ground = west_plaza_center
offcenter_ground_B = west_plaza_offcenter_B_oneliner
flower = west_plaza_topiary_2024a_half.T
trees = west_plaza_center_trees
west_square = [[center_ground, trees, offcenter_ground_B, flower, offcenter_ground_B.R, trees.R, center_ground]]


west_plaza_oneliner = Demo(
    station + roadstops + west_square,
    "West Plaza (7×1)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 8] * 2 + [[0] * 8] * 3,
)
