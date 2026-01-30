from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all, concourse_tiles
from station.stations.misc import default
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

row_4 = h_merge([semitraversable.demo_1(i, 4) for i in range(1, 5)], [[concourse], [cns.T], [cns], [concourse.T]])
v_sep = [[concourse_tiles.none] * len(row_4[0])] * 2
row_5 = h_merge(
    [semitraversable.demo_1(i, 5) for i in range(1, 5)], [[concourse], [cns.T], [default], [cns], [concourse.T]]
)
row_6 = h_merge(
    [semitraversable.demo_1(i, 6) for i in range(1, 5)], [[concourse], [cns.T], [cns], [cns.T], [cns], [concourse.T]]
)
row_7 = h_merge(
    [semitraversable.demo_1(i, 7) for i in range(1, 5)],
    [[concourse], [cns.T], [cns], [concourse_d_d], [cns.T], [cns], [concourse.T]],
)

semi_auto_demo = Demo(
    row_4 + v_sep + row_5 + v_sep + row_6 + v_sep + row_7,
    "Station templates (untraversable fronts)",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
