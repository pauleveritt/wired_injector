# wired_injector

Tired of picking apart the [wired](wired:index) container inside your data classes and services?
`wired_injector` brings type-based dependency injection, plus a pipeline with operators, to your code.

## Installation

Installation follows the normal Python packaging approach:

```bash
  $ pip install wired_injector
```

## Quick Examples

Make an injectable factory:

```{literalinclude} ../examples/usage/simple_injectable/factories.py
---
start-at: injectable(
---
```

You can then make an `InjectorRegistry` that scans for decorators:

```{literalinclude} ../examples/usage/simple_injectable/__init__.py
---
start-at: InjectorRegistry(
end-at: scan(
---
```

The inject can construct your instances.
Maybe you need the container's `Settings`:

```{literalinclude} ../examples/usage/injected_settings/factories.py
---
start-after: View that
end-at: Settings
---
```

Want to use `NamedTuple` instead of `dataclass`?

```{literalinclude} ../examples/usage/named_tuples/factories.py
---
start-after: View that
end-at: Settings
---
```

Or perhaps functions instead?

```{literalinclude} ../examples/usage/functions/factories.py
---
start-after: View that
end-at: return dict
---
```

Use `Annotated` to give instructions to the injector, such as look up one type but expect a return value of another:

```{literalinclude} ../examples/usage/annotations/factories.py
---
start-at: Annotated[
end-at: Annotated[
---
```

Use pipelines with operators -- even custom -- to narrow down the injection to the smallest surface area:

```{literalinclude} ../examples/usage/pipelines/factories.py
---
start-at: Annotated[
end-before: property
---
```

```{toctree}
---
hidden: true
---
examples/index
api
```
