#cython: language_level=3
# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.


cimport numpy as np

cdef packed struct Body_t:
    double r[3]
    double v[3]
    char probe  # [1]
    double m

# [1] Cython breaks when a struct has consecutive fields
#     of same type and different dimension.
#     see https://github.com/cython/cython/issues/1407
