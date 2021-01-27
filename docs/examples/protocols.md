# Protocols

"Yuck, Java!"

[Python PEP 544 Protocols](https://www.python.org/dev/peps/pep-0544/) brings *structural* typing, aka "static duck typing", to Python.
It separates the "interface" from the implementation, which is common in Java, and makes Python folks rethink their life decisions.

Truth is, protocols aren't for everybody.
Most will never need it.
But if you are in a certain bulls-eye...then it's worth considering.

Let's take a look at the *why*, the *how*, and the *what* of protocols, *without* `wired_injector`. 
Then, let's see protocols in action, in a supporting system, one designed for that very bulls-eye.

## Who?

Protocols, like type hints, are optional.
You can avoid and ignore them, even more easily than type hints.
Signs that this might be the right step for you:

- If you *hate type hints*, you'll likely hate protocols
- If you think Python is only for:
  * 30 lines scripts,
  * ...that will be forgotten in one week,
  * ...by folks in their first year of programming,
  * ...then you'll likely hate protocols... -ish
- If you are coolio with [nominal subtyping](https://www.python.org/dev/peps/pep-0544/#nominal-vs-structural-subtyping) (i.e. subclassing), then hug your inheritance trees and abc's

Signs you might be ok with protocols:

- You write "broad" software used and extended by lots of people for multiple years
- You agree with the Gang of Four [composition over inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/)
- Building a replaceable, pluggable system?
  * Multiple implementations of a "thing"
  * Now you're speaking my language

## Why

If that's the bulls-eye for *people*, what's the bulls-eye for *type of application*?

This document answers that with examples.
But this is such a hard sell, let's set some markers early.

- TypeScript is actually winning over the cowboy coders of *JavaScript*
- I'm making a `Greeter`...did I get it right?
- Red squiggles
    * The benefit of "fail faster"
    * In the IDE (duh)..."HELP ME HELP YOU!"
    * Static analysis in CI
    * Navigation, autocomplete etc. in code *and* tests
- Large-scale "pluggable apps"
- Design Patterns, Uncle Bob's open/closed in [SOLID](https://stackify.com/solid-design-open-closed-principle/), Bertrand Meyer [Design By Contract](https://en.wikipedia.org/wiki/Design_by_contract) 
  * This isn't about "Java"
  * It's about scalable designs
- Mostly for provider-side

## Key Insight

I kept fighting protocols, trying to mash them into being a modern `zope.interface`.
Thanks to Andrey Vlasovskikh, I am *kinda* embracing a certain zen.

- Protocols are a *loose* `is-a`
    * This is on purpose
    * You don't mark an implementation as "this is a `Greeter`"
    * The intent springs into existence on *usage*
- Nada interfaces
    * Narrator: He's still trying

Let's move on to some code which tries to *show the problem* being solved.

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

Let's start without any protocols, just a simple app:

- `Greeter`
- `greets`
- `Customer`

From a "let's build a pluggable system", line 14 is the important part:

```{literalinclude} ../../examples/protocols/simple_app/__init__.py
---
emphasize-lines: 14-14
---
```

The `test` function shows what will later be our "pluggable app".
That is, something that might handle a request.

This code:

- *Runs* in Python
- *Works* in PyCharm (static analysis)
- *Works* in mypy (static analysis)

Want to run it yourself? 
Go to `tests/test_examples.py` and run `test_examples_protocols` in pytest.
You can also run this with `mypy --strict`.

## Second Customer

Let's make a second kind of customer.
It's a contrived example: the only difference is a data value.
We'll then try greeting each kind of customer.

The code runs, the tests pass, but PyCharm and mypy are mad at line 35:

```{literalinclude} ../../examples/protocols/second_customer/__init__.py
---
emphasize-lines: 29-29
---
```

Here's what mypy reports:

```bash
$ mypy --strict examples/protocols/second_customer/
examples/protocols/second_customer/__init__.py:35: error: Argument 1 to "greet" of "Greeter" has incompatible type "FrenchCustomer"; expected "RegularCustomer"
Found 1 error in 1 file (checked 1 source file)
```

This makes complete sense: we don't have an inheritance tree, so `FrenchCustomer` isn't related to `RegularCustomer`.
Thanks, tooling!

## Base Customer

Our code runs but fails static analysis.
Let's fix that by making a base class `Customer` and then have our 

```{literalinclude} ../../examples/protocols/base_customer/__init__.py
---
emphasize-lines: 5-6, 10-10, 15-15
---
```

Nouns are (my opinion) a reasonable usage of superclasses for (nominal) typing. 
But (haha) even this has some problems (see: dataclass inheritance and field.)

## Second Greeter

Things are messier for parts of the system with behavior.
Let's add a second kind of `Greeter`:

```{literalinclude} ../../examples/protocols/second_greeter/__init__.py
---
emphasize-lines: 42
---
```

This code runs in Python, is ok in PyCharm, but `mypy --strict` is displeased:

```bash
$ mypy --strict examples/protocols/second_greeter/
examples/protocols/second_greeter/__init__.py:44: error: Incompatible types in assignment (expression has type "RegularGreeter", variable has type "FrenchGreeter")
Found 1 error in 1 file (checked 1 source file)
```

Let's gleefully embrace the wrong idea and again throw inheritance at this.

## Base Greeter

We've added a base class for `Greeter` and moved the `greet` method to it.
Our code runs in Python and is fine in static analysis for PyCharm and mypy:

```{literalinclude} ../../examples/protocols/base_greeter/__init__.py
---
emphasize-lines: 42
---
```

Line 57 solves the mypy complaint from before.
But we've opened up the rabbit-hole of inheritance.
What would be the alternative?
How could we just say:

- `AmericanGreeter` is a kind of `Greeter`
- ...without taking onboard all of "unwelcome guests"?

Gang of Four to the rescue! We want...composition over inheritance.

## Simple Protocols

First, a little restructuring, clarify responsibilities.
Our "app" that does the driving:

```{literalinclude} ../../examples/protocols/simple_protocols/__init__.py
---
emphasize-lines: 13-13, 18-18
---
```

Now, instead of *base classes* that define the "contract", we have...protocols:

```{literalinclude} ../../examples/protocols/simple_protocols/protocols.py
```

As you can see, though they look like classes, they actually have no implementation.

Our implementations are in another file:

```{literalinclude} ../../examples/protocols/simple_protocols/models.py
---
emphasize-lines: 20-20, 29-29
---
```

As you can see, our `greet` methods pass in a `Customer` protocol.
This **lets me test them** with a dummy while still getting the benefits of static typing (in fact, avoiding a failure.)
In fact, what's more interesting is *what's missing*: no subclassing, and no mention of the protocols that these implement!

Let's point out some interesting items at this point:

- In the emphasized line 13 above, we say we have a tuple of `Customer` objects. 
  What does that mean?
  It's actually kinda-freaky: it's structural and ducky.
  But it lets the tooling then help us (squigglies, autocomplete.)
  And lets that "database" contain any future instance of a type that fits the shape of the protocol.  

- Line 18...mypy gets mad about this.
  But PyCharm gets mad without it.
  ARRRRGH!

Protocols are already useful.
Let's **show** how tooling can tell us we have the wrong shape for a `Greeter`.
Let's also **show** what happens when `FrenchGreeter.greet` goes from `Customer` -> `FrenchCustomer`

Once we bit the bullet and do `Any` on Line 18 (or switch to string keys), mypy is happy.

## Adherent

What if you could state that an implementation implements a protocol?
We'd get...red squigglies for breaking the contract!

Here's a (problematic) [decorator implementation from Glyph](https://github.com/python/mypy/issues/4717#issuecomment-454609539):

```{literalinclude} ../../examples/protocols/adherent/models.py
---
emphasize-lines: 8-8, 14-14, 20-20, 30-30
---
```

When you break the contract, `mypy --strict` complains.
This saves the work of writing tests that assert the "contract" through a variable annotation.
It also opens the door for IDEs to do navigation, completion, refactoring, etc.

But alas...PyCharm doesn't have any support for this.


:::{admonition} Obscure "implements"
:class: note

PEP 544 has an oft-overlooked section [claiming that subclassing](https://www.python.org/dev/peps/pep-0544/#explicitly-declaring-implementation) can be used to say that a class is an implementation of a protocol.
If so, that would be great!
You could tell if you go it right, *while writing the implementation*
Maybe even get coding assistance.

Alas, it's a red herring.
It isn't really implemented, and likely never will be.
In fact, Glyph argues persuasively that it's an anti-pattern.
It certainly has negative side effects, by putting the protocol in the MRO.
:::

## Simple Pluggable App

All this is preface to an example showing a "pluggable app": multiple roles playing together, with caller and callee at arm's-length.
It uses `wired_injector` but that can be just an example of the pattern.

We'll go slow.
First, the driver code:

```{literalinclude} ../../examples/protocols/pluggable_app/__init__.py
```

This then loads the "pluggable app":

```{literalinclude} ../../examples/protocols/pluggable_app/app.py
---
emphasize-lines: 13-13
---
```

In a web application, for example, the registry is built at startup, then the containers are built on each request.
The interesting part: line 13 asks "the system" for an implementation of a *protocol*, not a class.
The "system" finds the right implementation for the context.
In this case, the "view" registered for a certain kind of `Customer`. 


What kinds of things are built into this "pluggable app"?
Let's look at the protocols:

```{literalinclude} ../../examples/protocols/pluggable_app/protocols.py
```

The system might ship with some default implementations of views:

```{literalinclude} ../../examples/protocols/pluggable_app/views.py
```

Again, these implementations make no statement about the protocols they support.
Their support is expressed simply by have the shape of some protocol.

The `@injectable` decorator is part of `wired_injector`, which is a system for helping build pluggable applications with dependency injection.
These lines say "the following class is a kind of View and should be used when the context is a FrenchCustomer".

## Pluggable System

Last step: a pluggable app.

Imagine big systems, such as, say, Sphinx or Django.
There's the *app* itself: it's not just a framework, it actually does something "out of the box".
Then there are *plugins* which can add to *or replace* what's in the app.
Finally, a particular *site* can customize and override anything, including pulling in plugins.

How do you have a system in which callers and callees have no knowledge of each other?
How do participants know if they are "painting in the lines"?

We'll start at the top with the driver:

```{literalinclude} ../../examples/protocols/pluggable_system/__init__.py
```

The pluggable app code makes a registry and goes looking for services to register:

```{literalinclude} ../../examples/protocols/pluggable_system/app/__init__.py
```

The pluggable app also writes the contracts for known pluggable things:

```{literalinclude} ../../examples/protocols/pluggable_system/app/protocols.py
```

You can then have some plugins that are scanned.
In this example, the plugins directory is empty.
And you can have a "site" area, which can define implementations:

```{literalinclude} ../../examples/protocols/pluggable_system/site/views.py
```

Since the site is scanned last, it wins, and this becomes the default view implementation.

Even better, since protocols are used, you can use some tooling to tell you if your site's view breaks the current *or future* contract.

## Challenges

That's a roundup of using protocols in a real system.
Let's discuss some of the downsides, after using them for a while:

- You'll get a bunch of "Yuck, Java" reactions
- It's *more work* to write a spec and an implementation
- Nearly everything is broken...this is new and rarely used, not sure it will ever catch on
  - Every protocol ticket in mypy feels obscure, magical, and unlikely to ever get fixed
- Squigglies, but the error is...?
- Interplay with metaprogramming (dataclasses, decorators, etc.)
- Can't say "implements"
- Can't use Protocol as a type hint
- Runtime feels like a hack
- No second-generation help (e.g. "PyCharm let me navigate to all the implementers", adapters are probably out)
