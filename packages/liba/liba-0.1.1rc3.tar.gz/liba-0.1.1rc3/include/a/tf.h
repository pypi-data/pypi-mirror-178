/*!
 @file tf.h
 @brief transfer function
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef A_TF_H
#define A_TF_H

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_TF transfer function
 @{
*/

/*!
 @brief instance structure for transfer function
*/
typedef struct a_tf_s
{
    a_real_t *u; //!< input
    a_real_t *v; //!< output
    const a_real_t *num; //!< numerator
    const a_real_t *den; //!< denominator
    a_uint_t m; //!< numerator number
    a_uint_t n; //!< denominator number
} a_tf_s;

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief set numerator for transfer function
 @param[in,out] ctx points to an instance of transfer function
 @param[in] m numerator number
 @param[in] num numerator
 @param[in] u input buffer
*/
A_PUBLIC a_void_t a_tf_set_num(a_tf_s *ctx, a_uint_t m, const a_real_t *num, a_real_t *u);

/*!
 @brief set denominator for transfer function
 @param[in,out] ctx points to an instance of transfer function
 @param[in] n denominator number
 @param[in] den denominator
 @param[in] v output buffer
*/
A_PUBLIC a_void_t a_tf_set_den(a_tf_s *ctx, a_uint_t n, const a_real_t *den, a_real_t *v);

/*!
 @brief initialize function for transfer function
 @param[in,out] ctx points to an instance of transfer function
 @param[in] m numerator number
 @param[in] num numerator
 @param[in] u input buffer
 @param[in] n denominator number
 @param[in] den denominator
 @param[in] v output buffer
*/
A_PUBLIC a_tf_s *a_tf_init(a_tf_s *ctx,
                           a_uint_t m, const a_real_t *num, a_real_t *u,
                           a_uint_t n, const a_real_t *den, a_real_t *v);

/*!
 @brief process function for transfer function
 @param[in,out] ctx points to an instance of transfer function
 @param[in] x controller output
 @return feedback
*/
A_PUBLIC a_real_t a_tf_proc(a_tf_s *ctx, a_real_t x);

/*!
 @brief terminate function for transfer function
 @param[in,out] ctx points to an instance of transfer function
*/
A_PUBLIC a_tf_s *a_tf_exit(a_tf_s *ctx);

/*!
 @brief zero function for transfer function
 @param[in,out] ctx points to an instance of transfer function
*/
A_PUBLIC a_tf_s *a_tf_zero(a_tf_s *ctx);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_TF */

#endif /* A_TF_H */
