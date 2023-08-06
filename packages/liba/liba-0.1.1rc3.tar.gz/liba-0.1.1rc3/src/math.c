#include "math.h"

a_f64_t a_f64_sq(a_f64_t x, a_f64_t *p)
{
#undef K
#if defined(_MSC_VER) && (_MSC_VER < 1914)
    const union
    {
        a_u64_t u;
        a_f64_t x;
    } k = {A_U64_C(0x41A0000000000000)};
#define K k.x
#else
#define K A_F64_C(0x1P27)
#endif
    a_f64_t xh, xl, xc;
    xc = x * (K + 1);
    xh = x - xc + xc;
    xl = x - xh;
    x *= x;
    *p = xh * xh - x + 2 * xh * xl + xl * xl;
    return x;
#undef K
}

#undef a_f32_hypot
a_f32_t a_f32_hypot(a_f32_t x, a_f32_t y)
{
#undef NEG
#undef POS
#if defined(_MSC_VER) && (_MSC_VER < 1914)
    const union
    {
        a_u32_t u;
        a_f32_t x;
    } pos = {A_U32_C(0x6C800000)},
      neg = {A_U32_C(0x12800000)};
#define POS pos.x
#define NEG neg.x
#else
#define POS A_F32_C(0x1P+90)
#define NEG A_F32_C(0x1P-90)
#endif
    union
    {
        a_f32_t x;
        a_u32_t u;
    } ux, uy;
    a_f32_t z;

    ux.x = x;
    uy.x = y;
    ux.u &= A_U32_C(~0) >> 1;
    uy.u &= A_U32_C(~0) >> 1;
    if (ux.u < uy.u)
    {
        ux.u ^= uy.u;
        uy.u ^= ux.u;
        ux.u ^= uy.u;
    }

    x = ux.x;
    y = uy.x;
    if (uy.u == 0xFF << 23)
    {
        return y;
    }
    if (ux.u >= 0xFF << 23 || uy.u == 0 || ux.u - uy.u >= 25 << 23)
    {
        return x + y;
    }

    z = 1;
    if (ux.u >= (0x7F + 60) << 23)
    {
        z = POS;
        x *= NEG;
        y *= NEG;
    }
    else if (uy.u < (0x7F - 60) << 23)
    {
        z = NEG;
        x *= POS;
        y *= POS;
    }
    return z * a_f32_sqrt(a_f32_c(a_f64_c(x) * a_f64_c(x) + a_f64_c(y) * a_f64_c(y)));
#undef NEG
#undef POS
}

#undef a_f64_hypot
a_f64_t a_f64_hypot(a_f64_t x, a_f64_t y)
{
#undef NEG
#undef POS
#if defined(_MSC_VER) && (_MSC_VER < 1914)
    const union
    {
        a_u64_t u;
        a_f64_t x;
    } pos = {A_U64_C(0x6BB0000000000000)},
      neg = {A_U64_C(0x1430000000000000)};
#define POS pos.x
#define NEG neg.x
#else
#define POS A_F64_C(0x1P+700)
#define NEG A_F64_C(0x1P-700)
#endif
    union
    {
        a_f64_t x;
        a_u64_t u;
    } ux, uy;
    a_int_t ex, ey;
    a_f64_t hx, lx, hy, ly, z;

    ux.x = x;
    uy.x = y;
    ux.u &= A_U64_C(~0) >> 1;
    uy.u &= A_U64_C(~0) >> 1;
    if (ux.u < uy.u)
    {
        ux.u ^= uy.u;
        uy.u ^= ux.u;
        ux.u ^= uy.u;
    }

    x = ux.x;
    y = uy.x;
    ex = a_int_c(ux.u >> 52);
    ey = a_int_c(uy.u >> 52);
    /* hypot(inf,nan) == inf */
    if (ey == 0x7FF)
    {
        return y;
    }
    if (ex == 0x7FF || uy.u == 0)
    {
        return x;
    }
    if (ex - ey > 64)
    {
        return x + y;
    }

    z = 1;
    if (ex > 0x3FF + 510)
    {
        z = POS;
        x *= NEG;
        y *= NEG;
    }
    else if (ey < 0x3FF - 450)
    {
        z = NEG;
        x *= POS;
        y *= POS;
    }
    hx = a_f64_sq(x, &lx);
    hy = a_f64_sq(y, &ly);
    return z * a_f64_sqrt(ly + lx + hy + hx);
#undef NEG
#undef POS
}

a_f32_t a_sqrt_inv(a_f32_t x)
{
    union
    {
        a_f32_t x;
        a_u32_t u;
    } u;
    u.x = x;
    if (a_likely(x > 0))
    {
        a_f32_t xh = A_F32_C(0.5) * x;
        u.u = A_U32_C(0x5F3759DF) - (u.u >> 1);
        u.x *= A_F32_C(1.5) - u.x * u.x * xh;
        u.x *= A_F32_C(1.5) - u.x * u.x * xh;
    }
    else if (x < 0)
    {
        u.u = A_F32_NNAN;
    }
    else
    {
        u.u |= A_F32_PINF;
    }
    return u.x;
}

a_u32_t a_u32_sqrt(a_u32_t x, a_u32_t *p)
{
    a_u32_t y = 0;
    for (a_uint_t i = 0; i < 32; i += 2)
    {
        a_u32_t k = A_U32_C(0x40000000) >> i;
        a_u32_t j = y + k;
        if (x >= j)
        {
            x -= j;
            y = (y >> 1) | k;
        }
        else
        {
            y >>= 1;
        }
    }
    if (p)
    {
        *p = x;
    }
    return y;
}

a_u64_t a_u64_sqrt(a_u64_t x, a_u64_t *p)
{
    a_u64_t y = 0;
    for (a_uint_t i = 0; i < 64; i += 2)
    {
        a_u64_t k = A_U64_C(0x4000000000000000) >> i;
        a_u64_t j = y + k;
        if (x >= j)
        {
            x -= j;
            y = (y >> 1) | k;
        }
        else
        {
            y >>= 1;
        }
    }
    if (p)
    {
        *p = x;
    }
    return y;
}
