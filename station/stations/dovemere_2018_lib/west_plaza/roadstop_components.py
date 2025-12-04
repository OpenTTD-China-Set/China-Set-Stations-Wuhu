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
    make_component("road_stop", "pillars", BuildingSymmetricalX, (16, 1, OVERPASS_HEIGHT), (0, 2, 0))
    make_component("road_stop", "pillars_with_bollards", BuildingSymmetricalX, (16, 1, OVERPASS_HEIGHT), (0, 2, 0))
    make_component("road_stop", "pillar_corner", BuildingSymmetricalX, (2, 1, OVERPASS_HEIGHT), (13, 2, 0))

    # Overpass layers
    make_component(
        "road_stop",
        "overpass",
        BuildingSymmetricalX,
        (16, 4, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_solid",
        BuildingSymmetricalX,
        (16, 4, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_entrance",
        BuildingSymmetricalX,
        (16, 4, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "platform",
        BuildingSymmetricalX,
        (16, 4, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_bridge_wide",
        BuildingSymmetrical,
        (16, 16, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_bridge_narrow",
        BuildingSymmetrical,
        (16, 16, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_bridge_half",
        BuildingSymmetricalY,
        (16, 16, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_long",
        BuildingSymmetricalX,
        (16, 14, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_long_narrow",
        BuildingFull,
        (16, 14, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_half_stair",
        BuildingFull,
        (16, 14, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )
    make_component(
        "road_stop",
        "overpass_stair",
        BuildingSymmetricalX,
        (16, 14, TOTAL_HEIGHT - OVERPASS_HEIGHT),
        (0, 0, OVERPASS_HEIGHT),
        joggle=JOGGLE_AMOUNT,
    )

    # Stairs
    make_component("road_stop", "stair_extender", BuildingFull, (8, 8, TOTAL_HEIGHT), (8, 6, 0), joggle=JOGGLE_AMOUNT)
    make_component("road_stop", "stair_extender_low", BuildingFull, (8, 8, PLATFORM_HEIGHT), (8, 6, 0), joggle=0)
    make_component(
        "road_stop", "stair_extender_onesided", BuildingFull, (8, 8, TOTAL_HEIGHT), (8, 6, 0), joggle=JOGGLE_AMOUNT
    )
    make_component(
        "road_stop", "stair_extender_onesided_low", BuildingFull, (8, 8, PLATFORM_HEIGHT), (8, 6, 0), joggle=0
    )

    # Underground Entrance
    make_component("road_stop", "underground_entrance", BuildingFull, (11, 8, 0), (0, 6, 16), joggle=JOGGLE_AMOUNT * 3)

    # Objects only
    make_component("road_stop", "overpass_low", BuildingSymmetricalX, (16, 4, PLATFORM_HEIGHT), (0, 0, 0), joggle=0)
