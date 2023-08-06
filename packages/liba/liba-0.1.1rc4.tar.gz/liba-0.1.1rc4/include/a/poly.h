/*!
 @file poly.h
 @brief polynomial
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef A_POLY_H
#define A_POLY_H

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_POLY polynomial
 @{
*/

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief convert between \f$ \sum_{i=0}^{n}a_{i}x^{i} \f$ and \f$ \sum_{i=0}^{n}a_{i}x^{n-i} \f$
*/
A_PUBLIC a_real_t *a_poly_inv(a_real_t *a, a_size_t n);

/*!
 @brief horner function for polynomial \f$ \sum_{i=0}^{n}a_{i}x^{i} \f$
 \f[
  \left\{\begin{array}{l}
  S_n = a_n\\
  S_i = xS_{i+1} + a_i,\quad(i=n-1,n-2,\cdots,1,0)\\
  P(x) = S_0
  \end{array}\right.
 \f]
*/
A_PUBLIC a_real_t a_poly_eval(const a_real_t *a, a_size_t n, a_real_t x);
A_PUBLIC a_real_t *a_poly_evaln(const a_real_t *a, a_size_t n, const a_real_t *ptr, a_size_t num, a_real_t *out);

/*!
 @brief horner function for polynomial \f$ \sum_{i=0}^{n}a_{i}x^{n-i} \f$
 @f[
  \left\{\begin{array}{l}
  S_0 = a_0\\
  S_i = xS_{i-1} + a_i,\quad(i=1,2,\cdots,n-1,n)\\
  P(x) = S_n
  \end{array}\right.
 @f]
*/
A_PUBLIC a_real_t a_poly_evar(const a_real_t *a, a_size_t n, a_real_t x);
A_PUBLIC a_real_t *a_poly_evarn(const a_real_t *a, a_size_t n, const a_real_t *ptr, a_size_t num, a_real_t *out);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_POLY */

#endif /* A_POLY_H */
