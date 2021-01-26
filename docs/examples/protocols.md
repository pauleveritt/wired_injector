# Protocols



:::{admonition} Importing `Protocol`
:class: note

If you are using Python 3.9 or higher, you can just import it.
Older, then you need to install `typing_extensions` and import from there.
To straddle, use something like this:

```python
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol
```
:::

## A Simple Starting Point


```{literalinclude} ../../examples/protocols/simple_app/__init__.py
```

## Second Customer


```{literalinclude} ../../examples/protocols/second_customer/__init__.py
```


## Base Customer


```{literalinclude} ../../examples/protocols/base_customer/__init__.py
```


## Second Greeter


```{literalinclude} ../../examples/protocols/second_greeter/__init__.py
```


## Base Greeter


```{literalinclude} ../../examples/protocols/base_greeter/__init__.py
```


## Simple Protocols


```{literalinclude} ../../examples/protocols/simple_protocols/__init__.py
```

