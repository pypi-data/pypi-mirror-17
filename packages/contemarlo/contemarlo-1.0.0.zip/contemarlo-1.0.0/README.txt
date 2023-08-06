ConteMarlo
A "Monte-Carlo-Like" tester.
https://pypi.python.org/pypi/contemarlo/
-Ryan Birmingham

The concept is simple (and probably already done better): detailed Monte-Carlo
but without the randomness or memory dependence.
Despite the memory independence, generators default to safe mode not to flood memory.

I to construct tests, so I know I don't break things.

Classes:
    Resolver - A generator for the next distribution value pair
    Resolver_md - A multidimensional abstraction of Resolver
    Distribution - A distribution, domain [0,1]
