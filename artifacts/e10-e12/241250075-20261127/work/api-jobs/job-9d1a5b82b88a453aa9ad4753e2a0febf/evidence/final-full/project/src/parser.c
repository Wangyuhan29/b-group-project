#include "parser.h"
#include "config.h"

#include <stdio.h>

static const Token *toks;
static int pos;

static long parse_expr(void);
static long parse_term(void);
static long parse_factor(void);

static Token peek(void) {
    return toks[pos];
}

static Token next_tok(void) {
    return toks[pos++];
}

static long parse_factor(void) {
    Token t = next_tok();
    if (t.kind == TOK_NUMBER) {
        return t.value;
    }
    if (t.kind == TOK_LPAREN) {
        long v = parse_expr();
        Token close = next_tok();
        if (close.kind != TOK_RPAREN) {
            fprintf(stderr, "error: expected ')'\n");
            return 0;
        }
        return v;
    }
    fprintf(stderr, "error: unexpected token\n");
    return 0;
}

static long parse_term(void) {
    long v = parse_factor();
    for (;;) {
        Token t = peek();
        if (t.kind == TOK_STAR) {
            next_tok();
            v = v * parse_factor();
        } else if (t.kind == TOK_SLASH) {
            next_tok();
            long d = parse_factor();
            if (d == 0) {
                fprintf(stderr, "error: division by zero\n");
                return 0;
            }
            v = v / d;
        } else {
            break;
        }
    }
    return v;
}

static long parse_expr(void) {
    long v = parse_term();
    for (;;) {
        Token t = peek();
        if (t.kind == TOK_PLUS) {
            next_tok();
            v = v + parse_term();
        } else if (t.kind == TOK_MINUS) {
            next_tok();
            v = v - parse_term();
        } else {
            break;
        }
    }
    return v;
}

long eval_expr(const char *expr) {
    static Token buf[TOKEN_CAPACITY];
    int n = tokenize(expr, buf, TOKEN_CAPACITY);
    if (n < 0) {
        fprintf(stderr, "error: cannot tokenize expression\n");
        return 0;
    }
    toks = buf;
    pos = 0;
    long v = parse_expr();
    Token t = next_tok();
    if (t.kind != TOK_END) {
        fprintf(stderr, "error: trailing characters\n");
        return 0;
    }
    return v;
}
