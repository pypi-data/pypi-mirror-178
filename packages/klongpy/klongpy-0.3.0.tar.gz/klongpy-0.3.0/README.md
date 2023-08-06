# klongpy
klong implemented in Python using numpy as the compute backend for vectorization.

Klong: https://t3x.org/klong

Performance: is approximately numpy speed

Supports extending klong with native python lambdas or functions and makes them available in the klong language.

    klong = KlongInterpreter()
    klong['f'] = lambda x, y, z: x*1000 + y - z
    r = klong.exec('f(3; 10; 20)')
    # r == [2990]

# Pandas integration

Pandas integration allows klong to operate on numpy vectors from imported data frames.

# Quickstart

## install

    pip install klongpy

## REPL

    $ python3 klongpy/repl.py

    Welcome to klongpy REPL
    author: Brian Guarraci
    repo  : https://github.com/briangu/klongpy
    crtl-c to quit

    ?>

## examples

    ?> 1+1
    2
    ?> prime::{&/x!:\2+!_x^1%2}
    :monad
    ?> prime@2
    0
    ?> prime@251
    1

to decipher the above: https://t3x.org/klong/prime.html

# Differences from klong

