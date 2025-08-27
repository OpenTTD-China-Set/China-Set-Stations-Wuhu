import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch

# FIXME
common_cb = {}
common_code = ""
from station.stations.dovemere_2018_lib.flexible_stations.common import (
    determine_platform_odd,
    determine_platform_even,
    make_demo,
    make_row,
    make_front_row,
    make_central_row,
)
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list
from .data import empty_tile, platform_tiles, two_side_tiles, concourse_tiles
from .registry import layouts


def fill_odd(d):
    return {**d, **{k + 1: v for k, v in d.items()}}


cb14 = {pclass: {} for pclass in platform_classes}
for pclass in platform_classes:
    for sclass in shelter_classes:
        p = platform_tiles["cns", pclass, "", sclass, "", ""]
        d = concourse_tiles[pclass, "d", sclass, "d"]
        cb14[pclass][sclass] = StationTileSwitch("T", fill_odd({0: empty_tile, 2: p, 4: p.T, 6: d}))

platform_templates = []

cb24_odd = make_vertical_switch(lambda t, d: {"e": 0, "n": 2, "f": 4, "c": 6}[determine_platform_odd(t, d)], cb24=True)
for p, pclass in enumerate(platform_classes):
    front = make_front_row((pclass, None, "platform"))
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24_odd, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cT"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24_odd: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        platform_templates.append(
            AStation(
                id=0x7F20 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cT",
                non_traversable_tiles=0b11000011,
                disabled_platforms=0b1,
                callbacks={
                    "select_tile_layout": cb24_odd.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )

cb24_even = make_vertical_switch(
    lambda t, d: {"e": 0, "n": 2, "f": 4, "c": 6}[determine_platform_even(t, d)], cb24=True
)
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24_even, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cT"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24_even: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        platform_templates.append(
            AStation(
                id=0x7F30 + p * 0x4 + s,
                translation_name="FLEXIBLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cT",
                non_traversable_tiles=0b11000011,
                disabled_platforms=0b1,
                callbacks={
                    "select_tile_layout": cb24_even.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass].to_index(layouts), purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )
