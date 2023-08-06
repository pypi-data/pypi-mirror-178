/*!
 @file a.h
 @brief algorithm library
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef A_A_H
#define A_A_H

#include "config.h"
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
#include <float.h>

/*!
 @addtogroup A algorithm library based on C
 @{
*/

#if defined(__cplusplus)
#define a_cast_r(T, x) reinterpret_cast<T>(x)
#define a_cast_d(T, x) dynamic_cast<T>(x)
#define a_cast_s(T, x) static_cast<T>(x)
#define a_cast_c(T, x) const_cast<T>(x)
#else /* !__cplusplus */
#define a_cast_r(T, x) ((T)(x))
#define a_cast_d(T, x) ((T)(x))
#define a_cast_s(T, x) ((T)(x))
#define a_cast_c(T, x) ((T)(x))
#endif /* __cplusplus */

#if !defined A_VOID_T
#define A_VOID_T void
#endif /* A_VOID_T */
#if defined(__cplusplus) && defined(A_HAVE_NULLPTR)
#define A_NULL nullptr
#else /* !__cplusplus */
#define A_NULL NULL
#endif /* __cplusplus */
/*! static cast to \ref a_void_t */
#define a_void_c(x) a_cast_s(A_VOID_T, x)
#define a_void_p(x) a_cast_s(A_VOID_T *, x)
#define a_void_P(x) a_cast_s(const A_VOID_T *, x)
/*! as the declaration of the incomplete type */
#define a_void_t A_VOID_T

#if !defined __cplusplus
#define A_FALSE 0
#define A_TRUE !A_FALSE
#else /* !__cplusplus */
#define A_FALSE false
#define A_TRUE true
#endif /* __cplusplus */
#if !defined A_BOOL_T
#define A_BOOL_T int
#endif /* A_BOOL_T */
/*! static cast to \ref a_bool_t */
#define a_bool_c(x) (!!(x))
/*! type, capable of holding one of the two values: 1 and 0 */
#define a_bool_t A_BOOL_T

#define a_byte_P(x) a_cast_s(const a_byte_t *, x)
#define a_char_P(x) a_cast_s(const a_char_t *, x)
#define a_byte_p(x) a_cast_s(a_byte_t *, x)
#define a_char_p(x) a_cast_s(a_char_t *, x)
#define a_byte_c(x) a_cast_s(a_byte_t, x)
#define a_char_c(x) a_cast_s(a_char_t, x)
#define a_byte_t unsigned char
#define a_char_t char
/* the most optimal integer type for the platform */
#define a_uint_P(x) a_cast_s(const a_uint_t *, x)
#define a_int_P(x) a_cast_s(const a_int_t *, x)
#define a_uint_p(x) a_cast_s(a_uint_t *, x)
#define a_int_p(x) a_cast_s(a_int_t *, x)
#define a_uint_c(x) a_cast_s(a_uint_t, x)
#define a_int_c(x) a_cast_s(a_int_t, x)
#define a_uint_t unsigned int
#define a_int_t int

#if !defined A_I_T
#define A_I_T signed int
#endif /* A_I_T */
#if !defined A_U_T
#define A_U_T unsigned int
#endif /* A_U_T */
#if !defined A_I_MIN
#define A_I_MIN INT_MIN
#endif /* A_I_MIN */
#if !defined A_I_MAX
#define A_I_MAX INT_MAX
#endif /* A_I_MAX */
#if !defined A_U_MAX
#define A_U_MAX UINT_MAX
#endif /* A_U_MAX */
/*! static cast to \ref a_i_t */
#define a_i_c(x) a_cast_s(A_I_T, x)
#define a_i_p(x) a_cast_s(A_I_T *, x)
#define a_i_P(x) a_cast_s(const A_I_T *, x)
/*! static cast to \ref a_u_t */
#define a_u_c(x) a_cast_s(A_U_T, x)
#define a_u_p(x) a_cast_s(A_U_T *, x)
#define a_u_P(x) a_cast_s(const A_U_T *, x)
/*! signed integer type is guaranteed to be at least 16 bits */
#define a_i_t A_I_T
/*! unsigned integer type is guaranteed to be at least 16 bits */
#define a_u_t A_U_T

#if !defined A_IS_T
#define A_IS_T signed short
#endif /* A_IS_T */
#if !defined A_US_T
#define A_US_T unsigned short
#endif /* A_US_T */
#if !defined A_IS_MIN
#define A_IS_MIN SHRT_MIN
#endif /* A_IS_MIN */
#if !defined A_IS_MAX
#define A_IS_MAX SHRT_MAX
#endif /* A_IS_MAX */
#if !defined A_US_MAX
#define A_US_MAX USHRT_MAX
#endif /* A_US_MAX */
/*! static cast to \ref a_is_t */
#define a_is_c(x) a_cast_s(A_IS_T, x)
#define a_is_p(x) a_cast_s(A_IS_T *, x)
#define a_is_P(x) a_cast_s(const A_IS_T *, x)
/*! static cast to \ref a_us_t */
#define a_us_c(x) a_cast_s(A_US_T, x)
#define a_us_p(x) a_cast_s(A_US_T *, x)
#define a_us_P(x) a_cast_s(const A_US_T *, x)
/*! signed integer type is guaranteed to be at least 16 bits */
#define a_is_t A_IS_T
/*! unsigned integer type is guaranteed to be at least 16 bits */
#define a_us_t A_US_T

