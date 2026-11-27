#ifndef MINICALC_TOKEN_H
#define MINICALC_TOKEN_H

typedef enum {
    TOK_NUMBER,
    TOK_PLUS, TOK_MINUS, TOK_STAR, TOK_SLASH,
    TOK_LPAREN, TOK_RPAREN,
    TOK_END,
    TOK_ERROR
} TokenKind;

typedef struct {
    TokenKind kind;
    long value;              /* 仅当 kind == TOK_NUMBER 时有意义 */
} Token;

/* 将表达式字符串切分为 token 序列。
 * 返回写入 tokens 的 token 数量（含 TOK_END），失败返回 -1。
 * tokens 至少要有 cap 个元素的空间。 */
int tokenize(const char *expr, Token *tokens, int cap);

#endif
