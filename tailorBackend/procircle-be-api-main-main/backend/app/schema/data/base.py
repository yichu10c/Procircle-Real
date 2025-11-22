"""
Data Model Base
"""

class StringEnumBase:
    @classmethod
    def values(cls):
        return [
            v for (k, v) in vars(cls).items()
            if not k.startswith("__") and not k.endswith("__")
        ]

    @classmethod
    def keys(cls):
        return [
            k for (k, v) in vars(cls).items()
            if not k.startswith("__") and not k.endswith("__")
        ]

    @classmethod
    def items(cls):
        return {
            k: v for (k, v) in vars(cls).items()
            if not k.startswith("__") and not k.endswith("__")
        }
