import grf
from station.lib import AStation, make_vertical_switch
from .. import common_cb, common_code
from ..layouts import layouts
from station.lib.templates.platforms import determine_platform_odd, determine_platform_even
from station.lib.templates.demo import make_demo
from .traversable import cb14
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list


semitraversable_stations = []
for p, pclass in enumerate(platform_classes):
    for s, sclass in enumerate(shelter_classes):
        cb24 = make_vertical_switch(
            lambda t, d: (6 if t == 0 or d == 0 else {"e": 0, "n": 2, "f": 4, "c": 6}[determine_platform_odd(t, d)]),
            cb24=True,
        )
        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24, layouts=layouts)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_1 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")
        semitraversable_stations.append(
            AStation(
                id=0xFF00 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                non_traversable_tiles=0b11000011,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
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
        cb24 = make_vertical_switch(
            lambda t, d: (0 if t == 0 or d == 0 else {"e": 0, "n": 2, "f": 4, "c": 6}[determine_platform_even(t, d)]),
            cb24=True,
        )

        demo_layout = make_demo(cb14[pclass][sclass], 4, 4, cb24, layouts=layouts)
        if pclass == "concrete" and sclass == "shelter_2":
            demo_2 = lambda r, c, cb14=cb14[pclass][sclass], cb24=cb24: cb14.demo(r, c, cb24)
        else:
            demo_layout.notes.append("noshow")

        semitraversable_stations.append(
            AStation(
                id=0xFF10 + p * 0x4 + s,
                translation_name="FLEXIBLE_UNTRAVERSABLE_NO_SIDE",
                layouts=layouts,
                class_label=b"\xe8\x8a\x9cA",
                non_traversable_tiles=0b11000011,
                disabled_platforms=0b111,
                callbacks={
                    "select_tile_layout": cb24.to_index(),
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
