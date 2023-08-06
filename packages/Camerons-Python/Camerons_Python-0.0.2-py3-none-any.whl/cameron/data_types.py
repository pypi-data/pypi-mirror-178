import json

__all__ = ["AttrDict"]


class AttrDict:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, key):
        return self.get(key)

    @classmethod
    def transform_output(cls, data):
        if isinstance(data, dict):
            return cls(data)
        elif isinstance(data, list):
            return [cls.transform_output(val) for val in data]
        else:
            return data

    def keys(self):
        return self._data.keys()

    def get(self, *args):
        return self.transform_output(self._data.get(*args))

    def __getitem__(self, key):
        return self.get(key)

    def items(self):
        for key, val in self._data.items():
            yield key, self.transform_output(val)

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._data)

    def __str__(self):
        return str(self._data)

    @classmethod
    def json_load(cls, filename):
        with open(filename) as f:
            return cls.transform_output(json.load(f))

    @classmethod
    def json_loads(cls, json_data):
        return cls.transform_output(json.loads(f))
