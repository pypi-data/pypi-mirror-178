/*!
 @file version.hpp
 @brief algorithm library version
 @copyright Copyright (C) 2020-present tqfx, All rights reserved.
*/

#ifndef A_VERSION_HPP
#define A_VERSION_HPP

#include "a.hpp"
#include "a/version.h"

namespace a
{
/*!
 @ingroup AA
 @addtogroup AA_VERSION algorithm library version based on C++
 @{
*/

/*!
 @brief enumeration for algorithm library version
*/
enum
{
    VERSION_MAJOR = A_VERSION_MAJOR,
    VERSION_MINOR = A_VERSION_MINOR,
    VERSION_PATCH = A_VERSION_PATCH
};

/*!
 @brief algorithm library version string
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_IPP)
A_PUBLIC cstr_t version(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_IPP)
A_INTERN cstr_t version(void)
{
    return A_VERSION;
}
#endif /* A_HAVE_INLINE */

/*!
 @brief algorithm library version major
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_IPP)
A_PUBLIC uint_t version_major(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_IPP)
A_INTERN uint_t version_major(void)
{
    return A_VERSION_MAJOR;
}
#endif /* A_HAVE_INLINE */
/*!
 @brief algorithm library version minor
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_IPP)
A_PUBLIC uint_t version_minor(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_IPP)
A_INTERN uint_t version_minor(void)
{
    return A_VERSION_MINOR;
}
#endif /* A_HAVE_INLINE */
/*!
 @brief algorithm library version patch
*/
#if !defined A_HAVE_INLINE || defined(A_VERSION_IPP)
A_PUBLIC uint_t version_patch(void);
#endif /* A_HAVE_INLINE */
#if defined(A_HAVE_INLINE) || defined(A_VERSION_IPP)
A_INTERN uint_t version_patch(void)
{
    return A_VERSION_PATCH;
}
#endif /* A_HAVE_INLINE */

/*! @} AA_VERSION */
} // namespace a

#endif /* A_VERSION_HPP */
