#define A_A_I
#include "inline.h"
#include "a/a.h"
#include "intern.h"

a_void_t a_swap(a_size_t siz, a_vptr_t lhs, a_vptr_t rhs)
{
    a_byte_t *l = a_byte_p(lhs);
    a_byte_t *r = a_byte_p(rhs);
    for (a_byte_t *d = r + siz; r != d; ++l, ++r)
    {
        *l ^= *r;
        *r ^= *l;
        *l ^= *r;
    }
}

a_umax_t a_hash_bkdr(a_cptr_t str, a_umax_t val)
{
    if (str)
    {
        for (const a_u8_t *p = a_u8_P(str); *p; ++p)
        {
            val = val * 131 + *p;
        }
    }
    return val;
}

a_umax_t a_hash_bkdrn(a_cptr_t ptr, a_size_t siz, a_umax_t val)
{
    if (ptr && siz)
    {
        for (const a_u8_t *p = a_u8_P(ptr); siz--; ++p)
        {
            val = val * 131 + *p;
        }
    }
    return val;
}
