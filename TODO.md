# TODO

## Now

## Next

## Soon

- Document:
  - custom decorators
  - use_props

## Eventually

- Allow `customers: Tuple[Customer]`, `Union[Foo, str]`
- Very friendly exceptions that tell the field and target very specifically
- Operators: `Key`, `Call`, `AsDict`
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
- Allow register_injectable to only supply `for_` and `target` then defaults to it
- Prevent the collision of `name` passed in as a prop and also used as the `container.get` param
- `attr` support on `Context`
- Decorator and scanner support a category option for scanner


