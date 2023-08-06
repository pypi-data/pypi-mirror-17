# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

#cython: language_level=3, cdivision=True, profile=True

"""
A solver for a gravitaty simulator.
Calculates the potential, then moves bodies according to it.
"""

import cython
cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport sqrt, ceil

from .body import Body
from .body cimport Body_t


cdef double GRAVITATIONAL_CONSTANT = 6.674e-8  # cm3 g-1 s-2


cdef class SolverConfig:
    """Wraps relevant config variables in a C struct for faster access."""
    cdef public double max_dt, substepping_target_acceleration
    cdef public int substepping_max_depth

    def __init__(self, global_config):
        """Extract relevant config variables from a global config."""
        self.max_dt = global_config.dt
        self.substepping_target_acceleration = \
            global_config.substepping_target_acceleration
        self.substepping_max_depth = global_config.substepping_max_depth


@cython.boundscheck(False)
cdef int determine_substepping_depth(
        SolverConfig config,
        Body_t[:] bodies_prev,
        Body_t[:] bodies_moved):
    """Determine target substepping depth, from 1 to maximum allowed."""

    if config.substepping_max_depth <= 1:
        return 1

    cdef int substepping_depth = 1
    cdef double acceleration

    cdef int i
    for i in range(bodies_prev.shape[0]):
        acceleration = sqrt(
                (bodies_prev[i].v[0] - bodies_moved[i].v[0]) ** 2 +
                (bodies_prev[i].v[1] - bodies_moved[i].v[1]) ** 2 +
                (bodies_prev[i].v[2] - bodies_moved[i].v[2]) ** 2
        ) / config.max_dt

        substepping_depth = <int> ceil(
            acceleration / config.substepping_target_acceleration
        )

        if substepping_depth >= config.substepping_max_depth:
            return config.substepping_max_depth

    return substepping_depth


cpdef int move_bodies_with_substepping(
        SolverConfig config,
        Body_t[:] bodies_prev,
        Body_t[:] out):
    move_bodies(config, bodies_prev, config.max_dt, out=out)
    """Determine substepping depth, call move_bodies multiple times."""

    cdef int substepping_depth
    substepping_depth = determine_substepping_depth(config, bodies_prev, out)

    cdef Body_t[:] buf_back, buf_front
    if substepping_depth > 1:
        # substantial acceleration detected
        # recalculation with substepping required
        substepped_dt = config.max_dt / substepping_depth
        buf_front, buf_back = bodies_prev.copy(), bodies_prev.copy()
        for i in range(substepping_depth):
            move_bodies(config, buf_front, substepped_dt, out=buf_back)
            buf_front, buf_back = buf_back, buf_front
        out[...] = buf_front
        return substepping_depth
    else:
        # speed changes turned out to be insubstantial
        # recalculation with substepping is not required
        return 1


@cython.boundscheck(False)
cdef inline void move_bodies(
        SolverConfig config,
        Body_t[:] bodies_prev,
        double dt,
        Body_t[:] out) nogil:
    """Call move_single_body for all bodies."""
    cdef int i
    for i in range(bodies_prev.shape[0]):
        out[i] = moved_single_body(config, bodies_prev[i], bodies_prev, dt)


@cython.boundscheck(False)
cdef inline Body_t moved_single_body(
        SolverConfig config,
        Body_t body_prev,
        Body_t[:] bodies_prev,
        double dt) nogil:
    """Calculate body movement and momentum change due to other bodies."""

    cdef double diff_r[3]
    cdef double distance
    cdef Body_t body_curr = body_prev

    cdef int i
    cdef Body_t other_body
    for i in range(bodies_prev.shape[0]):
        other_body = bodies_prev[i]
        if other_body.probe:
            continue

        diff_r = (
                other_body.r[0] - body_prev.r[0], 
                other_body.r[1] - body_prev.r[1], 
                other_body.r[2] - body_prev.r[2], 
        )

        distance = sqrt(diff_r[0] ** 2 + diff_r[1] ** 2 + diff_r[2] ** 2)
        if distance == 0:
            continue

        # F  =  G * m * M / R^2
        # a  =  F / m  =  G * M / R^2
        # a_x  =  a * R_x / R  =  (G * M / R^3) * R_x
        # dv_x  =  dt  * a_x  =  dt * (G * M / R^3) * R_x
        GM_R3 = GRAVITATIONAL_CONSTANT * other_body.m / distance ** 3
        body_curr.v[0] += dt * GM_R3 * diff_r[0]
        body_curr.v[1] += dt * GM_R3 * diff_r[1]
        body_curr.v[2] += dt * GM_R3 * diff_r[2]

    body_curr.r[0] += dt * (body_prev.v[0] + body_curr.v[0]) / 2
    body_curr.r[1] += dt * (body_prev.v[1] + body_curr.v[1]) / 2
    body_curr.r[2] += dt * (body_prev.v[2] + body_curr.v[2]) / 2

    return body_curr
