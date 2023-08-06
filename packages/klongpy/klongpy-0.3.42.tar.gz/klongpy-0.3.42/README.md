
![Unit Tests](https://github.com/briangu/klongpy/workflows/Unit%20Tests/badge.svg)

# KlongPy
KlongPy is a vectorized port of klong, a simple array lanaguage.  The result is a blazingly fast array language that has direct Python integration.

Numpy is used as the target because it itself is an [Iverson Ghost](https://analyzethedatanotthedrivel.org/2018/03/31/numpy-another-iverson-ghost/), or rather a descendent of APL.

Using numpy also means that via [CuPy](https://github.com/cupy/cupy), both CPU and GPU backends are supported.

If have no idea what Klong is, read this site [Klong](https://t3x.org/klong) and the [Klong Book](https://t3x.org/klong/book.html).  You're welcome.


# Performance

The Klong language is simple, so the overhead is low.  The bulk of the compute time will likely be spent in numpy doing actual work.

### Python

    def python_vec(number=100):
        r = timeit.timeit(lambda: [2 * (1 + x) for x in range(10000000)], number=number)
        return r/number

### NumPy (CPU) and CuPy

    # both use the same implementation
    def klong_vec(number=100):
        klong = KlongInterpreter()
        r = timeit.timeit(lambda: klong.exec("2*1+!10000000"), number=number)
        return r/number

### Results

    klong vec
    0.030662008338142185
    numpy vec
    0.031103943731170147
    klong vs numpy => 1.0144131261121019


# Status

KlongPy aims to be a complete implementation of klong.  It currently passes all of the integration tests provided by klong.  Additional tests will continue to be added to ensure proper vectorization, etc.

# Python integration

KlongPy supports direct Python integration by allowing you to use lambdas or functions, making these extensions available in the klong language - and vice versa.

    klong = KlongInterpreter()
    klong['f'] = lambda x, y, z: x*1000 + y - z
    r = klong.exec('f(3; 10; 20)')
    assert r[0] == 2990

Further, you can essentially use Klong as a complement to existing python code or vice versa.

    data = np.arange(10*9)
    klong['data'] = data
    r = klong.exec('1+data')
    assert r[0] == 1 + data

Variables may be directly retrieved from KlongPy context:

    r = klong.exec('Q::1+data')
    Q = klong['Q']
    print(Q)

### Pandas Integration

    TODO: Example

### Web server

    TODO: Example

# Installation

### CPU

    $ pip3 install klongpy

### GPU support

    $ pip3 install klongpy[gpu]


### Develop

    $ git clone https://github.com/briangu/klongpy.git
    $ cd klongpy
    $ python3 setup.py develop


## REPL

    $ pip3 install klongpy[repl]
    $ kgpy

    Welcome to klongpy REPL
    author: Brian Guarraci
    repo  : https://github.com/briangu/klongpy
    crtl-c to quit

    ?> 1+1
    2
    ?> prime::{&/x!:\2+!_x^1%2}
    :monad
    ?> prime@2
    0
    ?> prime@251
    1

Read about the [prime example here](https://t3x.org/klong/prime.html).


# Differences from Klong

The main difference between Klong and KlongPy is that KlongPy doesn't infinite precision because it's backed by NumPy which is restricted to doubles.

# Running tests

```bash
python3 -m unittest
```

# Acknowledgement

Huge thanks to Nils M Holm for his work on Klong and providing the foundations for this interesting project.

