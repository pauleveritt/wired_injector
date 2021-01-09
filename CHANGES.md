# Changes

## Unreleased

- Change `InjectorContainer.inject` to accept `cget_props` as a way of avoiding clashes between props and underlying `.get()` args

- Put `InjectorContainer` in top-level exports

- `attr` support on `Context`

- Decorator and scanner support a category option for scanner

- Make `target` available in an operator, to go get fields

- Create a `Field` operator that can fetch the default value from the target

## 0.3.0

- Allow register_injectable to only supply `for_` and `target` then defaults to it

## 0.2.0

- Add `InjectorRegistry` and `InjectorContainer` to improve DX

- Make the decorator designed to be subclassed, to allow `use_props`
  and `for_` to be automated
