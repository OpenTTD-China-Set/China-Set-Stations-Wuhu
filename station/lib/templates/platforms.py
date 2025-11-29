def invert_platform(platform):
    """Invert a platform identifier: f<->n, others unchanged."""
    return {"f": "n", "n": "f", "c": "c", "d": "d", "e": "e"}[platform]


def determine_platform_odd_top_half(t, d):
    return "nf"[t % 2]


def determine_platform_odd_bottom_half(t, d):
    return "fn"[d % 2]


def determine_platform_odd(t, d):
    if d > t:
        return invert_platform(determine_platform_odd(d, t))
    if t == 15 and 14 <= d <= 15:
        return "e"
    if (t + d) % 2 == 1:
        return "fn"[d % 2]
    if (t + d) % 4 == 0:
        if d < t:
            return "fn"[d % 2]
        return "e"
    if d < t:
        return "fn"[d % 2]
    return "c"


def determine_platform_even_top_half(t, d):
    return "fn"[t % 2]


def determine_platform_even_bottom_half(t, d):
    return "nf"[d % 2]


def determine_platform_even(t, d):
    if d == t == 0:
        return "e"
    if d > t:
        return invert_platform(determine_platform_even(d, t))
    if t == 15 and 15 <= d <= 15:
        return "e"
    if (t + d) % 2 == 1:
        return "nf"[d % 2]
    if (t + d) % 4 == 0:
        if d < t:
            return "nf"[d % 2]
        return "c"
    if d < t:
        return "nf"[d % 2]
    return "e"
