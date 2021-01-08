from enum import Enum


class Area(Enum):
    system = 10
    app = 20
    plugins = 30
    site = 40


class Kind(Enum):
    config = 1
    component = 2
    view = 3
    injectable = 4
