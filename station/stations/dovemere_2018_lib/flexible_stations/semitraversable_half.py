import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch
from .. import common_cb, common_code
from ..layouts import named_tiles, layouts
from station.lib.templates.platforms import (
    determine_platform_odd_bottom_half,
    determine_platform_odd_top_half,
    determine_platform_even_bottom_half,
    determine_platform_even_top_half,
)
from station.lib.templates.demo import make_demo
from .common import make_front_row_half
from .traversable import fill_odd
from .traversable_half import cb14_2, cb14_4
from station.stations.platform_lib import platform_classes, shelter_classes
from station.lib.parameters import parameter_list


named_tiles.globalize()


semitraversable_halfstations = []
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        front = make_front_row_half((pclass, sclass, "platform"))
        cb24 = make_vertical_switch(
            lambda t, d: 0 if d == 0 else {"n": 2, "f": 4}[determine_platform_odd_bottom_half(t, d)], cb24=True
        )
        cb14 = StationTileSwitch("T", fill_odd({0: front, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass]}))
        demo_layout = make_demo(cb14, 4, 4, cb24, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cf"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_halfstations.append(
            AStation(
                id=0xFE00 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE_NEAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cf",
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

        cb14 = StationTileSwitch("T", fill_odd({0: front.T, 2: cb14_4[pclass][sclass].T, 4: cb14_2[pclass][sclass].T}))
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 else {"n": 2, "f": 4}[determine_platform_odd_top_half(t, d)], cb24=True
        )
        demo_layout = make_demo(cb14, 4, 4, cb24, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cb"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_halfstations.append(
            AStation(
                id=0xFE40 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE_FAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cb",
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


front = make_front_row_half((None, None, ""))
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        cb24 = make_vertical_switch(
            lambda t, d: 0 if d == 0 else {"n": 2, "f": 4}[determine_platform_even_bottom_half(t, d)], cb24=True
        )
        cb14 = StationTileSwitch("T", fill_odd({0: front, 2: cb14_2[pclass][sclass], 4: cb14_4[pclass][sclass]}))
        demo_layout = make_demo(cb14, 4, 4, cb24, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cf"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_3 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_halfstations.append(
            AStation(
                id=0xFE10 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE_NEAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cf",
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

        cb14 = StationTileSwitch("T", fill_odd({0: front.T, 2: cb14_4[pclass][sclass].T, 4: cb14_2[pclass][sclass].T}))
        cb24 = make_vertical_switch(
            lambda t, d: 0 if t == 0 else {"n": 2, "f": 4}[determine_platform_even_top_half(t, d)], cb24=True
        )
        demo_layout = make_demo(cb14, 4, 4, cb24, layouts=layouts)
        demo_layout.category = b"\xe8\x8a\x9cb"
        if pclass == "concrete" and sclass == "shelter_2":
            demo_4 = lambda r, c, cb14=cb14, cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_halfstations.append(
            AStation(
                id=0xFE50 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE_FAR",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cb",
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
