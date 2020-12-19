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
examples/index
api
```
