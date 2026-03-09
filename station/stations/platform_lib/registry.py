from station.lib import AttrDict, ALayout, BuildingSymmetricalX, BuildingSymmetrical, BuildingCylindrical
from abc import ABC, abstractmethod
from ..misc import track_ground, building_ground, default_ground
from ..ground import ground_ps, ground_gs
from .aux import add_buffer_stop

gray_ps = ground_gs.gray

platform_ps = AttrDict(schema=("name", "platform_clas", "rail_facing", "shelter_class", "location"))
concourse_ps = AttrDict(schema=("platform_class", "side"))
platform_tiles = AttrDict(
    schema=("name", "platform_class", "rail_facing", "shelter_class", "location", "shelter_side", "concrete_covering")
)
waypoint_tiles = AttrDict(schema=("name", "north", "south"))
two_side_tiles = AttrDict(
    schema=(
        "name",
        "platform_class",
        "rail_facing",
        "shelter_class",
        "separator",
        "platform_class_2",
        "rail_facing_2",
        "shelter_class_2",
    )
)
concourse_tiles = AttrDict(prefix="concourse", schema=("platform_class", "side", "shelter_class", "shelter_side"))
layouts = []
entries = []


def make_entry(layout, symmetry, base_id):
    var = symmetry.get_all_variants(layout)
    l = symmetry.create_variants(var)
    if l.traversable:
        l = add_buffer_stop(l)
    layouts.extend(symmetry.get_all_variants(l))

    if symmetry is BuildingCylindrical:
        # FIXME: the problem here is that we should not use `get_all_variants` at all
        # The real answer would be `get_all_entries` plus their mirror versions
        # But this would require a synchronized change across all metastations
        # Which is left for future refactors
        layouts.extend(symmetry.get_all_variants(l))

    if base_id is not None:
        for i, entry in enumerate(symmetry.get_all_entries(l)):
            entry.id = base_id + i
            entries.append(entry)
    return l


