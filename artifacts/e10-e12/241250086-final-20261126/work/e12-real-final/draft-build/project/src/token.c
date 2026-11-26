#include "token.h"

#include <ctype.h>

int tokenize(const char *expr, Token *tokens, int cap) {
    const char *p = expr;
    int n = 0;

    while (*p != '\0') {
        while (isspace((unsigned char)*p)) {
            p++;
        }
        if (*p == '\0') {
            break;
        }
        if (n >= cap) {
            return -1;
        }

        Token t;
        t.kind = TOK_ERROR;
        t.value = 0;

        if (isdigit((unsigned char)*p)) {
            long v = 0;
            while (isdigit((unsigned char)*p)) {
                v = v * 10 + (long)(*p - '0');
                p++;
            }
            t.kind = TOK_NUMBER;
            t.value = v;
        } else {
            switch (*p) {
                case '+': t.kind = TOK_PLUS;   break;
                case '-': t.kind = TOK_MINUS;  break;
                case '*': t.kind = TOK_STAR;   break;
                case '/': t.kind = TOK_SLASH;  break;
                case '(': t.kind = TOK_LPAREN; break;
                case ')': t.kind = TOK_RPAREN; break;
                default:  t.kind = TOK_ERROR;  break;
            }
            p++;
        }

        if (t.kind == TOK_ERROR) {
            return -1;
        }
        tokens[n++] = t;
    }

    if (n >= cap) {
        return -1;
    }
    Token end;
    end.kind = TOK_END;
    end.value = 0;
    tokens[n++] = end;
    return n;
}