#if !defined A_IL_T
#define A_IL_T signed long
#endif /* A_IL_T */
#if !defined A_UL_T
#define A_UL_T unsigned long
#endif /* A_UL_T */
#if !defined A_IL_MIN
#define A_IL_MIN LONG_MIN
#endif /* A_IL_MIN */
#if !defined A_IL_MAX
#define A_IL_MAX LONG_MAX
#endif /* A_IL_MAX */
#if !defined A_UL_MAX
#define A_UL_MAX ULONG_MAX
#endif /* A_UL_MAX */
/*! static cast to \ref a_il_t */
#define a_il_c(x) a_cast_s(A_IL_T, x)
#define a_il_p(x) a_cast_s(A_IL_T *, x)
#define a_il_P(x) a_cast_s(const A_IL_T *, x)
/*! static cast to \ref a_ul_t */
#define a_ul_c(x) a_cast_s(A_UL_T, x)
#define a_ul_p(x) a_cast_s(A_UL_T *, x)
#define a_ul_P(x) a_cast_s(const A_UL_T *, x)
/*! signed integer type is guaranteed to be at least 32 bits */
#define a_il_t A_IL_T
/*! unsigned integer type is guaranteed to be at least 32 bits */
#define a_ul_t A_UL_T

#if defined(A_HAVE_LONG_LONG_TYPE)

#if !defined A_ILL_T
#define A_ILL_T signed long long
#endif /* A_ILL_T */
#if !defined A_ULL_T
#define A_ULL_T unsigned long long
#endif /* A_ULL_T */
#if !defined A_ILL_MIN
#define A_ILL_MIN LLONG_MIN
#endif /* A_ILL_MIN */
#if !defined A_ILL_MAX
#define A_ILL_MAX LLONG_MAX
#endif /* A_ILL_MAX */
#if !defined A_ULL_MAX
#define A_ULL_MAX ULLONG_MAX
#endif /* A_ULL_MAX */
/*! static cast to \ref a_ill_t */
#define a_ill_c(x) a_cast_s(A_ILL_T, x)
#define a_ill_p(x) a_cast_s(A_ILL_T *, x)
#define a_ill_P(x) a_cast_s(const A_ILL_T *, x)
/*! static cast to \ref a_ull_t */
#define a_ull_c(x) a_cast_s(A_ULL_T, x)
#define a_ull_p(x) a_cast_s(A_ULL_T *, x)
#define a_ull_P(x) a_cast_s(const A_ULL_T *, x)
/*! signed integer type is guaranteed to be at least 64 bits */
#define a_ill_t A_ILL_T
/*! unsigned integer type is guaranteed to be at least 64 bits */
#define a_ull_t A_ULL_T

#endif /* A_HAVE_LONG_LONG_TYPE */

#if !defined A_SINGLE_T
#define A_SINGLE_T float
#endif /* A_SINGLE_T */
#define A_SINGLE_C(X) X##F
#define A_SINGLE_F(F) F##f
#define A_SINGLE_F1(F, a) F##f(a)
#define A_SINGLE_F2(F, a, b) F##f(a, b)
#define A_SINGLE_F3(F, a, b, c) F##f(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_SINGLE_FN(F, ...) F##f(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */
#define A_SINGLE_MIN FLT_MIN
#define A_SINGLE_MAX FLT_MAX
#define A_SINGLE_INF a_single_c(A_DOUBLE_INF)
#define A_SINGLE_NAN (A_SINGLE_C(0.0) * A_SINGLE_INF)
/*! format constants for the fprintf family of functions */
#define A_SINGLE_PRI(F, C) "%" F C
/*! format constants for the fscanf family of functions */
#define A_SINGLE_SCN(F, C) "%" F C
/*! static cast to \ref a_single_t */
#define a_single_c(x) a_cast_s(A_SINGLE_T, x)
#define a_single_p(x) a_cast_s(A_SINGLE_T *, x)
#define a_single_P(x) a_cast_s(const A_SINGLE_T *, x)
/*! single precision floating point type. Matches IEEE-754 binary32 format if supported. */
#define a_single_t A_SINGLE_T

