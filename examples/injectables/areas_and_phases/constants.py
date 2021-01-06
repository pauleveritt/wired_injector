from enum import Enum


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


class Phase(Enum):
    init = 1
    postinit = 2