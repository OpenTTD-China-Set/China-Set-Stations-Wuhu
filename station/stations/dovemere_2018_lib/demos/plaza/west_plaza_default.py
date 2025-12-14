from station.lib import Demo, AParentSprite
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default, building_ground_layout, road_ground_vanilla_layout
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize()

station = h_merge([[[cns], [default]], semitraversable.demo_1(5, 7)[5:], [[cns], [default]]], [[], []])

# Road Stops
overpass = overpass
road = road_ground_vanilla_layout
roadstops = [[road] + [overpass] * 5 + [road]]

# Objects
building_ground_layout = building_ground_layout
west_square = [[building_ground_layout] * 7, [building_ground_layout] * 7]


west_plaza_default = Demo(
    station + roadstops + west_square,
    "West plaza (vanilla ground)",
    remap=get_1cc_remap(CompanyColour.BLUE),
    merge_bbox=True,
    altitude=[[1] * 8] * 2 + [[0] * 8] * 4,
)