#if !defined A_DOUBLE_T
#define A_DOUBLE_T double
#endif /* A_DOUBLE_T */
#define A_DOUBLE_C(X) X
#define A_DOUBLE_F(F) F
#define A_DOUBLE_F1(F, a) F(a)
#define A_DOUBLE_F2(F, a, b) F(a, b)
#define A_DOUBLE_F3(F, a, b, c) F(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_DOUBLE_FN(F, ...) F(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */
#define A_DOUBLE_MIN DBL_MIN
#define A_DOUBLE_MAX DBL_MAX
#define A_DOUBLE_INF (DBL_MAX * DBL_MAX)
#define A_DOUBLE_NAN (A_DOUBLE_C(0.0) * A_DOUBLE_INF)
/*! format constants for the fprintf family of functions */
#define A_DOUBLE_PRI(F, C) "%" F "l" C
/*! format constants for the fscanf family of functions */
#define A_DOUBLE_SCN(F, C) "%" F "l" C
/*! static cast to \ref a_double_t */
#define a_double_c(x) a_cast_s(A_DOUBLE_T, x)
#define a_double_p(x) a_cast_s(A_DOUBLE_T *, x)
#define a_double_P(x) a_cast_s(const A_DOUBLE_T *, x)
/*! double precision floating point type. Matches IEEE-754 binary32 format if supported. */
#define a_double_t A_DOUBLE_T

#if !defined A_EXTEND_T
#define A_EXTEND_T long double
#endif /* A_EXTEND_T */
#define A_EXTEND_C(X) X##L
#define A_EXTEND_F(F) F##l
#define A_EXTEND_F1(F, a) F##l(a)
#define A_EXTEND_F2(F, a, b) F##l(a, b)
#define A_EXTEND_F3(F, a, b, c) F##l(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_EXTEND_FN(F, ...) F##l(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */
#define A_EXTEND_MIN LDBL_MIN
#define A_EXTEND_MAX LDBL_MAX
#define A_EXTEND_INF (LDBL_MAX * LDBL_MAX)
#define A_EXTEND_NAN (A_EXTEND_C(0.0) * A_EXTEND_INF)
/*! format constants for the fprintf family of functions */
#define A_EXTEND_PRI(F, C) "%" F "L" C
/*! format constants for the fscanf family of functions */
#define A_EXTEND_SCN(F, C) "%" F "L" C
/*! static cast to \ref a_extend_t */
#define a_extend_c(x) a_cast_s(A_EXTEND_T, x)
#define a_extend_p(x) a_cast_s(A_EXTEND_T *, x)
#define a_extend_P(x) a_cast_s(const A_EXTEND_T *, x)
/*! extend precision floating point type. Matches IEEE-754 extend format if supported. */
#define a_extend_t A_EXTEND_T

#if !defined A_I8_T
#define A_I8_T int8_t
#endif /* A_I8_T */
#if !defined A_U8_T
#define A_U8_T uint8_t
#endif /* A_U8_T */
#if !defined A_I8_MIN
#define A_I8_MIN INT8_MIN
#endif /* A_I8_MIN */
#if !defined A_I8_MAX
#define A_I8_MAX INT8_MAX
#endif /* A_I8_MAX */
#if !defined A_U8_MAX
#define A_U8_MAX UINT8_MAX
#endif /* A_U8_MAX */
#if !defined A_I8_C
#define A_I8_C(X) INT8_C(X)
#endif /* A_I8_C */
#if !defined A_U8_C
#define A_U8_C(X) UINT8_C(X)
#endif /* A_U8_C */
/*! static cast to \ref a_i8_t */
#define a_i8_c(x) a_cast_s(A_I8_T, x)
#define a_i8_p(x) a_cast_s(A_I8_T *, x)
#define a_i8_P(x) a_cast_s(const A_I8_T *, x)
/*! static cast to \ref a_u8_t */
#define a_u8_c(x) a_cast_s(A_U8_T, x)
#define a_u8_p(x) a_cast_s(A_U8_T *, x)
#define a_u8_P(x) a_cast_s(const A_U8_T *, x)
/*! signed integer type with width of exactly 8 bits */
#define a_i8_t A_I8_T
/*! unsigned integer type with width of exactly 8 bits */
#define a_u8_t A_U8_T

#if !defined A_I16_T
#define A_I16_T int16_t
#endif /* A_I16_T */
#if !defined A_U16_T
#define A_U16_T uint16_t
#endif /* A_U16_T */
#if !defined A_I16_MIN
#define A_I16_MIN INT16_MIN
#endif /* A_I16_MIN */
#if !defined A_I16_MAX
#define A_I16_MAX INT16_MAX
#endif /* A_I16_MAX */
#if !defined A_U16_MAX
#define A_U16_MAX UINT16_MAX
#endif /* A_U16_MAX */
#if !defined A_I16_C
#define A_I16_C(X) INT16_C(X)
#endif /* A_I16_C */
#if !defined A_U16_C
#define A_U16_C(X) UINT16_C(X)
#endif /* A_U16_C */
/*! static cast to \ref a_i16_t */
#define a_i16_c(x) a_cast_s(A_I16_T, x)
#define a_i16_p(x) a_cast_s(A_I16_T *, x)
#define a_i16_P(x) a_cast_s(const A_I16_T *, x)
/*! static cast to \ref a_u16_t */
#define a_u16_c(x) a_cast_s(A_U16_T, x)
#define a_u16_p(x) a_cast_s(A_U16_T *, x)
#define a_u16_P(x) a_cast_s(const A_U16_T *, x)
/*! signed integer type with width of exactly 16 bits */
#define a_i16_t A_I16_T
/*! unsigned integer type with width of exactly 16 bits */
#define a_u16_t A_U16_T

