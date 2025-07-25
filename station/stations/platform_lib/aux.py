from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from station.lib import AttrDict, AParentSprite, AChildSprite, BuildingFull, Registers
from agrf.graphics.voxel import LazyVoxel

aux_ps = AttrDict(schema=("name",))

v = LazyVoxel(
    "bufferstop",
    prefix=".cache/render/station/cns",
    voxel_getter=lambda path="station/voxels/cns/bufferstop.vox": path,
    load_from="station/files/cns-gorender.json",
)
symmetry = BuildingFull
nosnow = v.discard_layers(("snow",), "nosnow")
snow = v.keep_layers(("snow",), "snow")
snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
snow.config["overlap"] = 1.3

nosnow.in_place_subset(symmetry.render_indices())
nosnow.config["agrf_manual_crop"] = (0, 20)
nosnow_sprite = symmetry.create_variants(nosnow.spritesheet(xspan=6, xdiff=10, yspan=6, ydiff=5))

snow.in_place_subset(symmetry.render_indices())
snow.config["agrf_childsprite"] = (0, -20)
snow_sprite = symmetry.create_variants(snow.spritesheet(xspan=6, xdiff=10, yspan=6, ydiff=5))

ps = AParentSprite(nosnow_sprite, (6, 6, 4), (5, 10, 0)).M.R
# No snow for now XD
# cs = AChildSprite(snow_sprite, (0, 0), flags={"dodraw": Registers.SNOW}).M.R

aux_ps[("bufferstop",)] = bufferstop = ps  # + cs

bufferstop_sw = bufferstop.R.copy()
bufferstop_sw.flags = {"dodraw": Registers.RAIL_CONTINUATION_S}
bufferstop_ne = bufferstop.copy()
bufferstop_ne.flags = {"dodraw": Registers.RAIL_CONTINUATION_N}
bufferstop_se = bufferstop.R.M.copy()
bufferstop_se.flags = {"dodraw": Registers.RAIL_CONTINUATION_S}
bufferstop_nw = bufferstop.M.copy()
bufferstop_nw.flags = {"dodraw": Registers.RAIL_CONTINUATION_N}


def add_buffer_stop_single_purchase(l):
    if l.ground_sprite.sprite.sprite_id == 1012:
        ret = l + bufferstop.R + bufferstop
    elif l.ground_sprite.sprite.sprite_id == 1011:
        ret = l + bufferstop.R.M + bufferstop.M
    else:
        assert False, l

    return ret


def add_buffer_stop_single(l):
    if l.ground_sprite.sprite.sprite_id == 1012:
        ret = l + bufferstop_sw + bufferstop_ne
    elif l.ground_sprite.sprite.sprite_id == 1011:
        ret = l + bufferstop_se + bufferstop_nw
    else:
        assert False, l

    return ret


def add_buffer_stop(l):
    sym = l.symmetry
    new_l = l.symmetry_fmap(add_buffer_stop_single)
    new_l_purchase = l.symmetry_fmap(add_buffer_stop_single_purchase)

    for l, l_purchase in zip(sym.get_all_variants(new_l), sym.get_all_variants(new_l_purchase)):
        l.purchase = l_purchase

    return new_l
