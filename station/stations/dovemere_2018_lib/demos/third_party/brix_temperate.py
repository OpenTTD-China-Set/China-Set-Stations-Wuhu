from station.lib import Demo
from ..realistic.normal import normal_demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.layout import DefaultGraphics

for tile_id in [1011, 1012, 3981]:
    DefaultGraphics.register_third_party_image(f"third_party/brix/temperate/{tile_id}.png", "brix-temperate", tile_id)

brix_temperate_demo = Demo(
    normal_demo.tiles, "with BRIX temperate", remap=get_1cc_remap(CompanyColour.GREEN), climate="brix-temperate"
)