#if !defined A_I32_T
#define A_I32_T int32_t
#endif /* A_I32_T */
#if !defined A_U32_T
#define A_U32_T uint32_t
#endif /* A_U32_T */
#if !defined A_I32_MIN
#define A_I32_MIN INT32_MIN
#endif /* A_I32_MIN */
#if !defined A_I32_MAX
#define A_I32_MAX INT32_MAX
#endif /* A_I32_MAX */
#if !defined A_U32_MAX
#define A_U32_MAX UINT32_MAX
#endif /* A_U32_MAX */
#if !defined A_I32_C
#define A_I32_C(X) INT32_C(X)
#endif /* A_I32_C */
#if !defined A_U32_C
#define A_U32_C(X) UINT32_C(X)
#endif /* A_U32_C */
/*! static cast to \ref a_i32_t */
#define a_i32_c(x) a_cast_s(A_I32_T, x)
#define a_i32_p(x) a_cast_s(A_I32_T *, x)
#define a_i32_P(x) a_cast_s(const A_I32_T *, x)
/*! static cast to \ref a_u32_t */
#define a_u32_c(x) a_cast_s(A_U32_T, x)
#define a_u32_p(x) a_cast_s(A_U32_T *, x)
#define a_u32_P(x) a_cast_s(const A_U32_T *, x)
/*! signed integer type with width of exactly 32 bits */
#define a_i32_t A_I32_T
/*! unsigned integer type with width of exactly 32 bits */
#define a_u32_t A_U32_T

#if !defined A_I64_T
#define A_I64_T int64_t
#endif /* A_I64_T */
#if !defined A_U64_T
#define A_U64_T uint64_t
#endif /* A_U64_T */
#if !defined A_I64_MIN
#define A_I64_MIN INT64_MIN
#endif /* A_I64_MIN */
#if !defined A_I64_MAX
#define A_I64_MAX INT64_MAX
#endif /* A_I64_MAX */
#if !defined A_U64_MAX
#define A_U64_MAX UINT64_MAX
#endif /* A_U64_MAX */
#if !defined A_I64_C
#define A_I64_C(X) INT64_C(X)
#endif /* A_I64_C */
#if !defined A_U64_C
#define A_U64_C(X) UINT64_C(X)
#endif /* A_U64_C */
/*! static cast to \ref a_i64_t */
#define a_i64_c(x) a_cast_s(A_I64_T, x)
#define a_i64_p(x) a_cast_s(A_I64_T *, x)
#define a_i64_P(x) a_cast_s(const A_I64_T *, x)
/*! static cast to \ref a_u64_t */
#define a_u64_c(x) a_cast_s(A_U64_T, x)
#define a_u64_p(x) a_cast_s(A_U64_T *, x)
#define a_u64_P(x) a_cast_s(const A_U64_T *, x)
/*! signed integer type with width of exactly 64 bits */
#define a_i64_t A_I64_T
/*! unsigned integer type with width of exactly 64 bits */
#define a_u64_t A_U64_T

#if !defined A_IMAX_T
#define A_IMAX_T intmax_t
#endif /* A_IMAX_T */
#if !defined A_UMAX_T
#define A_UMAX_T uintmax_t
#endif /* A_UMAX_T */
#if !defined A_IMAX_MIN
#define A_IMAX_MIN INTMAX_MIN
#endif /* A_IMAX_MIN */
#if !defined A_IMAX_MAX
#define A_IMAX_MAX INTMAX_MAX
#endif /* A_IMAX_MAX */
#if !defined A_UMAX_MAX
#define A_UMAX_MAX UINTMAX_MAX
#endif /* A_UMAX_MAX */
#if !defined A_IMAX_C
#define A_IMAX_C(X) INTMAX_C(X)
#endif /* A_IMAX_C */
#if !defined A_UMAX_C
#define A_UMAX_C(X) UINTMAX_C(X)
#endif /* A_UMAX_C */
/*! static cast to \ref a_imax_t */
#define a_imax_c(x) a_cast_s(A_IMAX_T, x)
#define a_imax_p(x) a_cast_s(A_IMAX_T *, x)
#define a_imax_P(x) a_cast_s(const A_IMAX_T *, x)
/*! static cast to \ref a_umax_t */
#define a_umax_c(x) a_cast_s(A_UMAX_T, x)
#define a_umax_p(x) a_cast_s(A_UMAX_T *, x)
#define a_umax_P(x) a_cast_s(const A_UMAX_T *, x)
/*! maximum-width signed integer type */
#define a_imax_t A_IMAX_T
/*! maximum-width unsigned integer type */
#define a_umax_t A_UMAX_T

