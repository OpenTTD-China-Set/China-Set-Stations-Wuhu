from station.lib import Demo
from ..realistic.normal import normal_demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.layout import DefaultGraphics

for tile_id in [1037, 1038, 4550]:
    DefaultGraphics.register_third_party_image(f"third_party/brix/arctic/{tile_id}.png", "brix-arctic", tile_id)

brix_arctic_demo = Demo(
    normal_demo.tiles,
    "with BRIX arctic",
    remap=get_1cc_remap(CompanyColour.BROWN),
    climate="brix-arctic",
    subclimate="snow",
)
