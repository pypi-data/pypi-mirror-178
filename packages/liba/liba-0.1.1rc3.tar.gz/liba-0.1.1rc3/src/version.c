#define A_VERSION_I
#include "a/a.h"
#undef A_INTERN
#define A_INTERN A_INLINE
#include "a/version.h"
#undef A_INTERN
