from station.lib import Demo
from ..realistic.normal import normal_demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.layout import DefaultGraphics

for tile_id in [1011, 1012, 1037, 1038, 3981, 4550]:
    DefaultGraphics.register_third_party_image(f"third_party/brix/tropical/{tile_id}.png", "brix-tropical", tile_id)

brix_tropical_demo = Demo(
    normal_demo.tiles,
    "with BRIX tropical",
    remap=get_1cc_remap(CompanyColour.LIGHT_BLUE),
    climate="brix-tropical",
    subclimate="desert",
)