#if !defined A_IPTR_T
#define A_IPTR_T intptr_t
#endif /* A_IPTR_T */
#if !defined A_UPTR_T
#define A_UPTR_T uintptr_t
#endif /* A_UPTR_T */
#if !defined A_IPTR_MIN
#define A_IPTR_MIN INTPTR_MIN
#endif /* A_IPTR_MIN */
#if !defined A_IPTR_MAX
#define A_IPTR_MAX INTPTR_MAX
#endif /* A_IPTR_MAX */
#if !defined A_UPTR_MAX
#define A_UPTR_MAX UINTPTR_MAX
#endif /* A_UPTR_MAX */
#if !defined A_IPTR_C
#define A_IPTR_C(X) INTPTR_C(X)
#endif /* A_IPTR_C */
#if !defined A_UPTR_C
#define A_UPTR_C(X) UINTPTR_C(X)
#endif /* A_UPTR_C */
/*! static cast to \ref a_iptr_t */
#define a_iptr_c(x) a_cast_s(A_IPTR_T, x)
#define a_iptr_p(x) a_cast_s(A_IPTR_T *, x)
#define a_iptr_P(x) a_cast_s(const A_IPTR_T *, x)
/*! static cast to \ref a_uptr_t */
#define a_uptr_c(x) a_cast_s(A_UPTR_T, x)
#define a_uptr_p(x) a_cast_s(A_UPTR_T *, x)
#define a_uptr_P(x) a_cast_s(const A_UPTR_T *, x)
/*! signed integer type capable of holding a pointer to void */
#define a_iptr_t A_IPTR_T
/*! unsigned integer type capable of holding a pointer to void */
#define a_uptr_t A_UPTR_T

#if !defined A_DIFF_T
#define A_DIFF_T ptrdiff_t
#endif /* A_DIFF_T */
#if !defined A_DIFF_MIN
#define A_DIFF_MIN PTRDIFF_MIN
#endif /* A_DIFF_MIN */
#if !defined A_DIFF_MAX
#define A_DIFF_MAX PTRDIFF_MAX
#endif /* A_DIFF_MAX */
/*! static cast to \ref a_diff_t */
#define a_diff_c(x) a_cast_s(A_DIFF_T, x)
#define a_diff_p(x) a_cast_s(A_DIFF_T *, x)
#define a_diff_P(x) a_cast_s(const A_DIFF_T *, x)
/*! signed integer type returned when subtracting two pointers */
#define a_diff_t A_DIFF_T

#if !defined A_SIZE_T
#define A_SIZE_T size_t
#endif /* A_SIZE_T */
#if !defined A_SIZE_MAX
#define A_SIZE_MAX SIZE_MAX
#endif /* A_SIZE_MAX */
/*! static cast to \ref a_size_t */
#define a_size_c(x) a_cast_s(A_SIZE_T, x)
#define a_size_p(x) a_cast_s(A_SIZE_T *, x)
#define a_size_P(x) a_cast_s(const A_SIZE_T *, x)
/*! unsigned integer type returned by the sizeof operator */
#define a_size_t A_SIZE_T

#if !defined A_F16_T
#define A_F16_T A_U16_T
#endif /* A_F16_T */
#define A_F16_NNAN A_U16_C(0xFE00)
#define A_F16_PNAN A_U16_C(0x7E00)
#define A_F16_NINF A_U16_C(0xFC00)
#define A_F16_PINF A_U16_C(0x7C00)

#if !defined A_F32_T
#define A_F32_T float
#endif /* A_F32_T */
#define A_F32_C(X) X##F
#define A_F32_F(F) F##f
#define A_F32_F1(F, a) F##f(a)
#define A_F32_F2(F, a, b) F##f(a, b)
#define A_F32_F3(F, a, b, c) F##f(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_F32_FN(F, ...) F##f(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */
#define A_F32_MIN FLT_MIN
#define A_F32_MAX FLT_MAX
#define A_F32_INF a_f32_c(A_F64_INF)
#define A_F32_NAN (A_F32_C(0.0) * A_F32_INF)
#define A_F32_NNAN A_U32_C(0xFFC00000)
#define A_F32_PNAN A_U32_C(0x7FC00000)
#define A_F32_NINF A_U32_C(0xFF800000)
#define A_F32_PINF A_U32_C(0x7F800000)
/*! format constants for the fprintf family of functions */
#define A_F32_PRI(F, C) "%" F C
/*! format constants for the fscanf family of functions */
#define A_F32_SCN(F, C) "%" F C
/*! static cast to \ref a_f32_t */
#define a_f32_c(x) a_cast_s(A_F32_T, x)
#define a_f32_p(x) a_cast_s(A_F32_T *, x)
#define a_f32_P(x) a_cast_s(const A_F32_T *, x)
/*! single precision floating point type. Matches IEEE-754 binary32 format if supported. */
#define a_f32_t A_F32_T

