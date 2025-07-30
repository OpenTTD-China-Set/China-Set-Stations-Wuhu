import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from .. import common_cb, common_code
from ..layouts import layouts
from .common import determine_platform_odd, determine_platform_even, make_demo, make_central_row_middle
from .traversable import cb24_odd, cb24_even, fill_odd
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list

cb14_0 = make_horizontal_switch(lambda l, r: make_central_row_middle(l, r, (None, None, "e")))
cb14_2 = {pclass: {} for pclass in platform_classes}
cb14_4 = {pclass: {} for pclass in platform_classes}
cb14_6 = {pclass: {} for pclass in platform_classes}
cb14 = {pclass: {} for pclass in platform_classes}
for pclass in platform_classes:
    for sclass in shelter_classes:
        cb14_2[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row_middle(l, r, (pclass, sclass, "n"))
        )
        cb14_4[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row_middle(l, r, (pclass, sclass, "f"))
        )
        cb14_6[pclass][sclass] = make_horizontal_switch(
            lambda l, r: make_central_row_middle(l, r, (pclass, sclass, "c"))
        )
        cb14[pclass][sclass] = StationTileSwitch(
            "T", fill_odd({0: cb14_0, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass], 6: cb14_6[pclass][sclass]})
        )


middle_stations = []
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24_odd)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24_odd: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        middle_stations.append(
            AStation(
                id=0xFE80 + p * 0x4 + s,
                translation_name="FLEXIBLE_CENTRAL_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cc",
                non_traversable_tiles=0b11,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24_odd.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass], purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                make_foundation=True,
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )

for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24_even)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24_even: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")

        middle_stations.append(
            AStation(
                id=0xFE90 + p * 0x4 + s,
                translation_name="FLEXIBLE_CENTRAL_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cc",
                non_traversable_tiles=0b11,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24_even.to_index(),
                    "select_sprite_layout": grf.DualCallback(
                        default=cb14[pclass][sclass], purchase=layouts.index(demo_layout)
                    ),
                    **common_cb,
                },
                make_foundation=True,
                extra_code=common_code,
                enable_if=[
                    parameter_list["E88A9CA_ENABLE_TEMPLATE"],
                    parameter_list[f"PLATFORM_{pclass.upper()}"],
                    parameter_list[f"SHELTER_{sclass.upper()}"],
                ],
                doc_layout=demo_layout,
            )
        )
