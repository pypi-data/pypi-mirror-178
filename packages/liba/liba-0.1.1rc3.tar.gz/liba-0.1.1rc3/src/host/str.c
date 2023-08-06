#if defined(_MSC_VER)
#if !defined _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_WARNINGS
#endif /* _CRT_SECURE_NO_WARNINGS */
#endif /* _MSC_VER */
#include "a/host/str.h"
#include <stdio.h>

a_str_s *a_str_new(void)
{
    a_str_s *ctx = (a_str_s *)malloc(sizeof(a_str_s));
    if (ctx)
    {
        a_str_ctor(ctx);
    }
    return ctx;
}

a_void_t a_str_die(a_str_s *ctx)
{
    if (ctx)
    {
        a_str_dtor(ctx);
        free(ctx);
    }
}

a_void_t a_str_ctor(a_str_s *ctx)
{
    ctx->_str = A_NULL;
    ctx->_num = 0;
    ctx->_mem = 0;
}

a_void_t a_str_dtor(a_str_s *ctx)
{
    if (ctx->_str)
    {
        free(ctx->_str);
        ctx->_str = A_NULL;
    }
    ctx->_num = 0;
    ctx->_mem = 0;
}

a_int_t a_str_init(a_str_s *ctx, a_cptr_t pdata, a_size_t nbyte)
{
    ctx->_num = nbyte;
    ctx->_mem = nbyte + 1;
    ctx->_mem = a_align(sizeof(a_vptr_t), ctx->_mem);
    ctx->_str = a_str_c(malloc(ctx->_mem));
    if (a_unlikely(ctx->_str == A_NULL))
    {
        return A_FAILURE;
    }
    if (pdata && nbyte)
    {
        memcpy(ctx->_str, pdata, nbyte);
    }
    ctx->_str[ctx->_num] = 0;
    return A_SUCCESS;
}

a_int_t a_str_copy(a_str_s *ctx, const a_str_s *obj)
{
    return a_str_init(ctx, obj->_str, obj->_num);
}

a_str_s *a_str_move(a_str_s *ctx, a_str_s *obj)
{
    memcpy(ctx, obj, sizeof(*obj));
    memset(obj, 0, sizeof(*obj));
    return ctx;
}

a_str_t a_str_exit(a_str_s *ctx)
{
    a_str_t str = ctx->_str;
    if (ctx->_str)
    {
        ctx->_str[ctx->_num] = 0;
        ctx->_str = A_NULL;
    }
    ctx->_mem = 0;
    ctx->_num = 0;
    return str;
}

a_int_t a_str_cmp(const a_str_s *lhs, const a_str_s *rhs)
{
    a_int_t ok = 0;
    if (lhs->_str && rhs->_str)
    {
        a_size_t num = lhs->_num < rhs->_num ? lhs->_num : rhs->_num;
        ok = memcmp(lhs->_str, rhs->_str, num);
    }
    if (ok)
    {
        return ok;
    }
    if (lhs->_num == rhs->_num)
    {
        return 0;
    }
    return lhs->_num < rhs->_num ? -1 : 1;
}

a_int_t a_str_alloc_(a_str_s *ctx, a_size_t mem)
{
    a_str_t str;
    mem = a_align(sizeof(a_vptr_t), mem);
    str = a_str_c(realloc(ctx->_str, mem));
    if (a_unlikely(!str && mem))
    {
        return A_FAILURE;
    }
    ctx->_str = str;
    ctx->_mem = mem;
    return A_SUCCESS;
}

a_int_t a_str_alloc(a_str_s *ctx, a_size_t mem)
{
    return ctx->_mem < mem ? a_str_alloc_(ctx, mem) : A_SUCCESS;
}

a_int_t a_str_getc_(a_str_s *ctx)
{
    a_int_t c = EOF;
    if (ctx->_num)
    {
        c = a_int_c(ctx->_str[--ctx->_num]);
    }
    return c;
}

a_int_t a_str_getc(a_str_s *ctx)
{
    a_int_t c = EOF;
    if (ctx->_num)
    {
        c = a_int_c(ctx->_str[--ctx->_num]);
        ctx->_str[ctx->_num] = 0;
    }
    return c;
}

a_int_t a_str_putc_(a_str_s *ctx, a_int_t c)
{
    if (a_unlikely(a_str_alloc(ctx, ctx->_num + 1)))
    {
        return EOF;
    }
    ctx->_str[ctx->_num++] = a_char_c(c);
    return c;
}

a_int_t a_str_putc(a_str_s *ctx, a_int_t c)
{
    if (a_unlikely(a_str_alloc(ctx, ctx->_num + 2)))
    {
        return EOF;
    }
    ctx->_str[ctx->_num++] = a_char_c(c);
    ctx->_str[ctx->_num] = 0;
    return c;
}

a_int_t a_str_putn_(a_str_s *ctx, a_cptr_t pdata, a_size_t nbyte)
{
    if (pdata && nbyte)
    {
        if (a_unlikely(a_str_alloc(ctx, ctx->_num + nbyte)))
        {
            return A_FAILURE;
        }
        memcpy(ctx->_str + ctx->_num, pdata, nbyte);
        ctx->_num += nbyte;
    }
    return A_SUCCESS;
}

a_int_t a_str_putn(a_str_s *ctx, a_cptr_t pdata, a_size_t nbyte)
{
    if (pdata)
    {
        if (a_unlikely(a_str_alloc(ctx, ctx->_num + nbyte + 1)))
        {
            return A_FAILURE;
        }
        if (nbyte)
        {
            memcpy(ctx->_str + ctx->_num, pdata, nbyte);
            ctx->_num += nbyte;
        }
        ctx->_str[ctx->_num] = 0;
    }
    return A_SUCCESS;
}

a_int_t a_str_puts(a_str_s *ctx, a_cptr_t str)
{
    return a_str_putn(ctx, str, strlen(a_char_P(str)));
}

a_int_t a_str_cat(a_str_s *ctx, const a_str_s *obj)
{
    return a_str_putn(ctx, obj->_str, obj->_num);
}

a_int_t a_str_vprintf(a_str_s *ctx, a_cstr_t fmt, va_list va)
{
    a_size_t siz;
    a_size_t mem;
    a_str_t str;
    a_int_t num;
    va_list ap;
    va_copy(ap, va);
    mem = ctx->_mem - ctx->_num;
    str = ctx->_str ? ctx->_str + ctx->_num : A_NULL;
    num = vsnprintf(str, mem, fmt, ap);
    va_end(ap);
    siz = a_size_c(num) + 1;
    if (siz > mem)
    {
        if (a_unlikely(a_str_alloc_(ctx, ctx->_num + siz)))
        {
            return EOF;
        }
        va_copy(ap, va);
        mem = ctx->_mem - ctx->_num;
        str = ctx->_str + ctx->_num;
        num = vsnprintf(str, mem, fmt, ap);
        va_end(ap);
    }
    ctx->_num += a_size_c(num);
    return num;
}

a_int_t a_str_printf(a_str_s *ctx, a_cstr_t fmt, ...)
{
    va_list va;
    va_start(va, fmt);
    a_int_t num = a_str_vprintf(ctx, fmt, va);
    va_end(va);
    return num;
}