#if !defined A_F64_T
#define A_F64_T double
#endif /* A_F64_T */
#define A_F64_C(X) X
#define A_F64_F(F) F
#define A_F64_F1(F, a) F(a)
#define A_F64_F2(F, a, b) F(a, b)
#define A_F64_F3(F, a, b, c) F(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_F64_FN(F, ...) F(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */
#define A_F64_MIN DBL_MIN
#define A_F64_MAX DBL_MAX
#define A_F64_INF (DBL_MAX * DBL_MAX)
#define A_F64_NAN (A_F64_C(0.0) * A_F64_INF)
#define A_F64_NNAN A_U64_C(0xFFF8000000000000)
#define A_F64_PNAN A_U64_C(0x7FF8000000000000)
#define A_F64_NINF A_U64_C(0xFFF0000000000000)
#define A_F64_PINF A_U64_C(0x7FF0000000000000)
/*! format constants for the fprintf family of functions */
#define A_F64_PRI(F, C) "%" F "l" C
/*! format constants for the fscanf family of functions */
#define A_F64_SCN(F, C) "%" F "l" C
/*! static cast to \ref a_f64_t */
#define a_f64_c(x) a_cast_s(A_F64_T, x)
#define a_f64_p(x) a_cast_s(A_F64_T *, x)
#define a_f64_P(x) a_cast_s(const A_F64_T *, x)
/*! double precision floating point type. Matches IEEE-754 binary64 format if supported. */
#define a_f64_t A_F64_T

typedef char *a_str_t;
#define a_str_c(x) a_cast_s(a_str_t, x)
typedef const char *a_cstr_t;
#define a_cstr_c(x) a_cast_s(a_cstr_t, x)
typedef void *a_vptr_t;
#define a_vptr_c(x) a_cast_s(a_vptr_t, x)
typedef const void *a_cptr_t;
#define a_cptr_c(x) a_cast_s(a_cptr_t, x)

typedef union a_cast_u
{
    a_i_t i;
    a_u_t u;
    a_is_t is;
    a_us_t us;
    a_il_t il;
    a_ul_t ul;
#if defined(A_HAVE_LONG_LONG_TYPE)
    a_ill_t ill;
    a_ull_t ull;
#endif /* A_HAVE_LONG_LONG_TYPE */
    a_i8_t i8;
    a_u8_t u8;
    a_i16_t i16;
    a_u16_t u16;
    a_i32_t i32;
    a_u32_t u32;
    a_i64_t i64;
    a_u64_t u64;
    a_f32_t f32;
    a_f64_t f64;
    a_diff_t diff;
    a_size_t size;
    a_imax_t imax;
    a_umax_t umax;
    a_iptr_t iptr;
    a_uptr_t uptr;
    a_cptr_t cptr;
    a_vptr_t vptr;
    a_cstr_t cstr;
    a_str_t str;
    a_char_t c;
} a_cast_u;

/*!
 @addtogroup A_REAL real number
 @{
*/

/*! real number bytes */
#if !defined A_REAL_TYPE
#if !defined A_SIZE_REAL
#define A_REAL_TYPE A_REAL_DOUBLE
#else /* !A_SIZE_REAL */
#define A_REAL_TYPE A_SIZE_REAL
#endif /* A_SIZE_REAL */
#endif /* A_REAL_TYPE */
#define A_REAL_SINGLE 0x04
#define A_REAL_DOUBLE 0x08
#define A_REAL_EXTEND 0x10
#if A_REAL_TYPE == A_REAL_SINGLE

/*! real number stored using `float` */
#if !defined A_REAL_T
#define A_REAL_T float
#endif /* A_REAL_T */
#if !defined A_REAL_MIN
#define A_REAL_MIN FLT_MIN
#endif /* A_REAL_MIN */
#if !defined A_REAL_MAX
#define A_REAL_MAX FLT_MAX
#endif /* A_REAL_MAX */

/*!
 expands to a floating-point constant expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_C(X) X##F
/*!
 expands to a floating-point function expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_F(F) F##f
#define A_REAL_F1(F, a) F##f(a)
#define A_REAL_F2(F, a, b) F##f(a, b)
#define A_REAL_F3(F, a, b, c) F##f(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_REAL_FN(F, ...) F##f(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */

/*! format constants for the fprintf family of functions */
#define A_REAL_PRI(F, C) "%" F C
/*! format constants for the fscanf family of functions */
#define A_REAL_SCN(F, C) "%" F C

#elif A_REAL_TYPE == A_REAL_DOUBLE

