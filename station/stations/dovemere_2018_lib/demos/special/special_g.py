from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_2cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="brick", shelter_class="shelter_2")

rail_near = [cns, v_central_n, cns, cns, cns, v_central_n, cns]
rail_far = [x.T for x in rail_near]
cns_c = concourse_d_d
rail_connector = [cns_c, v_central_c, cns_c, cns_c, cns_c, v_central_c, cns_c]
station = [
    h_end_asym_platform,
    tee_platform,
    h_gate_1_platform,
    h_gate_extender_1_platform,
    h_gate_1_platform.R,
    tee_platform,
    h_end_asym_platform.R,
]

special_demo_g = Demo(
    [[x.T for x in station], rail_far, rail_near, rail_connector, rail_far, rail_near, station],
    "Irregular 7×7 station layout",
    remap=get_2cc_remap(CompanyColour.YELLOW, CompanyColour.PALE_GREEN),
    climate="arctic",
)
