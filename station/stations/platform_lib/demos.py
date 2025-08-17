from station.lib import Demo
from .data import platform_tiles, two_side_tiles, concourse_tiles


def repeat(layouts, n):
    return [row * n for row in layouts]


platform_tiles.globalize()
two_side_tiles.globalize()
concourse_tiles.globalize()

plat = platform_tiles.cns_concrete_supported2_shelter_2.enable_foundation(9)
plat_T = platform_tiles.cns_concrete_supported2_shelter_2.T.enable_foundation(6)
plat2 = platform_tiles.cns_concrete_elevated2_shelter_2.T.lower_tile().enable_foundation(9)
plat2_T = platform_tiles.cns_concrete_elevated2_shelter_2.lower_tile().enable_foundation(6)
from station.stations.misc import sloped_track, track

sloped_track_foundation = sloped_track.lower_tile().add_default_foundation(72)
sloped_track_foundation_R = sloped_track.R.lower_tile().add_default_foundation(66)
sloped_track = sloped_track.lower_tile()

demos = {
    "Platforms": [
        Demo(repeat([[cns_concrete], [concourse_concrete_d], [cns_concrete.T]], 3), "Platform"),
        Demo(
            repeat([[cns_concrete_shelter_1], [cns_concrete_shelter_1_d], [cns_concrete_shelter_1.T]], 3),
            "Platform with shelter",
        ),
    ],
    "Lowered Grounds": [
        Demo(
            [
                [sloped_track] + [plat_T] * 10 + [sloped_track.R],
                [sloped_track] + [track] * 10 + [sloped_track.R],
                [sloped_track] + [track] * 10 + [sloped_track.R],
                [sloped_track_foundation] + [plat] * 10 + [sloped_track_foundation_R],
            ],
            "Test",
        ),
        Demo([[plat2_T]], "Test 2"),
        Demo([[plat]], "Test 3"),
        Demo([[plat2]], "Test 4"),
    ],
}
