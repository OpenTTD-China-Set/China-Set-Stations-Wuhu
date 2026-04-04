import inspect
from agrf.graphics.palette import company_colour_remap


def get_1cc_remap(colour):
    return company_colour_remap(colour, colour).to_sprite()


def get_2cc_remap(colour1, colour2):
    return company_colour_remap(colour1, colour2).to_sprite()


class AttrDict(dict):
    def __init__(self, *args, prefix=None, schema=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self._prefix = prefix
        self._schema = schema
        self._index = None

    @staticmethod
    def __tuple_to_str(t):
        return "_".join(a for a in t if a is not None and a != "")

    def __contains__(self, item):
        if super().__contains__(item):
            return True
        if isinstance(item, tuple):
            for k, v in self._index[item[0]].items():
                if all((a is None or b is None or a == b) for a, b in zip(k, item)):
                    return True
        return False

    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        if isinstance(item, tuple):
            for k, v in self._index[item[0]].items():
                if all((a is None or b is None or a == b) for a, b in zip(k, item)):
                    return v
        raise KeyError(item)

    def populate(self):
        self._index = {}
        for k, v in list(self.items()):
            if isinstance(k, tuple):
                str_key = self.__tuple_to_str(k)
                assert str_key not in self, f"populate() conflict! {str_key}"
                self[str_key] = v

                if k[0] not in self._index:
                    self._index[k[0]] = {}
                self._index[k[0]][k] = v

    def globalize(self, caller_globals=None, **kwargs):
        if caller_globals is None:
            caller_globals = inspect.currentframe().f_back.f_globals

        for k, v in self.items():
            if isinstance(k, str) and len(kwargs) == 0:
                caller_globals[k] = v
            elif isinstance(k, tuple):
                if all((a is None or kwargs.get(b) is None or a == kwargs.get(b)) for a, b in zip(k, self._schema)):
                    new_key = self.__tuple_to_str(
                        [self._prefix] + [a for a, b in zip(k, self._schema) if kwargs.get(b) is None]
                    )
                    assert new_key not in caller_globals, new_key
                    caller_globals[new_key] = v
