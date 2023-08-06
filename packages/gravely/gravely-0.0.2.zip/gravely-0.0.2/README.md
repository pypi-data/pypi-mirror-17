gravely, a gravity simulator
============================


Introduction
------------
`gravely` is a gravity simulator,
written to taste modern Python packaging practices.

It uses [Cython](http://cython.org) compiled extensions,
depends on [Numpy](http://www.numpy.org) and [h5py](http://www.h5py.org),
compiles into a single binary with [PyInstaller](http://pyinstaller.org) and
aims to support both Linux and Windows.
Not exactly a walk in the park.


License
-------
`gravely` is distributed under the terms of the MIT License;
see [LICENSE.txt](LICENSE.txt).


Usage
-----
Pyinstaller binary:

    ./gravely test
    ./gravely run
    ./gravely animate

Installed Python package:

    python3 -m gravely test
    python3 -m gravely run
    python3 -m gravely animate


Installation
------------
**First of all, try using a precompiled binary made with PyInstaller.**
If that doesn't suit you, you should report that
and proceed to installing the Python package.

The base requirements to begin with are a working C compiler,
`Python>=3.4` with development headers,
`setuptools>=20`, `numpy>=1.8.2` and `pip>=8`.
These should be enough to start installation of `gravely`
from a source archive or a precompiled wheel (`.whl`) file:

    python3 -m pip install gravely-*.zip
    python3 -m pip install gravely-*.whl

Other packages may or may not install automatically with pip/setuptools magic.

`gravely` also depends on `cython>=0.21` (build) and `h5py>=2.2` (run-time).
Rendering nice video animations requires `matplotlib>=1.4` and `ffmpeg`.
Testing requires `nose>=1.0`.

Try to satisfy as many of these
before attempting to build and install `gravely`.

### Linux, Debian-based
    apt-get install gcc python3 python3-dev python3-setuptools python3-pip \
            cython3 python3-numpy python3-matplotlib python3-nose ffmpeg

### Install necessary upgrades with pip
    pip3 install 'pip>=8'
    python3 -m pip install \
            'cython>=0.21' 'setuptools>=20' 'matplotlib>=1.4' 'nose>=1.0'
    python3 -m pip install -r requirements.txt

### Windows
Good luck.

Currently only Windows 10 and Python 3.5 are supported.

Some say that it's better to use specialized Python distributions like
[Anaconda](https://www.continuum.io) or
[Enthought Canopy](https://www.enthought.com/products/canopy)
to get the prerequisities straight.

As for vanilla Python... Visual Studio with Python support
and several pip invocations could be a good start:

    python -m pip install cython numpy matplotlib nose
    python -m pip install http://www.silx.org/pub/wheelhouse/h5py-2.6.0-cp35-cp35m-win_amd64.whl
