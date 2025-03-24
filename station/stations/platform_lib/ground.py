from agrf.graphics.helpers.blend import blend_alternative_sprites
from agrf.graphics.helpers.map import map_alternative_sprites
from agrf.graphics.voxel import LazyVoxel
from station.lib import BuildingSymmetrical, BuildingSymmetricalX, AParentSprite
from ..ground import named_images as ground_images

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


def make_sprite(name, symmetry, joggle):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/cns",
        voxel_getter=lambda path=f"station/voxels/cns/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        subset=symmetry.render_indices(),
    )

    v.config["joggle"] = joggle

    sprite = symmetry.create_variants(v.spritesheet())
    return sprite


pillar_base = make_sprite("pillar_base", BuildingSymmetricalX, JOGGLE_AMOUNT * 2)
pillar_base_merged = pillar_base.symmetry_fmap(lambda y: blend_alternative_sprites(ground_images.gray, y))
fake_bridge = make_sprite("fake_bridge", BuildingSymmetrical, JOGGLE_AMOUNT)
fake_bridge_merged = fake_bridge.symmetry_fmap(lambda y: blend_alternative_sprites(ground_images.gray, y))
