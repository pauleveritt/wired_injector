# TODO

## Now

## Next

## Eventually

- `wired.dataclasses.Context` sentinel
- InitVar and postinit ideas
- Allow `customers: Tuple[Customer]`
- Tests that cover TypeDict, regular classes
- What should happen when `Get` fails? Fallback to default, or fail?
- Very friendly exceptions that tell the field and target very specifically
- Operators: `Key`, `Call`, `AsDict`
- Ensure mypy is happy
- Handle Union[Foo, str]

## Done

- Get Annotated tests for each of 3 types
- Refactor fields to reduce duplication
- Eliminate previous 593 stuff
- Default values (function, named tuple, typed dict, dataclass)
