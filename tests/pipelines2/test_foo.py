from dataclasses import dataclass, field
from typing import TypeVar, Any, Type, Optional, Protocol


class Animal(Protocol):
    name: str


@dataclass
class Mammal:
    name: str


K = TypeVar('K')


@dataclass
class Container:
    items: Any = field(default_factory=dict)

    def get(self, key: Type[K]) -> Optional[K]:
        v: K = self.items.get(key)
        return v


def test_main() -> None:
    c = Container()
    c.items[Animal] = Mammal(name='cat')
    result = c.get(Animal)  # type: ignore
    if result is not None:
        assert 'cat' == result.name
