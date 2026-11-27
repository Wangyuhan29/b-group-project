#ifndef MINICALC_PARSER_H
#define MINICALC_PARSER_H

#include "token.h"

/* 计算算术表达式（支持 + - * / 和括号），返回结果。
 * 出错时打印错误信息并返回 0。 */
long eval_expr(const char *expr);

#endif
