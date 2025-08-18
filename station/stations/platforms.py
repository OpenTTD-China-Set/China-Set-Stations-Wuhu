import grf
from station.lib import AStation, AMetaStation
from station.lib.parameters import parameter_list
from .ground import named_ps as ground_ps
from station.stations.platform_lib import (
    platform_tiles,
    two_side_tiles,
    concourse_tiles,
    entries,
    platform_ps,
    concourse_ps,
)
from station.stations.platform_lib.data import (
    platform_height,
    shelter_height,
    platform_width,
    platform_classes,
    shelter_classes,
)
from station.stations.platform_lib.demos import demos


station_tiles = []
for i, entry in enumerate(entries):
    enable_if = []
    for platform_class in ["concrete", "brick"]:
        if platform_class in entry.notes:
            enable_if.append(parameter_list[f"PLATFORM_{platform_class.upper()}"])
    for shelter_class in ["shelter_1", "shelter_2"]:
        if shelter_class in entry.notes:
            enable_if.append(parameter_list[f"SHELTER_{shelter_class.upper()}"])
    station_tiles.append(
        AStation(
            id=entry.id,
            translation_name=(
                "CONCOURSE"
                if "concourse" in entry.notes
                else "PLATFORM" if entry.traversable else "PLATFORM_UNTRAVERSABLE"
            ),
            layouts=(
                [entry, entry.M, entry.purchase, entry.purchase.M] if entry.purchase is not None else [entry, entry.M]
            ),
            class_label=entry.category,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={
                "select_tile_layout": 0,
                "select_sprite_layout": grf.DualCallback(default=0, purchase=2 if entry.purchase is not None else 0),
            },
            enable_if=enable_if,
            doc_layout=entry,
        )
    )

the_stations = AMetaStation(station_tiles, b"\xe8\x8a\x9cP", [b"\xe8\x8a\x9cP", b"\xe8\x8a\x9cp"], demos)
