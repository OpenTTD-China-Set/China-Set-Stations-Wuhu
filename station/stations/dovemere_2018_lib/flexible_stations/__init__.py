from .semitraversable import semitraversable_stations
from .traversable import traversable_stations
from .side import side_stations
from .side_third import side_third_stations
from .semitraversable_half import semitraversable_halfstations
from .traversable_half import traversable_halfstations
from .central import middle_stations

station_templates = (
    semitraversable_stations
    + traversable_stations
    + side_stations
    + side_third_stations
    + semitraversable_halfstations
    + traversable_halfstations
    + middle_stations
)
