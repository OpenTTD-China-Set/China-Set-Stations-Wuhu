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

station = h_merge([[[cns], [default]], semitraversable.demo_1(1, 7)[5:], [[cns], [default]]], [[], []])

# Road Stops
roadstops = [[stair_end, overpass, stair_end.R]]

# Objects
west_square = [[center, center, center], [center, topiary_2024a_half, center]]


west_plaza_one_tile = Demo(
    station + roadstops + west_square,
    "West plaza (3×2)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
    altitude=[[1] * 4] * 2 + [[0] * 4] * 4,
)
