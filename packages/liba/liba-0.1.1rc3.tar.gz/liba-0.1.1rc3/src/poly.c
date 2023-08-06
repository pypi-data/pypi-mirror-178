#include "a/poly.h"

a_real_t *a_poly_inv(a_real_t *a, a_size_t n)
{
    for (a_real_t *l = a, *r = a + n - 1, *m = a + (n >> 1); l < m; ++l, --r)
    {
        a_swap(sizeof(a_real_t), l, r);
    }
    return a;
}

a_real_t a_poly_eval(const a_real_t *a, a_size_t n, a_real_t x)
{
    a_real_t y = 0;
    for (const a_real_t *p = --a + n; p > a; --p)
    {
        y = y * x + *p;
    }
    return y;
}

a_real_t *a_poly_evaln(const a_real_t *a, a_size_t n, const a_real_t *ptr, a_size_t num, a_real_t *out)
{
    a_real_t x; /* when ptr == out, cache it */
    for (const a_real_t *p = --a + n; num--; ++ptr, ++out)
    {
        x = *ptr;
        *out = 0;
        for (const a_real_t *q = p; q > a; --q)
        {
            *out = *out * x + *q;
        }
    }
    return out;
}

a_real_t a_poly_evar(const a_real_t *a, a_size_t n, a_real_t x)
{
    a_real_t y = 0;
    for (const a_real_t *q = a + n; a < q; ++a)
    {
        y = y * x + *a;
    }
    return y;
}

a_real_t *a_poly_evarn(const a_real_t *a, a_size_t n, const a_real_t *ptr, a_size_t num, a_real_t *out)
{
    a_real_t x; /* when ptr == out, cache it */
    for (const a_real_t *q = a + n; num--; ++ptr, ++out)
    {
        x = *ptr;
        *out = 0;
        for (const a_real_t *p = a; p < q; ++p)
        {
            *out = *out * x + *p;
        }
    }
    return out;
}
