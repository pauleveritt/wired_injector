from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING, Dict

if TYPE_CHECKING: # pragma: no cover
    from wired_injector import InjectorContainer

from .pipeline.default_pipeline import DefaultPipeline


@dataclass
class Injector:
    """Introspect targets and call/construct with container data.

    The injector is a factory in a container which fetch the data
    needed for a factory, then call it. The injector is a per-container
    service.
    """

    container: 'InjectorContainer'

    def __call__(
        self,
        target: Any,
        system_props: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        props = kwargs
        pipeline = DefaultPipeline(
            container=self.container,
            props=props,
            system_props=system_props,
            target=target,
        )
        result = pipeline()
        return result
