from agrf.lib.building.slope import slope_types
from station.lib import ADefaultGroundSprite, ALayout
from station.lib.registers import Registers


def make_slope_variants(d):
    for v in d.values():
        v.slope_variants = d
    return d


track_ground = ADefaultGroundSprite(1012, flags={"add": Registers.CLIMATE_RAIL_OFFSET})
road_ground = ADefaultGroundSprite(1314)
road_ground_turn = ADefaultGroundSprite(1321)
road_ground_vanilla = ADefaultGroundSprite(1333)

default_ground_slope_variants = {
    x: ADefaultGroundSprite(3981 + x, flags={"add": Registers.CLIMATE_OFFSET}) for x in slope_types
}
default_ground = default_ground_slope_variants[0]
building_ground = ADefaultGroundSprite(1420, flags={"add": Registers.ZERO})

track = ALayout(track_ground, [], True)
default = make_slope_variants({k: ALayout(v, [], False) for k, v in default_ground_slope_variants.items()})[0]
building_ground_layout = ALayout(building_ground, [], False)
road_ground_layout = ALayout(road_ground, [], False)
road_ground_turn_layout = ALayout(road_ground_turn, [], False)
road_ground_vanilla_layout = ALayout(road_ground_vanilla, [], False)
