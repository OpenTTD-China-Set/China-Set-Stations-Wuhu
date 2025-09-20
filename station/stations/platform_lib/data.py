from station.lib import (
    BuildingCylindrical,
    BuildingSymmetrical,
    BuildingSymmetricalX,
    BuildingFull,
    AParentSprite,
    AChildSprite,
    ALayout,
    Registers,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platform_lib import (
    PlatformFamily,
    register,
    platform_ps,
    concourse_ps,
    platform_tiles,
    two_side_tiles,
    concourse_tiles,
    make_entry,
)
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from ..ground import named_ps as ground_ps
from ..misc import default_ground


gray_ps = ground_ps.gray


platform_height = 4
platform_width = 5
shelter_height = 17
pillar_height = 18
YOFFSET = 0


class CNSPlatformFamily(PlatformFamily):
    def __init__(self):
        self.v = LazyVoxel(
            "cns",
            prefix=".cache/render/station/cns",
            voxel_getter=lambda path="station/voxels/cns/cns.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        self.concourse = LazyVoxel(
            "concourse",
            prefix=".cache/render/station/cns",
            voxel_getter=lambda path="station/voxels/cns/concourse.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        self.snow_sprites = {}

    @property
    def name(self):
        return "cns"

    def get_platform_classes(self):
        return ["concrete", "brick"]

    def get_shelter_classes(self):
        return ["shelter_1", "shelter_2"]

    def _get_snow_sprite(self, location, shelter_class):
        key = location + "_" + shelter_class
        if key in self.snow_sprites:
            return self.snow_sprites[key]

        if location in ["building"]:
            symmetry = BuildingFull
        else:
            symmetry = BuildingSymmetricalX

        s = shelter_class + ("_" if location != "" else "") + location
        skeeps = {s, s + "_snow"}
        v2 = self.v.keep_layers(tuple(skeeps), f"subset_{s}_snow_base")
        v3 = self.v.keep_layers((s + "_snow",), f"subset_{s}_snow_only")
        v = v3.compose(v2, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
        v.config["overlap"] = 1.3
        v.config["agrf_childsprite"] = (0, -YOFFSET)
        v.in_place_subset(symmetry.render_indices())
        s = symmetry.create_variants(v.spritesheet())
        self.snow_sprites[key] = AChildSprite(s, (0, 0), flags={"dodraw": Registers.SNOW})

        return self.snow_sprites[key]

    def get_sprite(self, location, rail_facing, platform_class, shelter_class):
        if platform_class == "":
            pkeeps = set()
        else:
            pkeeps = {platform_class + ("_side" if rail_facing == "side" else "")}
        if shelter_class == "":
            skeeps = set()
        else:
            if location == "building_narrow":
                skeeps = {shelter_class + "_building", "pillar_building"}
            elif location == "building_v_narrow":
                skeeps = {shelter_class + "_building_v"}
            else:
                skeeps = {shelter_class + ("_" if location != "" else "") + location}
                if platform_class != "" and shelter_class != "pillar":
                    if location == "building":
                        skeeps.add("escalator")
                    if location == "building_v":
                        skeeps.add("escalator_v")
                    if location == "building_noescalator":
                        skeeps.add("building")
                    if location == "building_v_noescalator":
                        skeeps.add("building_v")

        v2 = self.v.keep_layers(
            tuple(pkeeps) + tuple(skeeps), f"subset_{platform_class}_{rail_facing}_{shelter_class}_{location}"
        )
        v2.config["agrf_manual_crop"] = (0, YOFFSET)
        if location in ["building", "building_narrow"]:
            symmetry = BuildingFull
        else:
            symmetry = BuildingSymmetricalX
        v2.in_place_subset(symmetry.render_indices())
        foundation_height = platform_height if platform_class == "cut" else 0
        sprite = symmetry.create_variants(
            v2.spritesheet(xdiff=16 - platform_width, xspan=platform_width, zdiff=foundation_height)
        )

        height = max((platform_height if platform_class != "" else 0), (shelter_height if shelter_class != "" else 0))
        if shelter_class in ["shelter_1", "shelter_2"]:
            child_sprites = [self._get_snow_sprite(location.replace("_narrow", ""), shelter_class)]

            # XXX Temporarily disable snow sprites until WenSim adds them in CNS
            child_sprites = []
        else:
            child_sprites = []
        return AParentSprite(
            sprite,
            (16, platform_width, height - foundation_height),
            (0, 16 - platform_width, foundation_height),
            child_sprites=child_sprites,
        )

    def get_concourse_sprite(self, platform_class, side):
        if platform_class == "none":
            ckeeps = {"concourse"}
        elif side == "d":
            ckeeps = {"concourse", platform_class, platform_class + "_t"}
        else:
            ckeeps = {"concourse", platform_class}

        if platform_class == "none" or side == "d":
            symmetry = BuildingSymmetrical
        else:
            symmetry = BuildingSymmetricalX

        v2 = self.concourse.keep_layers(tuple(ckeeps), f"subset_{platform_class}_{side}")
        v2.in_place_subset(symmetry.render_indices())

        sprite = symmetry.create_variants(v2.spritesheet())
        return AParentSprite(sprite, (16, 16, platform_height), (0, 0, 0))


platform_classes = ["concrete", "brick"]
shelter_classes = ["shelter_1", "shelter_2"]


pf = CNSPlatformFamily()
register(pf)

platform_ps.populate()
concourse_ps.populate()
platform_tiles.populate()
two_side_tiles.populate()
concourse_tiles.populate()


empty_tile = make_entry(
    ALayout(default_ground, [], False, category=b"\xe8\x8a\x9cp", notes=["empty"]), BuildingCylindrical, 0x7FFF
)
