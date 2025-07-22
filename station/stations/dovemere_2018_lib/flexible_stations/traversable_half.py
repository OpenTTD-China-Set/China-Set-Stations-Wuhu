import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from .. import common_cb, common_code
from ..layouts import named_tiles, layouts
from .common import (
    determine_platform_odd_bottom_half,
    determine_platform_odd_top_half,
    determine_platform_even_bottom_half,
    determine_platform_even_top_half,
    make_front_row_half,
    make_demo,
    make_row,
    make_central_row_near,
)
from .traversable import fill_odd, front2
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list


named_tiles.globalize()

front = {pclass: {} for pclass in platform_classes}
h_n = {pclass: {} for pclass in platform_classes}
h_f = {pclass: {} for pclass in platform_classes}
h_d = {pclass: {} for pclass in platform_classes}
cb14_2 = {pclass: {} for pclass in platform_classes}
cb14_4 = {pclass: {} for pclass in platform_classes}
cb14_6 = {pclass: {} for pclass in platform_classes}
for pclass in platform_classes:
    for sclass in shelter_classes:
        front[pclass][sclass] = make_front_row_half((pclass, sclass, "third_f"))

        h_n[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row_near(l, r, (pclass, sclass, "n")))
        h_f[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row_near(l, r, (pclass, sclass, "f")))
        h_d[pclass][sclass] = make_horizontal_switch(lambda l, r: make_central_row_near(l, r, (pclass, sclass, "d")))

        cb14_2[pclass][sclass] = make_vertical_switch(lambda t, d: (front2[pclass] if d == 0 else h_n[pclass][sclass]))
        cb14_4[pclass][sclass] = make_vertical_switch(
            lambda t, d: (front[pclass][sclass] if d == 0 else h_f[pclass][sclass])
        )
        cb14_6[pclass][sclass] = make_vertical_switch(
            lambda t, d: (front[pclass][sclass] if d == 0 else h_d[pclass][sclass])
        )


traversable_halfstations = []
cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd_bottom_half(t, d)], cb24=True)
cb24_top = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_odd_top_half(t, d)], cb24=True)

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        cb14 = StationTileSwitch(
            "T", fill_odd({2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )
        demo_layout = make_demo(cb14, 4, 4, cb24)
        demo_layout.category = b"\xe8\x8a\x9cf"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_halfstations.append(
            AStation(
                id=0xFE20 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE_NEAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cf",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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

        cb14 = cb14.T
        demo_layout = make_demo(cb14, 4, 4, cb24_top)
        demo_layout.category = b"\xe8\x8a\x9cb"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14, cb24=cb24_top: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_halfstations.append(
            AStation(
                id=0xFEA0 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE_FAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cb",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                callbacks={
                    "select_tile_layout": cb24_top.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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


front = make_front_row_half((None, None, ""))
cb24 = make_vertical_switch(lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even_bottom_half(t, d)], cb24=True)
cb24_top = make_vertical_switch(
    lambda t, d: {"n": 2, "f": 4, "d": 6}[determine_platform_even_top_half(t, d)], cb24=True
)
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        cb14 = StationTileSwitch(
            "T", fill_odd({0: front, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )
        demo_layout = make_demo(cb14, 4, 4, cb24)
        demo_layout.category = b"\xe8\x8a\x9cf"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_3 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_halfstations.append(
            AStation(
                id=0xFE30 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE_NEAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cf",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                callbacks={
                    "select_tile_layout": cb24.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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

        cb14 = cb14.T
        demo_layout = make_demo(cb14, 4, 4, cb24_top)
        demo_layout.category = b"\xe8\x8a\x9cb"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_4 = lambda r, c, cb14=cb14, cb24=cb24_top: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        traversable_halfstations.append(
            AStation(
                id=0xFEB0 + p * 0x4 + s,
                translation_name="FLEXIBLE_SIDE_FAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cb",
                cargo_threshold=40,
                non_traversable_tiles=0b11,
                callbacks={
                    "select_tile_layout": cb24_top.to_index(None),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14.to_index(layouts), purchase=layouts.index(demo_layout)
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
