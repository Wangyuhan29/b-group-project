# strace 原始跟踪证据（Minicalc c0，WSL Ubuntu x86_64）

生成时间：2026-10-09T12:40:25Z

## 构建命令输出（make.stdout）
```
gcc -std=c11 -Wall -Wextra -Iinclude -g -c src/main.c -o main.o
gcc -std=c11 -Wall -Wextra -Iinclude -g -c src/parser.c -o parser.o
gcc -std=c11 -Wall -Wextra -Iinclude -g -c src/token.c -o token.o
gcc -std=c11 -Wall -Wextra -Iinclude -g -c src/util.c -o util.o
gcc -std=c11 -Wall -Wextra -Iinclude -g main.o parser.o token.o util.o -o minicalc
```

## make -pn 中 .o 声明规则
```
789:parser.o: src/parser.c include/parser.h
806:util.o: src/util.c include/util.h include/legacy.h
1101:main.o: src/main.c include/config.h include/parser.h
1270:token.o: src/token.c include/token.h
```

## 各 trace 文件对应进程
```
trace.log.3876 -> 
trace.log.3877 -> 
trace.log.3878 -> 
trace.log.3879 -> 
trace.log.3880 -> 
trace.log.3881 -> 
trace.log.3882 -> 
trace.log.3883 -> 
trace.log.3884 -> 
trace.log.3885 -> 
trace.log.3886 -> 
trace.log.3887 -> 
trace.log.3888 -> 
trace.log.3889 -> 
trace.log.3890 -> 
trace.log.3891 -> 
```

## 头文件访问分类（newfstatat = make 检查状态；openat = 编译器实际读取）
```
--- config.h ---
stat(状态检查)次数: 0
openat(实际读取)次数: 0
--- parser.h ---
stat(状态检查)次数: 0
openat(实际读取)次数: 0
--- token.h ---
stat(状态检查)次数: 0
openat(实际读取)次数: 0
--- util.h ---
stat(状态检查)次数: 0
openat(实际读取)次数: 0
--- legacy.h ---
stat(状态检查)次数: 0
openat(实际读取)次数: 0
```
