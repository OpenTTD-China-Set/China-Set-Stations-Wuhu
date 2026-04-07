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

station = h_merge([[[cns], [default]], semitraversable.demo_1(5, 7)[5:], [[cns], [default]]], [[], []])

# Not-road-stops
not_roadstops = [
    [
        center,
        center_overpass_lawn,
        offcenter_A_overpass,
        center_staircase_3,
        offcenter_A_overpass.R,
        center_overpass_lawn.R,
        center,
    ]
]

# Objects
west_square = [
    [
        center_toilet_lawn.T,
        center_split_lawn,
        offcenter_B_decorated,
        topiary_2024a_half,
        offcenter_B_decorated.R,
        center_split_lawn.R,
        center_toilet_lawn.T.R,
    ]
]


west_plaza_roadless = Demo(
    station + not_roadstops + west_square,
    "West plaza (default, 7×2, no road)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 8] * 2 + [[0] * 8] * 3,
)
