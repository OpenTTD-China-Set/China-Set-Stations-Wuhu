from station.lib import Demo
from .data import platform_tiles, two_side_tiles, concourse_tiles


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
]
