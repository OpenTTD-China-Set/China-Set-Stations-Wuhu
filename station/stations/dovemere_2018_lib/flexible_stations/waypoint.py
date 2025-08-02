import grf
from station.lib import AStation, StationTileSwitch, make_vertical_switch, make_horizontal_switch
from .. import common_cb, common_code
from ..layouts import layouts
from .common import determine_platform_odd, determine_platform_even, make_demo, make_central_row_middle
from .traversable import cb24_odd, cb24_even, fill_odd
from station.stations.platforms import platform_classes, shelter_classes
from station.lib.parameters import parameter_list

cb14 = make_horizontal_switch(lambda l, r: make_central_row_middle(l, r, (None, None, "empty")))

waypoint_templates = []
demo = make_demo(cb14, 4, 1)
demo.category = b"\xe8\x8a\x9cc"
demo.notes.append("waypoint")
waypoint_templates.append(
    AStation(
        id=0xFFF0,
        translation_name="FLEXIBLE_CENTRAL_SIDE",
        layouts=layouts,
        class_label=b"\xe8\x8a\x9cA",
        callbacks={"select_sprite_layout": grf.DualCallback(default=cb14, purchase=layouts.index(demo)), **common_cb},
        make_foundation=True,
        extra_code=common_code,
        enable_if=[parameter_list["E88A9CA_ENABLE_TEMPLATE"]],
        doc_layout=demo,
        is_waypoint=True,
    )
)
