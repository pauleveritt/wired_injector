# wired_injector

Tired of picking apart the [wired](wired:index) container inside your data classes and services?
`wired_injector` brings type-based dependency injection, plus a pipeline with operators, to your code.

## Installation

Installation follows the normal Python packaging approach:

```bash
  $ pip install wired_injector
```

## Quick Examples

Imagine we have a `wired` app.
It makes a "registry" at startup, pointed at a Python package to scan for decorators.
Then, for each "request", it makes a container to generate a results:

```{literalinclude} ../examples/index/simple_factory/__init__.py
---
start-at: The app
end-before: return expected, result
---
```

It loads some factories:

```{literalinclude} ../examples/index/simple_factory/factories.py
---
start-at: service_factory()
end-at: return cls()
---
```

This, though, could be simpler, using the [@injectable](wired_injector.injectable) decorator.
It eliminates `__wired_factory__`:

```{literalinclude} ../examples/index/injectable_view/factories.py
---
start-at: injectable()
end-at: str =
---
```

That's cheating, though: the `View` doesn't really *depend* on anything in the container.
Let's introduce some `Settings`:

```{literalinclude} ../examples/index/settings_view/factories.py
---
start-at: Site settings
end-at: name=name
---
```

Crap, we brought back `__wired_factory__` and it's a whopper.
Let's use the injector to make that a little better:

```{literalinclude} ../examples/index/injector_settings/factories.py
---
start-at: Injectable view
end-at: f'View - {site_name}'
---
```

That's quite interesting...the `View` has a dataclass field of type `Settings`.
The injector knows to go do `container.get(Settings)` and pass it in when constructing a view.

What if the type we get back isn't the type we look up?
In the following, the `name` property uses `upper_name` which isn't on `Settings`.
It's on `MySettings` which overrides `Settings`.
You can use Python's `Annotated` to give instructions to the injector:

```{literalinclude} ../examples/index/annotated/factories.py
---
start-at: class Settings
end-at: f'View - {site_name}'
---
```

With this, our IDE can correctly autocomplete on `self.settings.upper_name`.

What is `Get`?
It's part of a `wired_injector` "pipeline" of operators.
In this simple case, it says to get the `Settings` from the container.

Is this unique to dataclasses?
Nope.
In fact, the switch to `Annotated` was to get beyond dataclass fields.
Here's a `NamedTuple` implementation:

```{literalinclude} ../examples/index/annotated_namedtuple/factories.py
---
start-at: Injectable NamedTuple
end-at: f'View - {site_name}'
---
```

What about plain old functions?
They have arguments and arguments can have types which can use `Annotated`.
Sure, why not:

```{literalinclude} ../examples/index/annotated_functions/factories.py
---
start-at: Injectable function
end-at: dict(name
---
```

But the injector can do better than just re-mapping types.
We don't really need -- in some cases like component props, actually don't want -- the entire `Settings`.
What if we could use the injector pipeline like a little DSL?

```{literalinclude} ../examples/index/operators/factories.py
---
start-at: Injectable view
end-at: f'View - {self.site_name}'
---
```

That's a pipeline with just one operator.
It's actually a shorthand form of a pipeline that could explicitly use the `Attr` operator:

```{literalinclude} ../examples/index/pipelines/factories.py
---
start-at: Injectable view
end-at: f'View - {self.site_name}'
---
```

Other operators are built-in, and systems and sites can add their own.
For example, `Themester` has some component-centric operators.

```{toctree}
---
hidden: true
---
usage/index
api
```
