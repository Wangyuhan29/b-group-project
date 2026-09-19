#include <stdio.h>
#include <string.h>

#include "config.h"
#include "parser.h"
#include "util.h"

int main(int argc, char **argv) {
    if (argc < 2) {
        die("usage: minicalc \"<expression>\"");
    }
    if (strcmp(argv[1], "--version") == 0 || strcmp(argv[1], "-v") == 0) {
        printf("%s %s\n", APP_NAME, APP_VERSION);
        return 0;
    }
    printf("%ld\n", eval_expr(argv[1]));
    return 0;
}
