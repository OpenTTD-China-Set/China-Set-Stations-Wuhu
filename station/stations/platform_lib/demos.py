from station.lib import Demo
from .data import platform_tiles, two_side_tiles, concourse_tiles

platform_tiles.globalize()
two_side_tiles.globalize()
concourse_tiles.globalize()

demos = [
    Demo([[cns_concrete], [cns_concrete_d], [cns_concrete.T]], "Platform"),
    Demo([[cns_concrete_side], [cns_concrete_d], [cns_concrete_side.T]], "Platform with concrete grounds"),
    Demo([[cns_concrete_shelter_1], [cns_concrete_shelter_1_d], [cns_concrete_shelter_1.T]], "Platform with shelter"),
]
