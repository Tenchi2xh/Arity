# Arity TODO

## Goals

- Full package for immutable functional programming
- Single import: many libraries have elements of FP, and you import them piece by piece. Arity should do `from arity import *` and make everything available as if Python was suddenly a new FP language
- Should be easy to debug
- Have pretty prints for all collections
- Support for both Python 2 & 3

## Features

- [ ] Immutable collections
- [ ] Streams
- [ ] Curse existing collections for collection methods (`map`, etc.)
- [ ] Curse numbers classes (add `to`, `until`, etc.)
- [ ] Uniform map/reduce/etc. across Python versions
- [ ] Iterator helpers (`fold`, `grouped`, `sliding`, etc.)
- [ ] Short lambda functions inspired from fn.py's underscore, with unique identifier support (i.e. `(x + y) * x`)
- [ ] Partial functions
- [ ] Function composition
- [ ] Some aspect of point-free style
- [ ] Nifty decorators:
    - [x] `@tail_recursive` to ensure tail recursion and apply optimization
    - [ ] `@pure` to ensure a function has no side-effects (blacklisting of impure things, going through the AST to count assignments with stacked scopes)
    - [ ] `@curry`