/*! real number stored using `double` */
#if !defined A_REAL_T
#define A_REAL_T double
#endif /* A_REAL_T */
#if !defined A_REAL_MIN
#define A_REAL_MIN DBL_MIN
#endif /* A_REAL_MIN */
#if !defined A_REAL_MAX
#define A_REAL_MAX DBL_MAX
#endif /* A_REAL_MAX */

/*!
 expands to a floating-point constant expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_C(X) X
/*!
 expands to a floating-point function expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_F(F) F
#define A_REAL_F1(F, a) F(a)
#define A_REAL_F2(F, a, b) F(a, b)
#define A_REAL_F3(F, a, b, c) F(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_REAL_FN(F, ...) F(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */

/*! format constants for the fprintf family of functions */
#define A_REAL_PRI(F, C) "%" F C
/*! format constants for the fscanf family of functions */
#define A_REAL_SCN(F, C) "%" F "l" C

#elif A_REAL_TYPE == A_REAL_EXTEND

/*! real number stored using `long double` */
#if !defined A_REAL_T
#define A_REAL_T long double
#endif /* A_REAL_T */
#if !defined A_REAL_MIN
#define A_REAL_MIN LDBL_MIN
#endif /* A_REAL_MIN */
#if !defined A_REAL_MAX
#define A_REAL_MAX LDBL_MAX
#endif /* A_REAL_MAX */

/*!
 expands to a floating-point constant expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_C(X) X##L
/*!
 expands to a floating-point function expression having the value specified by its argument and the type \ref a_real_t
*/
#define A_REAL_F(F) F##l
#define A_REAL_F1(F, a) F##l(a)
#define A_REAL_F2(F, a, b) F##l(a, b)
#define A_REAL_F3(F, a, b, c) F##l(a, b, c)
#if defined(A_HAVE_VARIADIC_MACROS)
#define A_REAL_FN(F, ...) F##l(__VA_ARGS__)
#endif /* A_HAVE_VARIADIC_MACROS */

/*! format constants for the fprintf family of functions */
#define A_REAL_PRI(F, C) "%" F "L" C
/*! format constants for the fscanf family of functions */
#define A_REAL_SCN(F, C) "%" F "L" C

#else /* !A_REAL_TYPE */
#error unknown precision
#endif /* A_REAL_TYPE */

#define A_REAL_INF a_cast_s(A_REAL_T, A_F64_INF)
#define A_REAL_NAN (A_REAL_C(0.0) * A_REAL_INF)

/*! static cast to \ref a_real_t */
#define a_real_c(x) a_cast_s(A_REAL_T, x)
#define a_real_p(x) a_cast_s(A_REAL_T *, x)
#define a_real_P(x) a_cast_s(const A_REAL_T *, x)
/*! compiler built-in real number type */
#define a_real_t A_REAL_T

typedef union a_real_u
{
    a_real_t v; //!< a real value
    a_real_t *p; //!< real vector
} a_real_u;

/*! @} A_REAL */

/*!
 @brief size of memory that alignment is specified by alignment
 @param base specifies the alignment that is a power of two
 @param size number of bytes to allocate
*/
#define a_align(base, size) ((a_cast_s(a_size_t, size) + (base)-1) & ~((base)-1))

/*!
 @brief size of an array
 @param a must be an array variable
*/
#define a_arrayof(a) (sizeof(a) / sizeof(*(a)))

/*!
 @brief offset of a structure member
 @param type structure type
 @param member member variable
*/
#if defined(offsetof)
#define a_offsetof(type, member) offsetof(type, member)
#else /* !offsetof */
#define a_offsetof(type, member) a_cast_r(a_size_t, &a_cast_r(type *, 0)->member)
#endif /* offsetof */

/*!
 @brief container of a structure member
 @param ptr pointer to a member variable
 @param type structure type
 @param member member variable
*/
#define a_container_of(ptr, type, member) a_cast_r(type *, a_cast_r(a_uptr_t, ptr) - a_offsetof(type, member))

/*!
 @brief iterate from 0 to n and not include n
 @param I index type of the iteration
 @param i index variable of the iteration
 @param n final value of the iteration
*/
#define a_forenum(I, i, n) for (I i = 0; i < (n); ++i)

/*!
 @brief iterate from n to 0 and not include n
 @param I index type of the iteration
 @param i index variable of the iteration
 @param n final value of the iteration
*/
#define a_forenum_reverse(I, i, n) for (I i = (n); i-- > 0;)

