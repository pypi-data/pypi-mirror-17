from six import with_metaclass


class EnumAttr(object):
    def __init__(self, parent, name, index, value):
        self.parent = parent
        self.name = name
        self.index = index
        self.value = value

    def __eq__(self, other):
        if isinstance(other, EnumAttr):
            return (self.parent == other.parent) and (self.index == other.index)

        return self.value == other

    def __cmp__(self, other):
        if isinstance(other, EnumAttr):
            return self.index - other.index

        return self.value.__cmp__(other)

    def __repr__(self):
        return '<EnumAttr {}>'.format(self.name)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.index


class BaseEnumMeta(type):
    def __getattr__(self, attr):
        if attr.lower() in self.attrs:
            return self.attrs[attr.lower()]
        raise AttributeError

    def __getitem__(self, item):
        return self.get(item)

    def get(self, entry):
        for attr in self.attrs.values():
            if attr == entry or attr.name == entry or attr.value == entry:
                return attr

    @property
    def ALL(self):
        return self.attrs.keys()

    @property
    def ALL_VALUES(self):
        return self.attrs.values()


def Enum(*args, **kwargs):
    class _T(with_metaclass(BaseEnumMeta)):
        pass

    _T.attrs = {}
    _T.order = []

    if args:
        _T.order = args
        _T.attrs = {e.lower(): EnumAttr(_T, e.lower(), i, e) for i, e in enumerate(args)}
    else:
        _T.order = []
        _T.attrs = {k.lower(): EnumAttr(_T, k.lower(), v, v) for k, v in kwargs.items()}

    return _T
