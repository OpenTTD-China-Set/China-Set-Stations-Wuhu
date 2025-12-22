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
from station.stations.platform_lib.templates import platform_templates


station_tiles = []
for i, entry in enumerate(entries):
    enable_if = []
    for platform_class in ["concrete", "brick"]:
        if platform_class in entry.notes:
            enable_if.append(parameter_list[f"PLATFORM_{platform_class.upper()}"])
    for shelter_class in ["shelter_1", "shelter_2"]:
        if shelter_class in entry.notes:
            enable_if.append(parameter_list[f"SHELTER_{shelter_class.upper()}"])

    if "concourse" in entry.notes:
        translation_name = "CONCOURSE"
    elif "empty" in entry.notes:
        translation_name = "EMPTY"
    elif "empty pit" in entry.notes:
        translation_name = "SUNKEN"
    elif "empty pit 2" in entry.notes:
        translation_name = "SUNKEN_2"
    elif entry.traversable:
        translation_name = "PLATFORM"
    else:
        translation_name = "PLATFORM_UNTRAVERSABLE"

    if entry.purchase is not None:
        if "pit" in entry.notes:
            new_entry = entry.foundation.add_to_layout(entry)
            new_entry_M = entry.foundation.M.add_to_layout(entry.M)

            layouts = [entry.purchase, entry.purchase.M, new_entry.default, new_entry_M.default]
            for x, y in zip(new_entry._ranges, new_entry_M._ranges):
                layouts.append(x.ref)
                layouts.append(y.ref)
            sprite_layout = grf.DualCallback(default=new_entry.to_index(layouts), purchase=2)
            make_foundation = False
            foundation_object = entry.foundation
        else:
            layouts = [entry, entry.M, entry.purchase, entry.purchase.M]
            sprite_layout = grf.DualCallback(default=entry, purchase=2)
            make_foundation = entry.foundation is not None
            foundation_object = None
    else:
        layouts = [entry, entry.M]
        sprite_layout = grf.DualCallback(default=entry, purchase=0)
        make_foundation = entry.foundation is not None
        foundation_object = None

    station_tiles.append(
        AStation(
            id=entry.id,
            translation_name=translation_name,
            layouts=layouts,
            class_label=entry.category,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={
                "select_tile_layout": 0,
                **({"select_sprite_layout": sprite_layout} if entry.foundation is not None else {}),
            },
            make_foundation=make_foundation,
            foundation_object=foundation_object,
            enable_if=enable_if,
            doc_layout=entry,
            general_flags=0b10000 if "extended" in entry.notes else 0,
        )
    )

the_stations = AMetaStation(
    platform_templates + station_tiles,
    b"\xe8\x8a\x9cP",
    [
        b"\xe8\x8a\x9cT",
        b"\xe8\x8a\x9cP",
        b"\xe8\x8a\x9cp",
        b"\xe8\x8a\x9cL",
        b"\xe8\x8a\x9cl",
        b"\xe8\x8a\x9cE",
        b"\xe8\x8a\x9ce",
        b"\xe8\x8a\x9cU",
    ],
    demos,
)
