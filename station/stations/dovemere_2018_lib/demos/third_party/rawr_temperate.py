from station.lib import Demo
from ..realistic.normal import normal_demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.layout import DefaultGraphics

for tile_id in [1011, 1012, 3981]:
    DefaultGraphics.register_third_party_image(f"third_party/rawr/temperate/{tile_id}.png", "rawr-temperate", tile_id)

rawr_temperate_demo = Demo(
    normal_demo.tiles, "with RAWR temperate", remap=get_1cc_remap(CompanyColour.GREY), climate="rawr-temperate"
)