class PlatformFamily(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def get_platform_classes(self):
        pass

    @abstractmethod
    def get_shelter_classes(self):
        pass

    @abstractmethod
    def get_sprite(self, location, rail_facing, platform_class, shelter_class):
        pass

    @abstractmethod
    def get_concourse_sprite(self, location, rail_facing, platform_class, shelter_class):
        pass


def register(pf: PlatformFamily):
    platform_classes = pf.get_platform_classes()
    shelter_classes = pf.get_shelter_classes()
    name = pf.name

    def make_notes(platform_class, shelter_class="", shelter_class_2=""):
        notes = []
        if platform_class in platform_classes:
            notes.append(platform_class)
        if shelter_class in shelter_classes:
            notes.append(shelter_class)
        if shelter_class_2 in shelter_classes:
            notes.append(shelter_class_2)
        return notes

    # Part I: platforms with rails

    for pid, platform_class in enumerate(["np", "cut"] + platform_classes):
        for sid, shelter_class in enumerate(["", "pillar"] + shelter_classes):
            if (platform_class, shelter_class) == ("np", ""):
                # Don't create the "nothing" tile
                continue

            if platform_class in ["np", "cut"]:
                rail_facings = [""]
            else:
                rail_facings = ["", "side"]

            if shelter_class == "":
                locations = [""]
            elif shelter_class == "pillar":
                locations = ["", "building", "central"]
            else:
                locations = ["", "building", "building_narrow", "building_v", "building_v_narrow"]

            for lid, location in enumerate(locations):
                for rid, rail_facing in enumerate(rail_facings):
                    ps = pf.get_sprite(location, rail_facing, platform_class, shelter_class)
                    platform_ps[(name, platform_class, rail_facing, shelter_class, location)] = ps

                    for cid, (concrete_cover, cdesc) in enumerate([([], ""), ([ground_ps.gray_third.T], "covered")]):
                        for ssid, (l, make_symmetrical, shelter_side) in enumerate(
                            [([ps], False, ""), ([ps, ps.T], True, "d")]
                        ):
                            if ssid == 1 and cid == 1:
                                make_symmetrical = False
                                try:
                                    shelterless_ps = platform_ps[(name, platform_class, rail_facing, "", location)]
                                except:
                                    continue
                                if shelter_class == "":
                                    continue
                                concrete_cover = []
                                l = [ps, shelterless_ps.T]

                            if make_symmetrical:
                                cur_symmetry = ps.sprite.symmetry.add_y_symmetry()
                            else:
                                cur_symmetry = ps.sprite.symmetry

                            if platform_class not in ["np", "cut"] and shelter_class != "pillar" and location == "":
                                my_id = (
                                    0x7000 + (pid - 2) * 0x200 + sid * 0x40 + (rid % 2) * 0x20 + ssid * 0x10 + cid * 0x2
                                )
                            else:
                                my_id = None

                            platform_tiles[
                                (name, platform_class, rail_facing, shelter_class, location, shelter_side, cdesc)
                            ] = make_entry(
                                ALayout(
                                    track_ground,
                                    l + concrete_cover,
                                    True,
                                    category=(b"\xe8\x8a\x9cP"),
                                    notes=make_notes(platform_class, shelter_class),
                                ),
                                cur_symmetry,
                                my_id,
                            )

    # Part II: asymmetrical platforms with rails

    for pid, platform_class in enumerate(platform_classes):
        for rid, rail_facing in enumerate(["", "side"]):
            for rid2, rail_facing_2 in enumerate(["", "side"]):
                for sid, shelter_class in enumerate([""] + shelter_classes):
                    for sid2, shelter_class_2 in enumerate([""] if shelter_class == "" else ["", shelter_class]):
                        if (rail_facing, shelter_class) < (rail_facing_2, shelter_class_2):
                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            cur_symmetry = BuildingSymmetricalX

                            var = cur_symmetry.get_all_variants(
                                ALayout(
                                    track_ground,
                                    [platform_ps[(name, *suffix, "")], platform_ps[(name, *suffix2, "")].T],
                                    True,
                                    category=b"\xe8\x8a\x9cP",
                                    notes=make_notes(platform_class, shelter_class, shelter_class_2),
                                )
                            )
                            l = cur_symmetry.create_variants(var)
                            l = add_buffer_stop(l)

                            for i, entry in enumerate(cur_symmetry.get_all_entries(l)):
                                entry.id = 0x7800 + pid * 0x80 + rid * 0x40 + rid2 * 0x20 + sid * 0x4 + sid2 * 0x2 + i
                                entries.append(entry)

                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            two_side_tiles[(name, *suffix, "and", *suffix2)] = l
                            two_side_tiles[(name, *suffix2, "and", *suffix)] = l.T

    # Part III: full platforms without rails

    for pid, platform_class in enumerate(["none"] + platform_classes):
        for ssid, side in enumerate(["", "d"] if platform_class != "none" else [""]):
            ps = pf.get_concourse_sprite(platform_class, side)
            concourse_ps[(platform_class, side)] = ps

            if platform_class == "none" or side == "d":
                symmetry = BuildingSymmetrical
            else:
                symmetry = BuildingSymmetricalX

            var = symmetry.get_all_variants(
                ALayout(
                    gray_ps, [ps], False, category=b"\xe8\x8a\x9cp", notes=["concourse"] + make_notes(platform_class)
                )
            )
            l = symmetry.create_variants(var)
            for i, entry in enumerate(symmetry.get_all_entries(l)):
                entry.id = 0x7A00 + pid * 0x4 + ssid * 0x2 + i
                entries.append(entry)
            concourse_tiles[(platform_class, side, "", None)] = l

            if platform_class != "none":
                for sid, shelter_class in enumerate(shelter_classes):
                    shelter = platform_ps[(name, "cut", "", shelter_class, "")]
                    for lid, (l, needs_symmetrical, shelter_side) in enumerate(
                        [([shelter], False, ""), ([shelter, shelter.T], True, "d")]
                    ):
                        if needs_symmetrical:
                            if side == "d":
                                cur_sym = symmetry
                            else:
                                continue
                        else:
                            cur_sym = BuildingSymmetricalX

                        concourse_tiles[(platform_class, side, shelter_class, shelter_side)] = make_entry(
                            ALayout(
                                gray_ps,
                                l + [ps],
                                False,
                                category=b"\xe8\x8a\x9cp",
                                notes=["concourse"] + make_notes(platform_class, shelter_class),
                            ),
                            cur_sym,
                            0x7B00 + pid * 0x20 + ssid * 0x10 + sid * 0x4 + lid * 0x2,
                        )

    # Part IV: platforms without rails

    for pid, platform_class in enumerate(platform_classes):
        for sid, shelter_class in enumerate(["", "pillar"] + shelter_classes):
            rail_facings = ["solid"]

            if shelter_class == "":
                locations = [""]
            elif shelter_class == "pillar":
                locations = ["", "building", "central"]
            else:
                locations = ["", "building", "building_narrow", "building_v", "building_v_narrow"]

            for lid, location in enumerate(locations):
                for rid, rail_facing in enumerate(rail_facings):
                    ps = pf.get_sprite(location, rail_facing, platform_class, shelter_class)
                    platform_ps[(name, platform_class, rail_facing, shelter_class, location)] = ps

                    for cid, (solid_ground, cdesc) in enumerate(
                        [(default_ground, "grass"), (gray_ps, "concrete"), (building_ground, "")]
                    ):
                        for ssid, (l, make_symmetrical, shelter_side) in enumerate(
                            [([ps], False, ""), ([ps, ps.T], True, "d")]
                        ):
                            if make_symmetrical:
                                cur_symmetry = ps.sprite.symmetry.add_y_symmetry()
                            else:
                                cur_symmetry = ps.sprite.symmetry

                            if platform_class not in ["np", "cut"] and shelter_class != "pillar" and location == "":
                                my_id = 0x7C00 + cid * 0x80 + pid * 0x20 + ssid * 0x10 + sid * 0x4
                            else:
                                my_id = None

                            platform_tiles[
                                (name, platform_class, rail_facing, shelter_class, location, shelter_side, cdesc)
                            ] = make_entry(
                                ALayout(
                                    solid_ground,
                                    l,
                                    False,
                                    category=(
                                        b"\xe8\x8a\x9cZ"
                                        if cid == 1
                                        else b"\xe8\x8a\x9cr" if cid == 2 else b"\xe8\x8a\x9cz"
                                    ),
                                    notes=make_notes(platform_class, shelter_class),
                                ),
                                cur_symmetry,
                                my_id,
                            )

    # Part V: waypoints
    make_entry(
        ALayout(track_ground, [], True, category=b"\xe8\x8a\x9cQ", notes=["waypoint"]), BuildingSymmetrical, 0x7110
    )
    make_entry(
        ALayout(track_ground, [ground_ps.gray_third], True, category=b"\xe8\x8a\x9cQ", notes=["waypoint"]),
        BuildingSymmetricalX,
        0x7111,
    )
    make_entry(
        ALayout(
            track_ground,
            [ground_ps.gray_third, ground_ps.gray_third.T],
            True,
            category=b"\xe8\x8a\x9cQ",
            notes=["waypoint"],
        ),
        BuildingSymmetrical,
        0x7113,
    )
