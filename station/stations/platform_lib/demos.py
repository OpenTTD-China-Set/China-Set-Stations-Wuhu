from station.lib import Demo
from station.stations.dovemere_2018_lib.west_plaza.grounds import named_layouts
from .data import platform_tiles, two_side_tiles, concourse_tiles, empty_concrete_tile


def repeat(layouts, n):
    return [row * n for row in layouts]


platform_tiles.globalize()
two_side_tiles.globalize()
concourse_tiles.globalize()

demos = [
    Demo(repeat([[cns_concrete], [concourse_concrete_d], [cns_concrete.T]], 3), "Platform"),
    Demo(
        repeat([[cns_concrete_shelter_1], [cns_concrete_shelter_1_d], [cns_concrete_shelter_1.T]], 3),
        "Platform with shelter",
    ),
    Demo(
        repeat([[empty_concrete_tile], [cns_concrete_covered], [cns_concrete_covered.T], [empty_concrete_tile]], 4),
        "Concrete grounds",
    ),
    Demo(repeat([[empty_concrete_tile]] * 4, 4), "Concrete grounds only"),
    Demo(
        repeat(
            [
                [named_layouts[("west_plaza", "center")]],
                [empty_concrete_tile],
                [empty_concrete_tile],
                [named_layouts[("west_plaza", "center")]],
            ],
            4,
        ),
        "With west square of Wuhu station",
    ),
]
