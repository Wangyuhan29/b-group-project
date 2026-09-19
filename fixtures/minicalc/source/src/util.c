#include "util.h"
#include "legacy.h"

#include <stdio.h>
#include <stdlib.h>

void legacy_die_hook(void) {
    /* C2：恢复对遗留头文件的引用，使 util.o 真正读取 legacy.h。 */
}

void die(const char *msg) {
    legacy_die_hook();
    fprintf(stderr, "%s\n", msg);
    exit(1);
}
