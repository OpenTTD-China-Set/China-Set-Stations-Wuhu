from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from ..utils import h_merge

globalize_all(platform_class="brick", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize(group="west_plaza")

station = h_merge([[[cns], [default]], semitraversable.demo_1(5, 7)[5:], [[cns], [default]]], [[], []])

# Road Stops
roadstops = [[stair_end, overpass, stair_narrow, stair_extender_narrow, stair_narrow.R, overpass, stair_end.R]]

# Objects
west_square = [[center] * 7] * 3


west_plaza_toyland = Demo(
    station + roadstops + west_square,
    "West plaza (toyland)",
    remap=get_1cc_remap(CompanyColour.YELLOW),
    merge_bbox=True,
    climate="toyland",
    altitude=[[1] * 8] * 2 + [[0] * 8] * 3 + [[1, 0, 0, 1, 1, 0, 0, 1]] + [[1] * 8],
)
