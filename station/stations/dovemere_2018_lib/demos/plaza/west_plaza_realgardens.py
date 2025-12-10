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
stair_end = stair_end
overpass = overpass
stair = stair_narrow
stair_extender = stair_extender_narrow
roadstops = [[stair_end, overpass, stair, stair_extender, stair.R, overpass, stair_end.R]]


# Objects
def real(x, y):
    return ALayout(AGroundSprite(image_sprite(f"third_party/realgardens/{x}.png", y=y)), [], True)


ground = real(315, 129)
crossroads = real(680, 129)
grassy = real(490, 185)
long_grassy = real(475, 143)
yard = real(576, 129)
path = real(560, 129)
pavilion_L = real(626, 157)
pavilion_R = real(624, 156)
thick_tee = real(203, 138)
tee_L = real(568, 208)
tee_R = real(570, 208)
big_tee = real(582, 188)
zig_L = real(648, 232)
zig_R = real(649, 197)
zag_L = real(647, 246)
zag_R = real(650, 240)
corner_L = real(640, 180)
corner_R = real(634, 253)
corner_TL = real(633, 240)
corner_TR = real(639, 253)
turn_L = real(585, 210)
turn_R = real(584, 241)


edge = real(615, 205)
edge_bottom = real(617, 241)


west_square = [
    [ground, grassy, thick_tee, thick_tee, thick_tee, grassy, ground],
    # [zag_L, edge_bottom, corner_TL, path, corner_TR, edge_bottom, zag_R],
    [corner_L, big_tee, zig_L, crossroads, zig_R, big_tee, corner_R],
    [pavilion_L, tee_L, grassy, path, grassy, tee_R, pavilion_R],
]


west_plaza_realgardens = Demo(
    station + roadstops + west_square,
    "West plaza (with RealGarden)",
    remap=get_1cc_remap(CompanyColour.GREEN),
    merge_bbox=True,
    climate="tropical",
    altitude=[[1] * 8] * 2 + [[0] * 8] * 5,
)
