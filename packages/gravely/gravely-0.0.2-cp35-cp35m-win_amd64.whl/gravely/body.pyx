# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

#cython: language_level=3, profile=True

"""
Basic Body object for the simulation.
A physical body with mass, coordinates and momentum.
Its class lacks behaviour and only stores data.
Technically it's a C struct, sometimes posing as a numpy record array.
"""

import numpy as np
cimport numpy as np


dtype = np.dtype([
    ('r', np.double, (3,)),
    ('v', np.double, (3,)),
    ('probe', np.int8),
    ('m', np.double),
], align=False)


cpdef inline Body_t Body(double m=0, double x=0, double y=0, double z=0,
        double vx=0, double vy=0, double vz=0, char probe=False):
    cdef Body_t b
    b.m = m
    b.r[0], b.r[1], b.r[2] = x, y, z
    b.v[0], b.v[1], b.v[2] = vx, vy, vz
    b.probe = probe
    return b


def BodyArray(bodies):
    """Create an numpy array if bodies from an iterable of dicts."""
    bodies = list(bodies)  # to make sure that len(bodies) works.
    body_array = np.empty(len(bodies), dtype=dtype)
    for i, b in enumerate(bodies):
        body_array[i]['m'] = b['m']
        body_array[i]['r'] = b['r']
        body_array[i]['v'] = b['v']
        body_array[i]['probe'] = b['probe']
    return body_array
