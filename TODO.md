# TODO

## Now

## Next

- Allow `customers: Tuple[Customer]`

## Soon

- Document:
  - custom decorators
  - use_props

## Eventually

- Very friendly exceptions that tell the field and target very specifically
- Operators: `Key`, `Call`, `AsDict`
- Ensure mypy is happy
- Handle Union[Foo, str]
- Tests that cover TypeDict, regular classes
- InitVar and postinit ideas

## Done

- Get Annotated tests for each of 3 types
- Refactor fields to reduce duplication
- Eliminate previous 593 stuff
- Default values (function, named tuple, typed dict, dataclass)
- `Context` operator
- What should happen when `Get` fails? Fallback to default, or fail?
- System props
- Make a `@injectable` decorator
- Allow the injectable class-based decorator to be subclassed 
  to gain a default `for_`
- myst for docs
- Put API into Sphinx docs
  * Improve docstrings and use Napoleon
  * intersphinx
- Refactor examples to not be executed immediately on import
- Use new examples style
