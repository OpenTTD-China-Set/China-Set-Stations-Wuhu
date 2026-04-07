from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import road_ground_turn_layout, default
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize(group="west_plaza")

col = [[cns], [default], [default], [default]]
station = h_merge([col, col, semitraversable.demo_1(5, 9)[5:], col, col], [[]] * 4)

# Objects
station += [
    [
        center.M,
        center_lawn.M,
        road_ground_turn_layout,
        stair_narrow,
        stair_extender_narrow,
        stair_narrow.R,
        road_ground_turn_layout.R,
        center_lawn.T.M,
        center.T.M,
    ],
    [
        diagonal.M,
        offcenter_A_corner_lawn_2.R.M,
        center_lawn,
        offcenter_A_corner_lawn_2,
        center,
        offcenter_A_corner_lawn_2.R,
        center_lawn.R,
        offcenter_A_corner_lawn_2.T.R.M,
        diagonal.T.M,
    ],
    [
        diagonal.M,
        diagonal.M,
        center_split_lawn,
        offcenter_B_decorated,
        topiary_2024a_half,
        offcenter_B_decorated.R,
        center_split_lawn.R,
        diagonal.T.M,
        diagonal.T.M,
    ],
]


west_plaza_three_sides = Demo(
    station,
    "West plaza (three sides)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 10] * 2 + [[0] * 2 + [1] * 6 + [0] * 2] * 2 + [[0] * 10] * 4,
)
