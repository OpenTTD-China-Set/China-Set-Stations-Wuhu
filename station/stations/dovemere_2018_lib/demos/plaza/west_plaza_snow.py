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

# Road Stops
roadstops = [[stair_end, overpass, stair_narrow, stair_extender_narrow, stair_narrow.R, overpass, stair_end.R]]

# Objects
west_square = [
    [
        center_lawn_edge,
        center_lawn,
        offcenter_A_decorated_lawn,
        center,
        offcenter_A_decorated_lawn.R,
        center_lawn.R,
        center_lawn_edge.R,
    ],
    [
        center_toilet_lawn.T,
        center_split_lawn,
        offcenter_B_decorated,
        topiary_2024a_half,
        offcenter_B_decorated.R,
        center_split_lawn.R,
        center_toilet_lawn.T.R,
    ],
]


west_plaza_snow = Demo(
    station + roadstops + west_square,
    "West plaza (snow)",
    remap=get_1cc_remap(CompanyColour.PINK),
    merge_bbox=True,
    climate="arctic",
    subclimate="snow",
    altitude=[[1] * 8] * 2 + [[0] * 8] * 4,
)
