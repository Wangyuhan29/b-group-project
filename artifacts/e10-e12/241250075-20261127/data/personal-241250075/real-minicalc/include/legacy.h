#ifndef MINICALC_LEGACY_H
#define MINICALC_LEGACY_H

/* 遗留兼容头文件：C0/C1 时无人引用（REDUNDANT）；
 * C2 起被 util.c 重新使用，使冗余声明变为真实依赖。 */

#define LEGACY_COMPAT 1

/* 遗留的退出前兼容钩子：C2 起由 util.c 实现并在 die() 中调用。 */
void legacy_die_hook(void);

#endif
