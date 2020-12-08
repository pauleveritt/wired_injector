# wired_injector: Dependency Injection for Containers

Tired of picking apart the [wired](https://wired.readthedocs.io/en/latest/) container inside your data classes and services?
`wired_injector` brings type-based dependency injection, plus operators, to your code.


## Installation

Installation follows the normal Python packaging approach:

```bash
  $ pip install wired_injector
```

## Quick Examples

Imagine we have a `wired` app.
It makes a "registry" at startup, pointed at a Python package to scan for decorators.
Then, for each "request", it makes a container to generate a results:

```{literalinclude} ../examples/index/simple_factory.py
---
start-at: from examples import example_registry
end-before: def test
---
```

This, though, could be simpler, using the `@injectable` decorator.
It eliminates `__wired_factory__`:

```{literalinclude} ../examples/index/injectable_view.py
---
start-at: injectable()
end-at: str =
---
```

We do this by making an `Injector`, bound to the container.
Then, instead of doing `container.get(View)`, we use the injector:

```python
container = registry.create_container()
injector = Injector(container)
container.register_singleton(injector, Injector)
view: View = injector(View)
```

:::{note}
This is a bit of ceremony that gets handled in an app.
For example, `Themester` wires this up for you.
:::

That's cheating, though: the `View` doesn't really *depend* on anything in the container.
Let's introduce some `Settings`:

```{literalinclude} ../examples/index/settings_view.py
---
start-at: Site settings
end-at: name=name
---
```

Crap, we brought back `__wired_factory__` and it's a whopper.
Let's use the injector to make that a little better:

```{literalinclude} ../examples/index/injector_settings.py
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

```{literalinclude} ../examples/index/annotated.py
---
start-at: class Settings
end-at: f'View - {site_name}'
---
```

With this, our IDE can correctly autocomplete on `self.settings.upper_name`.

What is `Get`?
It's part of a `wired_injector` "pipeline" of operators.
In this simple case, it says to get the `Settings` from the container.

But it can do better.
We don't really need -- in some cases like component props, actually don't want -- the entire `Settings`.
What if we could use the injector pipeline like a little DSL?

```{literalinclude} ../examples/index/operators.py
---
start-at: Injectable view
end-at: f'View - {self.site_name}'
---
```
