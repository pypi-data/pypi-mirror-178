#ifndef COMPLEX_H
#define COMPLEX_H

#include "a/complex.h"
#include "a/real.h"

#if defined(__GNUC__)
#include <complex.h>
#define A_COMPLEX_T _Complex A_REAL_T
#elif a_prereq_msvc(18, 0)
#include <complex.h> // 12.0
#if A_REAL_TYPE == A_REAL_SINGLE
#define A_COMPLEX_T _Fcomplex
#elif A_REAL_TYPE == A_REAL_DOUBLE
#define A_COMPLEX_T _Dcomplex
#elif A_REAL_TYPE == A_REAL_EXTEND
#define A_COMPLEX_T _Lcomplex
#endif /* A_REAL_TYPE */
#endif /* A_COMPLEX_T */
#if defined(A_COMPLEX_T)

/* compiler built-in complex number type */
#define a_complex_t A_COMPLEX_T

#endif /* A_COMPLEX_T */

#endif /* COMPLEX_H */
