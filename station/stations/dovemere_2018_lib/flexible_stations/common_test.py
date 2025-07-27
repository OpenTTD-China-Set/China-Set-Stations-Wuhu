from station.stations.dovemere_2018_lib.flexible_stations.common import (
    determine_platform_odd,
    determine_platform_odd_top_half,
    determine_platform_odd_bottom_half,
    determine_platform_even,
    determine_platform_even_top_half,
    determine_platform_even_bottom_half,
    get_left_index_suffix,
    named_tiles,
)


def check_platform_function(fn, n, expected):
    assert expected == "".join(fn(min(t, 15), min(n - 1 - t, 15)) for t in range(n))


def test_determine_platform_odd():
    check_platform_function(determine_platform_odd, 7, "nfncfnf")
    check_platform_function(determine_platform_odd, 8, "nfnfnfnf")
    check_platform_function(determine_platform_odd, 9, "nfnfenfnf")
    check_platform_function(determine_platform_odd, 10, "nfnfnfnfnf")


def test_determine_platform_odd_huge():
    check_platform_function(determine_platform_odd, 29, "nf" * 6 + "nfenf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 30, "nf" * 6 + "nfeenf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 31, "nf" * 6 + "nfeeenf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 32, "nf" * 6 + "nfeeeenf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 33, "nf" * 6 + "nfeeeeenf" + "nf" * 6)


def test_determine_platform_odd_top_half():
    check_platform_function(determine_platform_odd_top_half, 7, "nfnfnfn")
    check_platform_function(determine_platform_odd_top_half, 8, "nfnfnfnf")
    check_platform_function(determine_platform_odd_top_half, 9, "nfnfnfnfn")
    check_platform_function(determine_platform_odd_top_half, 10, "nfnfnfnfnf")


def test_determine_platform_odd_top_half_huge():
    check_platform_function(determine_platform_odd_top_half, 15, "nf" * 7 + "n")
    check_platform_function(determine_platform_odd_top_half, 16, "nf" * 8)


def test_determine_platform_odd_bottom_half():
    check_platform_function(determine_platform_odd_bottom_half, 7, "fnfnfnf")
    check_platform_function(determine_platform_odd_bottom_half, 8, "nfnfnfnf")
    check_platform_function(determine_platform_odd_bottom_half, 9, "fnfnfnfnf")
    check_platform_function(determine_platform_odd_bottom_half, 10, "nfnfnfnfnf")


def test_determine_platform_odd_bottom_half_huge():
    check_platform_function(determine_platform_odd_bottom_half, 15, "f" + "nf" * 7)
    check_platform_function(determine_platform_odd_bottom_half, 16, "nf" * 8)


def test_determine_platform_even():
    check_platform_function(determine_platform_even, 7, "fnfenfn")
    check_platform_function(determine_platform_even, 8, "fnfnfnfn")
    check_platform_function(determine_platform_even, 9, "fnfncfnfn")
    check_platform_function(determine_platform_even, 10, "fnfnfnfnfn")


def test_determine_platform_even_huge():
    check_platform_function(determine_platform_even, 29, "fn" * 7 + "c" + "fn" * 7)
    check_platform_function(determine_platform_even, 30, "fn" * 7 + "fn" + "fn" * 7)
    check_platform_function(determine_platform_even, 31, "fn" * 7 + "fen" + "fn" * 7)
    check_platform_function(determine_platform_even, 32, "fn" * 7 + "feen" + "fn" * 7)
    check_platform_function(determine_platform_even, 33, "fn" * 7 + "feeen" + "fn" * 7)


def test_determine_platform_even_top_half():
    check_platform_function(determine_platform_even_top_half, 7, "fnfnfnf")
    check_platform_function(determine_platform_even_top_half, 8, "fnfnfnfn")
    check_platform_function(determine_platform_even_top_half, 9, "fnfnfnfnf")
    check_platform_function(determine_platform_even_top_half, 10, "fnfnfnfnfn")


def test_determine_platform_even_top_half_huge():
    check_platform_function(determine_platform_even_top_half, 15, "fn" * 7 + "f")
    check_platform_function(determine_platform_even_top_half, 16, "fn" * 8)


def test_determine_platform_even_bottom_half():
    check_platform_function(determine_platform_even_bottom_half, 7, "nfnfnfn")
    check_platform_function(determine_platform_even_bottom_half, 8, "fnfnfnfn")
    check_platform_function(determine_platform_even_bottom_half, 9, "nfnfnfnfn")
    check_platform_function(determine_platform_even_bottom_half, 10, "fnfnfnfnfn")


def test_determine_platform_even_bottom_half_huge():
    check_platform_function(determine_platform_even_bottom_half, 15, "n" + "fn" * 7)
    check_platform_function(determine_platform_even_bottom_half, 16, "fn" * 8)


def test_get_left_index_suffix():
    f = ("concrete", "shelter_1", "f")
    n = ("concrete", "shelter_1", "n")

    assert named_tiles.side_a_concrete_shelter_1_f is get_left_index_suffix(3, 1, f)
    assert named_tiles.side_b2_concrete_shelter_1_n.T is get_left_index_suffix(2, 2, f)
    assert named_tiles.side_a_concrete_shelter_1_n.T is get_left_index_suffix(1, 3, f)

    assert named_tiles.side_a_concrete_shelter_1_n is get_left_index_suffix(4, 1, n)
    assert named_tiles.side_b_concrete_shelter_1_n is get_left_index_suffix(3, 2, n)
    assert named_tiles.side_b_concrete_shelter_1_f.T is get_left_index_suffix(2, 3, n)
    assert named_tiles.side_a_concrete_shelter_1_f.T is get_left_index_suffix(1, 4, n)
