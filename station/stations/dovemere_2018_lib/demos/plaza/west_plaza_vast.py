from station.lib import Demo, AGroundSprite, ALayout
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.image_sprite import image_sprite
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
def vast(x):
    return ALayout(AGroundSprite(image_sprite(f"third_party/vast/vast_{x}.png")), [], True)


ground = vast(26)
symbol = vast(47)
grassy = vast(70)
west_square = [
    [ground, grassy, ground, ground, ground, grassy, ground],
    [grassy, grassy, ground, symbol, ground, grassy, grassy],
    [grassy, ground, ground, ground, ground, ground, grassy],
]


west_plaza_vast = Demo(
    station + roadstops + west_square,
    "West plaza (with VAST Objects tiles)",
    remap=get_1cc_remap(CompanyColour.MAUVE),
    merge_bbox=True,
    altitude=[[1] * 8] * 2 + [[0] * 8] * 5,
)
