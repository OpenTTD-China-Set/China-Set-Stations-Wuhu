from station.lib import BuildingFull, BuildingSymmetricalX, BuildingSymmetricalY, BuildingSymmetrical, AttrDict
from .components import make_component as original_make_component

WIDTH = 3
TOTAL_HEIGHT = 12
PLATFORM_HEIGHT = 3
OVERPASS_HEIGHT = 11
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 9

JOGGLE_AMOUNT = 45 - 32 * 2**0.5

components = AttrDict(schema=("type", "name"))
make_component = lambda *args, **kwargs: original_make_component(*args, **kwargs, components=components)


def make_components():
    # Pillars
    make_component("road_stop", "pillars_with_bollards", BuildingSymmetricalX, (16, 1, OVERPASS_HEIGHT), (0, 2, 0))

    # Overpass layers
    make_component(
        "road_stop",
        "overpass",
        BuildingSymmetricalX,
        (16, 4, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
