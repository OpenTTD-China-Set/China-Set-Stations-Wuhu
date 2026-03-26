from dataclasses import dataclass
import functools
import grf
from station.lib.foundation_switch import FoundationSwitch
from agrf.lib.building.layout import ALayout
from agrf.lib.building.foundation import Foundation


@dataclass
class Action2Pool:
    max_id: int = 1
    foundation_to_id: dict = None
    foundations: list = None
    id_to_action2: dict = None

    def __post_init__(self):
        if self.foundation_to_id is None:
            self.foundation_to_id = {}
        if self.foundations is None:
            self.foundations = []
        if self.id_to_action2 is None:
            self.id_to_action2 = {}

    def get_foundation_id(self, foundation):
        if foundation in self.foundation_to_id:
            return self.foundation_to_id[foundation]
        self.foundation_to_id[foundation] = self.max_id
        self.foundations.append(foundation.make_foundations())
        self.id_to_action2[self.max_id] = grf.GenericSpriteLayout(
            ent1=[self.max_id], ent2=[self.max_id], feature=grf.STATION
        )
        self.max_id += 1
        return self.foundation_to_id[foundation]

    def get_action_2(self, foundation):
        if isinstance(foundation, grf.Switch):
            return foundation.fmap(lambda x: self.get_action_2(x))
        elif not isinstance(foundation, Foundation):
            return self.get_action_2(foundation.to_switch())
        cur_id = self.get_foundation_id(foundation)
        return self.id_to_action2[cur_id]

    def get_action_2_zero(self):
        if 0 not in self.id_to_action2:
            self.id_to_action2[0] = grf.GenericSpriteLayout(ent1=[0], ent2=[0], feature=grf.STATION)
        return self.id_to_action2[0]

    def export(self):
        ret = []
        if self.max_id > 1:
            for i, f in enumerate(self.foundations):
                ret.append(grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(f), first_set=i + 1))
                ret.extend(f)
        return ret

    def __hash__(self):
        return id(self)

    @functools.cache
    def map_foundation_switch(self, s):
        if isinstance(s, Foundation):
            return self.get_action_2(s)
        return s.fmap(lambda x: self.map_foundation_switch(x))

    @functools.cache
    def map_switch(self, s):
        if isinstance(s, ALayout):
            if s.foundation is s.M.foundation:
                return self.get_action_2(s.foundation)
            return grf.Switch(
                ranges={1: self.get_action_2(s.M.foundation)},
                code="extra_callback_info2 % 2",
                default=self.get_action_2(s.foundation),
            )
        return s.fmap(lambda x: self.map_switch(x))
