import grf
from station.lib import make_horizontal_switch, make_vertical_switch
from station.lib.templates.platforms import invert_platform
from ..layouts import named_tiles, layouts


def horizontal_layout(l, r, onetile, twotile, lwall, general, window, window_extender, threetile=None):
    threetile = threetile or twotile
    if l + r == 0:
        return onetile
    if l + r == 1:
        return [twotile, twotile.R][l]
    if l + r == 2:
        return [threetile, window_extender, threetile.R][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([lwall] + [general] * o + [window] + [window_extender] * c + [window.R] + [general] * o + [lwall.R])[l]


def make_row(onetile, twotile, lwall, general, window, window_extender, threetile=None):
    return make_horizontal_switch(
        lambda l, r: horizontal_layout(
            l, r, onetile, twotile, lwall, general, window, window_extender, threetile=threetile
        )
    )


def make_front_row(suffix):
    row = [
        named_tiles[(c, *suffix)]
        for c in ["v_end_gate", "corner_gate", "corner", "front_normal", "front_gate", "front_gate_extender"]
    ]
    row[1] = make_vertical_switch(lambda t, d: named_tiles[("corner_gate_2", *suffix)] if t == 1 else row[1])
    row[2] = make_vertical_switch(lambda t, d: named_tiles[("corner_2", *suffix)] if t == 1 else row[2])
    return make_row(*row)


def make_front_row_half(suffix):
    row = [
        named_tiles[(c, *suffix)]
        for c in ["v_end_gate", "corner_gate", "corner", "front_normal", "front_gate", "front_gate_extender"]
    ]
    row[1] = make_vertical_switch(lambda t, d: named_tiles[("corner_gate_2", *suffix)] if t == 0 else row[1])
    row[2] = make_vertical_switch(lambda t, d: named_tiles[("corner_2", *suffix)] if t == 0 else row[2])
    return make_row(*row)


def get_tile(name, desc):
    return named_tiles[(name, *desc)]


def reverse(x):
    if x is None:
        return None
    return x[:-1] + (invert_platform(x[-1]),)


def get_left_index_suffix(t, d, suffix):
    if d > t:
        return get_left_index_suffix(d, t, reverse(suffix)).T
    if t + d == 2:
        return get_tile("side_a2", suffix)
    if t + d == 3:
        return get_tile("side_a3", suffix)
    if t + d == 4:
        return [get_tile("side_a", suffix), get_tile("side_b2", suffix)][d - 1]
    if t == d:
        return get_tile("side_c", suffix)
    if d == 1:
        return get_tile("side_a", suffix)
    if d == 2:
        return get_tile("side_b", suffix)
    return get_tile("side_c", suffix)


def get_left_index_suffix_2(t, d, suffix):
    if t == d == 1:
        return get_tile("side_a2_windowed", suffix)
    if d == 1:
        return get_tile("side_a3_windowed", suffix)
    if t == 1:
        return get_tile("side_a3_windowed", reverse(suffix)).T
    return get_tile("side_d", suffix)


def make_central_row(l, r, suffix):
    return horizontal_layout(
        l,
        r,
        make_vertical_switch(lambda t, d: get_tile("v_central", suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix_2(t, d, suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix(t, d, suffix)),
        make_vertical_switch(lambda t, d: get_tile("central", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed_extender", suffix)),
    )


def get_left_index_suffix_near(t, d, suffix):
    if t == 0 and d == 1:
        return get_tile("side_a3", suffix)
    if d == 1:
        return get_tile("side_a", suffix)
    if d == 2:
        return get_tile("side_b", suffix)
    return get_tile("side_c", suffix)


def get_left_index_suffix_2_near(t, d, suffix):
    if d == 1:
        return get_tile("side_a3_windowed", suffix)
    return get_tile("side_d", suffix)


def make_central_row_near(l, r, suffix):
    return horizontal_layout(
        l,
        r,
        make_vertical_switch(lambda t, d: get_tile("v_central", suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix_2_near(t, d, suffix)),
        make_vertical_switch(lambda t, d: get_left_index_suffix_near(t, d, suffix)),
        make_vertical_switch(lambda t, d: get_tile("central", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed_extender", suffix)),
    )


def make_central_row_middle(l, r, suffix):
    return horizontal_layout(
        l,
        r,
        make_vertical_switch(lambda t, d: get_tile("v_central", suffix)),
        make_vertical_switch(lambda t, d: get_tile("side_d", suffix)),
        make_vertical_switch(lambda t, d: get_tile("side_c", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed", suffix)),
        make_vertical_switch(lambda t, d: get_tile("central_windowed_extender", suffix)),
    )
