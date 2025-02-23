from station.lib import BuildingSymmetricalX
from ..objects_utils import named_layouts, register, templates


def make_templates():
    named_layouts.populate()

    center_ground = named_layouts.west_plaza_center
    offcenter_A = named_layouts.west_plaza_offcenter_A_decorated_lawn
    flower = named_layouts.west_plaza_topiary_2024a_half
    offcenter_B = named_layouts.west_plaza_offcenter_B_decorated
    edge = named_layouts.west_plaza_center_lawn
    edge_2 = named_layouts.west_plaza_center_toilet_lawn
    split_lawn = named_layouts.west_plaza_center_split_lawn
    west_square = [
        [center_ground, edge, offcenter_A, center_ground, offcenter_A.R, edge.R, center_ground],
        [edge_2.T, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, edge_2.T.R],
    ]
    register(
        west_square,
        BuildingSymmetricalX,
        b"T",
        starting_id=0x0F00,
        purchase_layout=center_ground,
        destination=templates,
    )
