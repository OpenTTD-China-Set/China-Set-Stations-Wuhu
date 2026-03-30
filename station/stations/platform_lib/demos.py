from station.lib import Demo
from station.stations.dovemere_2018_lib.west_plaza.grounds import named_layouts
from .data import platform_tiles, two_side_tiles, concourse_tiles, empty_concrete_tile
from station.stations.misc import track, default


def repeat(layouts, n):
    return [row * n for row in layouts]


platform_tiles.globalize()
two_side_tiles.globalize()
concourse_tiles.globalize()

plat = platform_tiles.cns_concrete_supported2_shelter_2
plat1 = platform_tiles.cns_concrete_elevated_shelter_2.T
plat2 = platform_tiles.cns_concrete_elevated2_shelter_2.T

demos = {
    "Platforms": [
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
    ],
    "Lowered Grounds": [
        Demo(
            [
                [default] + [plat1.T] * 2 + [default],
                [track] + [plat.T] * 2 + [track],
                [track] + [plat] * 2 + [track],
                [default] + [plat1] * 2 + [default],
            ],
            "Test 1",
            altitude=[[0] * 5] * 2 + [[0, 1, 1, 1, 0]] + [[0] * 5] * 2,
        ),
        Demo(
            [
                [default] + [plat2.T] * 2 + [default],
                [track] + [plat.T] * 2 + [track],
                [track] + [plat] * 2 + [track],
                [default] + [plat2] * 2 + [default],
            ],
            "Test 2",
            altitude=[[0] * 5] + [[1] * 5] + [[1, 2, 2, 2, 1]] + [[1] * 5] + [[0] * 5],
        ),
        Demo([[default, plat2.T, default]], "Elevated 2, Slope 6", altitude=[[0, 0, 0, 0], [1, 1, 1, 1]]),
        Demo([[default, plat2.T, default]], "Elevated 2, Slope 10", altitude=[[0, 0, 1, 1], [1, 1, 0, 0]]),
        Demo([[default, plat2.T, default]], "Elevated 2, Slope 7", altitude=[[1, 1, 0, 0], [1, 1, 1, 1]]),
        Demo([[default, plat2.T, default]], "Elevated 2, Slope 14", altitude=[[0, 0, 1, 1], [1, 1, 1, 1]]),
        Demo([[default, plat2, default]], "Elevated 2, Slope 9", altitude=[[1, 1, 1, 1], [0, 0, 0, 0]]),
        Demo([[default, plat2, default]], "Elevated 2, Slope 5", altitude=[[1, 1, 0, 0], [0, 0, 1, 1]]),
        Demo([[default, plat2, default]], "Elevated 2, Slope 13", altitude=[[1, 1, 1, 1], [0, 0, 1, 1]]),
        Demo([[default, plat2, default]], "Elevated 2, Slope 11", altitude=[[1, 1, 1, 1], [1, 1, 0, 0]]),
        Demo([[default], [plat2.T.M], [default]], "Elevated 2, Slope 3", altitude=[[1, 0]] * 4),
        Demo([[default], [plat2.M], [default]], "Elevated 2, Slope 12", altitude=[[0, 1]] * 4),
        Demo([[default, plat, default]], "Supported 2, Slope 9", altitude=[[1, 1, 1, 1], [0, 0, 0, 0]]),
    ],
}
