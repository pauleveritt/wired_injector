# TODO

## Now

- Allow the injectable class-based decorator to be subclassed 
  to gain a default `for_`
  
## Next

- Allow `customers: Tuple[Customer]`
- Use new examples style
- myst for docs

## Soon

- Put API into Sphinx docs
  * Improve docstrings and use Napoleon


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