/*!
 @brief iterate over an array
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param num number of elements in this array
*/
#define a_foreach(T, it, ptr, num)                      \
    for (T *it = a_cast_s(T *, ptr),                    \
           *it##_ = a_likely(it) ? it + (num) : A_NULL; \
         it < it##_; ++it)

/*!
 @brief iterate over an array in reverse
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param num number of elements in this array
*/
#define a_foreach_reverse(T, it, ptr, num)                           \
    for (T *it##_ = a_likely(ptr) ? a_cast_s(T *, ptr) - 1 : A_NULL, \
           *it = a_likely(ptr) ? it##_ + (num) : A_NULL;             \
         it > it##_; --it)

/*!
 @brief iterate over an array
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param end the end address of this array
*/
#define a_iterate(T, it, ptr, end) \
    for (T *it = a_cast_s(T *, ptr), *it##_ = a_cast_s(T *, end); it < it##_; ++it)

/*!
 @brief iterate over an array in reverse
 @param T the element type in this array
 @param it pointer to the current element
 @param ptr starting address of this array
 @param end the end address of this array
*/
#define a_iterate_reverse(T, it, ptr, end)                           \
    for (T *it##_ = a_likely(ptr) ? a_cast_s(T *, ptr) - 1 : A_NULL, \
           *it = a_likely(end) ? a_cast_s(T *, end) - 1 : A_NULL;    \
         it > it##_; --it)

/*!
 @brief enumeration for return values
*/
enum
{
    A_SUCCESS /*!< return success */,
    A_FAILURE /*!< return failure */,
    A_INVALID /*!< return invalid */
};

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_f32_t a_f32_from(a_u32_t x);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_f32_t a_f32_from(a_u32_t x)
{
    union
    {
        a_u32_t u;
        a_f32_t x;
    } u;
    u.u = x;
    return u.x;
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_u32_t a_f32_into(a_f32_t x);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_u32_t a_f32_into(a_f32_t x)
{
    union
    {
        a_f32_t x;
        a_u32_t u;
    } u;
    u.x = x;
    return u.u;
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_f64_t a_f64_from(a_u64_t x);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_f64_t a_f64_from(a_u64_t x)
{
    union
    {
        a_u64_t u;
        a_f64_t x;
    } u;
    u.u = x;
    return u.x;
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_u64_t a_f64_into(a_f64_t x);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_u64_t a_f64_into(a_f64_t x)
{
    union
    {
        a_f64_t x;
        a_u64_t u;
    } u;
    u.x = x;
    return u.u;
}
#endif /* A_HAVE_INLINE */

/*!
 @brief swap two different memory blocks of the same size
 @param[in] siz the size of memory block being swapped
 @param[in,out] lhs points to memory block on the left
 @param[in,out] rhs points to memory block on the right
*/
A_PUBLIC a_void_t a_swap(a_size_t siz, a_vptr_t lhs, a_vptr_t rhs);

#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_void_t a_swap1(a_vptr_t lhs, a_vptr_t rhs);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_void_t a_swap1(a_vptr_t lhs, a_vptr_t rhs)
{
    *a_u8_p(lhs) ^= *a_u8_p(rhs);
    *a_u8_p(rhs) ^= *a_u8_p(lhs);
    *a_u8_p(lhs) ^= *a_u8_p(rhs);
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_void_t a_swap2(a_vptr_t lhs, a_vptr_t rhs);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_void_t a_swap2(a_vptr_t lhs, a_vptr_t rhs)
{
    *a_u16_p(lhs) ^= *a_u16_p(rhs);
    *a_u16_p(rhs) ^= *a_u16_p(lhs);
    *a_u16_p(lhs) ^= *a_u16_p(rhs);
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_void_t a_swap4(a_vptr_t lhs, a_vptr_t rhs);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_void_t a_swap4(a_vptr_t lhs, a_vptr_t rhs)
{
    *a_u32_p(lhs) ^= *a_u32_p(rhs);
    *a_u32_p(rhs) ^= *a_u32_p(lhs);
    *a_u32_p(lhs) ^= *a_u32_p(rhs);
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_void_t a_swap8(a_vptr_t lhs, a_vptr_t rhs);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_void_t a_swap8(a_vptr_t lhs, a_vptr_t rhs)
{
    *a_u64_p(lhs) ^= *a_u64_p(rhs);
    *a_u64_p(rhs) ^= *a_u64_p(lhs);
    *a_u64_p(lhs) ^= *a_u64_p(rhs);
}
#endif /* A_HAVE_INLINE */
#if !defined A_HAVE_INLINE || defined(A_A_I)
A_PUBLIC a_void_t a_swapz(a_vptr_t lhs, a_vptr_t rhs);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_A_I)
A_INTERN a_void_t a_swapz(a_vptr_t lhs, a_vptr_t rhs)
{
    *a_size_p(lhs) ^= *a_size_p(rhs);
    *a_size_p(rhs) ^= *a_size_p(lhs);
    *a_size_p(lhs) ^= *a_size_p(rhs);
}
#endif /* A_HAVE_INLINE */

/*!
 @brief Brian Kernighan and Dennis Ritchie
 @param[in] str string to be processed
 @param[in] val initial value
 @return hash value
*/
A_PUBLIC a_umax_t a_hash_bkdr(a_cptr_t str, a_umax_t val);
A_PUBLIC a_umax_t a_hash_bkdrn(a_cptr_t ptr, a_size_t siz, a_umax_t val);

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A */

#endif /* A_A_H */
