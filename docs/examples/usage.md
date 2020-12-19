# Usage

Let's see some usage of `wired_injector`.

:::{admonition} The title
:class: note

Each example [is available in the repo](https://github.com/pauleveritt/wired_injector/tree/master/examples/usage) as full working example packages.
:::

## Regular [wired](wired:index) Example

We will use as a starting point a simple, manual [wired](wired:index) application.

```{literalinclude} ../../examples/usage/simple_factory/__init__.py
---
---
```

It loads some factories:

```{literalinclude} ../../examples/usage/simple_factory/factories.py
---
---
```

## Non-Injected, But With `__wired_factory__`

[wired](wired:index) has a way to avoid writing extra factory function.
You can use a class method named `__wired_factory__`:

```{literalinclude} ../../examples/usage/wired_factory/factories.py
---
emphasize-lines: 10-13
---
```

Our registration can now just point to the target as the factory:

```{literalinclude} ../../examples/usage/wired_factory/__init__.py
---
emphasize-lines: 8-8
---
```

## Decorators

Before getting into injection, let's simplify the app by using decorators.
`wired_injector` includes `InjectorRegistry` which has a [venusian](venusian:index) `Scanner` instance and a method to do scanning for decorators:

```{literalinclude} ../../examples/usage/scanner/__init__.py
---
emphasize-lines: 8-8
---
```

One tiny change to our factory.
We decorate our factory with the `@service_factory()` from `wired`.
This elminated the need for `registry.register_factory`:

```{literalinclude} ../../examples/usage/scanner/factories.py
---
emphasize-lines: 6-6
---
```

## Simplest Injection

What if we could get rid of the `__wired_factory__` on `View`?

This is a very simple dataclass.
Its one field has a default value.
In fact, `wired_injector` has a `@injectable` decorator that can do this:

```{literalinclude} ../../examples/usage/simple_injectable/factories.py
---
emphasize-lines: 6-6
---
```

However, we can't use a regular `wired.ServiceContainer` to get `View`.
We need a container that has an "injector" in it, as the injector is tied to the container.
Thus, we use `InjectorRegistry.create_injectable_container`:

```{literalinclude} ../../examples/usage/simple_injectable/__init__.py
---
emphasize-lines: 11-11
---
```

## Injecting Data

That's cheating, though: the `View` doesn't really *depend* on anything in the container.
Let's introduce some `Settings`:

```{literalinclude} ../../examples/usage/settings_manual/factories.py
---
start-after: Site settings
end-at: name=name
---
```

We want to our `View` to be constructed with information from the `Settings`.
This means getting `Settings` from the container, getting the `site_name`, then using it in the construction of the `View` instance.

Which all means we're back to `__wired_factory__` and `@service_factory`:

```{literalinclude} ../../examples/usage/settings_manual/factories.py
---
start-after: View that uses site settings
end-at: name=name
emphasize-lines: 1-1, 6-11
---
```

## Injecting Values

Crap, we brought back `__wired_factory__` -- and it's a whopper.
Here's where we really start to see the value of the injector.

Let's tell the injector go get `Settings` from the container:

```{literalinclude} ../../examples/usage/injected_settings/factories.py
---
start-after: View that uses site settings
end-at: return f'
---
```

No `__wired_factory__` thanks to the switch to `@injectable`.
It looks at the types of your fields and transparently does a `container.get()` for that type.
We then added a `name` property to combine the default value with `site_name`.

## Named Tuples

Allergic to dataclasses? 
How about injectable `typing.NamedTuple` classes?

```{literalinclude} ../../examples/usage/named_tuples/factories.py
---
start-after: View that uses site settings
end-at: return f'
---
```

## Functions

Maybe you're a friend of functional programming.
Here's the view, but as an injectable function that returns a dict:

```{literalinclude} ../../examples/usage/functions/factories.py
---
start-after: View that uses site settings
end-at: return dict
---
```

## Override

`wired` has a neat feature that lets you replace an existing registration.
Let's pass a `for_` to our `@injectable` that says "`MySettings` should be used when you ask for `Settings`":

```{literalinclude} ../../examples/usage/replace/factories.py
---
emphasize-lines: 12-12
---
```

How might this be used?
A pluggable app might define an injectable, which is replaced by a plugin, which might then be replaced by a local site customization.

## Annotations

What if the type we get back isn't the type we look up?

In our last case we used `settings: Settings` as the field.
But we kind of know that the injector is going to give us a `MySettings` instance.
Thus, we'd like the *type checker* to use `MySettings` and the *injector* to look up `BaseSettings`.

[PEP 593](https://www.python.org/dev/peps/pep-0593/) `Annotation` to the rescue.
This lets a type decorations encode extra information to be used by other systems.
In `wired_injector`, this "extra information" is used as instructions to the injector.

```{literalinclude} ../../examples/usage/annotations/factories.py
---
emphasize-lines: 27-27
---
```

With this, our IDE can correctly autocomplete on `self.settings`.

What is `Get`?
It's part of a `wired_injector` "pipeline" of operators.
In this simple case, it says to get `BaseSettings` from the container.

## Annotated NamedTuple

Is this unique to dataclasses?
Nope.
In fact, the switch to `Annotated` was to get beyond dataclass fields.
Here's a `NamedTuple` implementation:

```{literalinclude} ../../examples/usage/annotated_namedtuples/factories.py
---
---
```

## Annotated Functions

What about plain old functions?
They have arguments and arguments can have types which can use `Annotated`.
Sure, why not:

```{literalinclude} ../../examples/usage/annotated_functions/factories.py
---
start-at: Injectable function
end-at: dict(name
---
```

## Props

This is a lot of magic.
Is it worth it?
Let's examine the primary use-case that motivated this: React-style props.

We currently get all of `Settings`, even though all we need is `site_name`.
It makes our injectable sign up for a bigger outside surface area, while making consumers have to support all of `Settings`, "just in case".

If you want components such as `<View/>`, then this works: the injector gets `Settings`.
But if you want other templates to be able to pass in an override value..they don't want to do `<View settings={settings} />`.
That's too big a promise.
They want to do `<View site_name="Custom Name" />`. 
This story also applies to testing, etc.

Let's refactor to make this injectable be more props-oriented:

```{literalinclude} ../../examples/usage/props/factories.py
---
start-after: View
end-at: return f'
emphasize-lines: 4-8
---
```

We now tell the world explicitly what we need: just the `site_name` from `Settings`.

## Custom Props

So that limits the surface area.
How can the *caller* override the injected value?

First, we need to say our `@injectable` behaves a little differently: it wants to support passing in props.

```{literalinclude} ../../examples/usage/custom_prop_value/factories.py
---
start-after: View
end-at: return f
emphasize-lines: 1-1
---
```

Next, we want to pass a "prop" to the injector as part of injection.
All the other fields will come from regular means:

```{literalinclude} ../../examples/usage/custom_prop_value/__init__.py
---
start-at: container.inject
end-at: container.inject
---
```

Systems like `viewdom_wired` automate both the `use_props` and `container.inject` aspect of this.

## Pipelines

We currently have a "pipeline" with one operator: `Get`.
You actually can string together multiple operators:
Let's break the `attr` argument into its own pipeline usage:

```{literalinclude} ../../examples/usage/pipelines/factories.py
---
start-at: View
end-before: property
---
```

Other operators are built-in, and systems and sites can add their own.
The pipeline has some nice flow-of-control features based on custom exceptions.
For example, `Themester` has some component-centric operators.

## Context

```{literalinclude} ../../examples/usage/context/factories.py
---
emphasize-lines: 6-6
---
```

This time we use the `Context` operator to get the container's "context".
Where does that come from?
We create the container but with a `context` keyword argument:

```{literalinclude} ../../examples/usage/context/__init__.py
---
start-at: Per "request"
end-before: container.get
---
```

Context-driven registration is one of the key benefits of `wired`.

## Context Override

We saw in `Replace` how a new implementation could register as a replacement of an existing one. 
`wired` has an even better feature: *multiple*, context-dependent registrations using the container *context*.

We have a `View` that can handle any kind of context.
Let's make a `View` that will be used when the container has a `FrenchCustomer`:

```{literalinclude} ../../examples/usage/context_override/factories.py
---
emphasize-lines: 36-36
---
```

- We make a second kind of "customer"...`FrenchCustomer`

- We also make a second `View` named `FrenchView`

- This new view is "a kind of" `View` (`for_=View`) and should be used when `context=FrenchCustomer`)

- Its `name` property says `Bonjour` instead of `Hello`

This time, when we process a request, we will put a `FrenchCustomer` in the container context:

```{literalinclude} ../../examples/usage/context_override/__init__.py
---
start-at: customer =
end-at: customer =
---
```

