# Injectables

A system based on ``Injectables`` works in 4 phases:

Find
====

Go look in the system, the app, plugins, and the site for injectables
that want to be registered.

Record
======

Instead of directly calling ``registry.register_factory``, record the
registration info into ``Injectables.pending_items``.

Commit
======

When finished with each area, e.g. ``system``, "commit" the
``pending_items`` with the enum value of the area, e.g. ``system``.
This does nothing more than:

- Remove each ``Injectable`` in ``pending_items``

- Change its ``area`` field from ``None`` to the value being committed

- Append it to the permanent ``items`` list

Apply
=====

After all the injectables have been collected, iterate through each,
in "order", and call ``InjectorRegistry.register_factory``.

What is the "order"? For each "phase" (in order), then each "area"
(in order). Thus, the system might register all ``phase=init`` injectables
first, and with those, ``area=system`` first. It's possible that, later,
a third level grouping is implemented, to allow register ``kind=config``
before other kinds of injectables.

The ``area`` is something under the control of the caller. We don't
demand that each usage of a decorator/register_injectable says whether
it is in the system, the app, or a plugin. That info can be determined
by the caller.

The ``phase``, though, *is* something each decorator/register_injectable
should determine. Only it knows if the information it is providing or
consuming should be at a certain point in registration. This is simplified
by a reasonable default: you can go first and don't depend on anything else.

- ``register_injectable`` (and thus ``@injectable`` and all derived decorators)
  defer their registration until a second ``apply_injectables`` step
- Group the injectables by phase, then "area" (e.g. system, app, plugin,
  site), then apply them
- Keep track of the injectables to allow instrospection and other special
  uses, such as generating Sphinx config directives from the
  `kind=Kind.config` injectables
- The actual area/phase/kind vocabularies are external, provided as enums,
  which allow sorting the priority of the values
- Generic `info` dict which lets a system pass along extra information that
  can be put to some use
- Rely on Python 3.7 or later ordering of dicts


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
  * Decide whether to get rid of customizable venusian scan `category = 'wired'` on decorator

## Work Done

* ``Injectables`` dataclass, stored as optional on the registry
* `system` field which records registrations
* `add_injectables` applies the registrations at end
* Processing is done in batches to implement the "area" part
* Optional instance on `InjectorRegistry`
* Change `register_injectable` to add to `system`
* Change decorator if needed (or at least write a test)
* Don't apply until later
