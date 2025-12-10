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
object_layouts.globalize()

col = [[cns], [default], [default], [default]]
station = h_merge([col, col, semitraversable.demo_1(5, 9)[5:], col, col], [[]] * 4)

# Objects
diagonal = west_plaza_diagonal
center_ground = west_plaza_center
offcenter_A = west_plaza_offcenter_A_corner_lawn_2
flower = west_plaza_topiary_2024a_half
offcenter_B = west_plaza_offcenter_B_decorated
edge = west_plaza_center_lawn
edge_2 = west_plaza_center_toilet_lawn
split_lawn = west_plaza_center_split_lawn

station += [
    [
        center_ground.M,
        edge.M,
        road_ground_turn_layout,
        stair_narrow,
        stair_extender_narrow,
        stair_narrow.R,
        road_ground_turn_layout.R,
        edge.T.M,
        center_ground.T.M,
    ],
    [
        diagonal.M,
        offcenter_A.R.M,
        edge,
        offcenter_A,
        center_ground,
        offcenter_A.R,
        edge.R,
        offcenter_A.T.R.M,
        diagonal.T.M,
    ],
    [diagonal.M, diagonal.M, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, diagonal.T.M, diagonal.T.M],
]


west_plaza_three_sides = Demo(
    station,
    "West plaza (three sides)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 10] * 4 + [[0] * 10] * 4,
)
