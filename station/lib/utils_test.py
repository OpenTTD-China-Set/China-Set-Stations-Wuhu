import pytest

from station.lib.utils import get_1cc_remap, class_label_printable, AttrDict


def test_class_label_printable_basic():
    # 'A' (0x41), NUL (0x00 -> '0'), space (0x20)
    data = b"A\x00 "
    assert class_label_printable(data) == "A0 "


def test_class_label_printable_mixed_controls_and_printables():
    # ESC (0x1B -> '1B'), DEL (0x7F -> '\x7f' by chr), space, 'A'
    data = bytes([0x1B, 0x7F, 0x20, 0x41])
    expected = "1B" + "\x7f" + " " + "A"
    assert class_label_printable(data) == expected


def test_attrdict_attribute_and_item_access():
    ad = AttrDict({"alpha": 1})
    # attribute access
    assert ad.alpha == 1
    # adding via attribute reflects in dict
    ad.beta = 2
    assert "beta" in ad
    assert ad["beta"] == 2


def test_attrdict_populate_and_contains_getitem_with_tuples():
    ad = AttrDict({("foo", "bar"): "v", ("foo", None): "w"}, prefix="pre", schema=["s1", "s2"])

    ad.populate()

    # populate should create string keys from tuple keys
    assert "foo_bar" in ad
    assert ad["foo_bar"] == "v"
    assert "foo" in ad
    assert ad["foo"] == "w"

    # tuple membership and retrieval via partial tuple
    assert ("foo", None) in ad
    assert ("foo", "bar") in ad

    # Direct tuple key access returns its exact value
    assert ad[("foo", None)] == "w"

    # Partial tuple lookup through index (not a direct key)
    assert ad[("foo", "baz")] == "w"

    # missing keys should raise
    with pytest.raises(KeyError):
        _ = ad[("bar", "baz")]


def test_attrdict_globalize_basic_and_filtered_keys():
    ad = AttrDict({("foo", "bar"): 42, "X": 9}, prefix="pre", schema=["s1", "s2"])

    # When kwargs empty, string keys are exported and tuple keys expand fully
    g: dict = {}
    ad.globalize(caller_globals=g)
    assert g["X"] == 9
    assert g["pre_foo_bar"] == 42

    # When kwargs provided, string keys are not exported; tuple keys are filtered
    g2: dict = {}
    ad.globalize(caller_globals=g2, s1=None, s2="bar")
    assert "X" not in g2
    assert g2 == {"pre_foo": 42}

    # Mismatch should result in no export when there is no wildcard (None) value in tuples
    g3: dict = {}
    ad.globalize(caller_globals=g3, s2="baz")
    assert g3 == {}

    # Conflict should raise AssertionError
    g4: dict = {"pre_foo_bar": 0}
    with pytest.raises(AssertionError):
        ad.globalize(caller_globals=g4)


def test_get_1cc_remap_smoke():
    # Smoke test: function executes and returns a value
    result = get_1cc_remap(0)
    assert result is not None
