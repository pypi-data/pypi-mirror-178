/*!
 @file version.h
 @brief algorithm library version
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef A_VERSION_H
#define A_VERSION_H

#include "a.h"

/*!
 @ingroup A
 @addtogroup A_VERSION algorithm library version based on C
 @{
*/

/*! algorithm library version major */
#ifndef A_VERSION_MAJOR
#define A_VERSION_MAJOR 0
#endif /* A_VERSION_MAJOR */

/*! algorithm library version minor */
#ifndef A_VERSION_MINOR
#define A_VERSION_MINOR 0
#endif /* A_VERSION_MINOR */

/*! algorithm library version patch */
#ifndef A_VERSION_PATCH
#define A_VERSION_PATCH 0
#endif /* A_VERSION_PATCH */

/*! algorithm library version tweak */
#ifndef A_VERSION_TWEAK
#define A_VERSION_TWEAK A_U64_C(0)
#endif /* A_VERSION_TWEAK */

/*! algorithm library version string */
#ifndef A_VERSION
#define A_VERSION "0.0.0"
#endif /* A_VERSION */

#if defined(__cplusplus)
extern "C" {
#endif /* __cplusplus */

/*!
 @brief algorithm library version string
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_I)
A_PUBLIC a_cstr_t a_version(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_I)
A_INTERN a_cstr_t a_version(void)
{
    return A_VERSION;
}
#endif /* A_HAVE_INLINE */

/*!
 @brief algorithm library version major
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_I)
A_PUBLIC a_uint_t a_version_major(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_I)
A_INTERN a_uint_t a_version_major(void)
{
    return A_VERSION_MAJOR;
}
#endif /* A_HAVE_INLINE */

/*!
 @brief algorithm library version minor
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_I)
A_PUBLIC a_uint_t a_version_minor(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_I)
A_INTERN a_uint_t a_version_minor(void)
{
    return A_VERSION_MINOR;
}
#endif /* A_HAVE_INLINE */

/*!
 @brief algorithm library version patch
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_I)
A_PUBLIC a_uint_t a_version_patch(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_I)
A_INTERN a_uint_t a_version_patch(void)
{
    return A_VERSION_PATCH;
}
#endif /* A_HAVE_INLINE */

#if defined(__cplusplus)
} /* extern "C" */
#endif /* __cplusplus */

/*! @} A_VERSION */

#endif /* A_VERSION_H */
