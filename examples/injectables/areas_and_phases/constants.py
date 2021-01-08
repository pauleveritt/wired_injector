from enum import Enum


class Area(Enum):
    system = 10
    app = 20
    plugins = 30
    site = 40


class Phase(Enum):
    init = 10
    postinit = 20
