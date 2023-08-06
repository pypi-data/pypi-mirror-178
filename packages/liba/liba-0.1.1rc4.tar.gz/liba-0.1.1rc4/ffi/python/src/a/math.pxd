from a cimport *

cdef extern from "a/math.h":
    a_f32_t a_sqrt_inv(a_f32_t x)
