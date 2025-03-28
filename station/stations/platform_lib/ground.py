from agrf.graphics.helpers.blend import blend_alternative_sprites
from agrf.graphics.helpers.map import map_alternative_sprites
from agrf.graphics.voxel import LazyVoxel
from station.lib import BuildingSymmetrical, BuildingSymmetricalX, AParentSprite, AGroundSprite
from station.lib.registers import Registers
from station.stations.empty import empty_sprite, empty_offset
from ..ground import named_images as ground_images
from agrf.lib.building.foundation import Foundation

JOGGLE_AMOUNT = 45 - 32 * 2**0.5


def create_huge_ground(sprite, scale, bpp):
    x1 = sprite.copy().move(-32 * scale, 16 * scale)
    x2 = sprite.copy().move(32 * scale, 16 * scale)
    x3 = sprite.copy().move(0, 32 * scale)
    sprite.blend_over(x1)
    sprite.blend_over(x2)
    sprite.blend_over(x3)
    return sprite


big_gray = ground_images.gray.symmetry_fmap(
    lambda y: map_alternative_sprites(y, create_huge_ground, "tiling", xofs=-32, yofs=-32)
)


def make_sprite(name, symmetry, joggle, width=16, childsprite=None):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/cns",
        voxel_getter=lambda path=f"station/voxels/cns/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        subset=symmetry.render_indices(),
    )

    v.config["joggle"] = joggle
    if childsprite is not None:
        v.config["agrf_relative_childsprite"] = childsprite

    sprite = symmetry.create_variants(v.spritesheet(xdiff=16 - width, xspan=width))
    return sprite


pillar = AParentSprite(make_sprite("pillar", BuildingSymmetricalX, JOGGLE_AMOUNT, width=5), (16, 5, 8), (0, 11, 0))

pillar_base = make_sprite("pillar_base", BuildingSymmetricalX, JOGGLE_AMOUNT * 2)
pillar_base_merged = pillar_base.symmetry_fmap(lambda y: Foundation(y, big_gray, False))
pillar_base_ground = pillar_base_merged.symmetry_fmap(lambda y: y.convert_foundation_to_ground())
pillar_base_underground = AParentSprite(pillar_base_ground, (16, 16, 0), (0, 0, 0), flags={"dodraw": Registers.NOSLOPE})
pillar_base_underground_gs = AGroundSprite(pillar_base_ground)

fake_bridge = make_sprite("fake_bridge", BuildingSymmetrical, JOGGLE_AMOUNT)
fake_bridge_merged = fake_bridge.symmetry_fmap(lambda y: Foundation(y, big_gray, False))

fake_bridge_2 = make_sprite("fake_bridge_2", BuildingSymmetrical, JOGGLE_AMOUNT * 2)
fake_bridge_merged_2 = fake_bridge_2.symmetry_fmap(lambda y: Foundation(y, big_gray, False, 8))
