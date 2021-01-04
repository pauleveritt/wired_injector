# TODO

## Now

Config system which can record all the injectables, apply them, then report on them for uses such as generation of Sphinx config directives.

- Write some examples that exercise it
  * Multi-area, multi-phase, multi-kind system (e.g. themester)
  * Custom decorator (e.g. `config`) which sets default: phase, kind, info
  * Get a listing of info['shortname'] after apply
- Change decorator to have default kind (but the class and invocation can pass it in)

- Example issues that I'm trying to solve with `Injectables`
  * Themester, Sphinx, app might all want to set `_static` output target
  * Nice autocomplete on config attrs/values for site admin
  * Is `ThemeConfig` protocol really needed?
  * Single `ThemabasterConfig` winds up as a garbage barge
  
- Injectables To-Do from whiteboard
  * Setup in phases: pre/post/neither, system/app/plugins/site
  * Sphinx app gets setup from conf.py
    - But can scan for decorators in conf.py or packages below
  * Make static root a first class part of Themester config
    - Other config can reference it
  * Config field values can depend on other field values
  * Slim down `make_registry` and friends
    - Inline into storytime, no need to be separate
  * Ensure `@config` can do `__wired_factory__` for special cases
  * Use `Injectable.info` to collect stuff like `shortname` that can be used for Sphinx config directives



## Next

- Pipeline, PipelineField, PipelineStep
  * Handle common exceptions more gracefully
  * Provide access to props and system_props
  * Write a `Props('propname')` operator
  * Introduce logging to help debugging
  * Research PyCharm breakpoints (doesn't stop on a return)  
  * Put a specific plug-point to enable debugging breakpoints
- Make an example showing plain-old-class, perhaps even typed-dict

## Soon

- Context manager
  * https://medium.com/swlh/python-coding-tip-using-the-with-statement-instead-try-finally-f45a645c6008

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
- Make `target` available in an operator, to go get fields
- Create a `Field` operator that can fetch the default value from the target


