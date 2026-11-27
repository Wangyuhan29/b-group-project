# minicalc —— 用于 DevOps E2 BuildChecker/EChecker 测试的小型 C 项目
#
# 说明：本 Makefile 刻意没有完整声明真实头文件依赖（模拟真实项目常见缺陷），
# 供 BuildChecker 检出 MISSING / REDUNDANT 发现。预期发现见 README.md。
#
# 跨平台：Windows（MinGW）下产物为 minicalc.exe，Unix/Linux 下为 minicalc。

CC      := gcc
CFLAGS  := -std=c11 -Wall -Wextra -Iinclude -g
OBJS    := main.o parser.o token.o util.o

EXE := minicalc
ifeq ($(OS),Windows_NT)
EXE := minicalc.exe
endif

ifeq ($(OS),Windows_NT)
RUN := $(EXE)
RM  := del /Q
else
RUN := ./$(EXE)
RM  := rm -f
endif

.PHONY: all clean test

all: $(EXE)

# 刻意缺陷：main.c 实际还 #include "util.h"，并经 parser.h 间接包含 "token.h"，但规则均未声明 -> MISSING ×2
main.o: src/main.c include/config.h include/parser.h
	$(CC) $(CFLAGS) -c $< -o $@

# 刻意缺陷：parser.c 实际经 parser.h 传递包含 "token.h"，但规则未声明 -> MISSING
parser.o: src/parser.c include/parser.h
	$(CC) $(CFLAGS) -c $< -o $@

token.o: src/token.c include/token.h
	$(CC) $(CFLAGS) -c $< -o $@

# 刻意缺陷：规则声明了 include/legacy.h，但编译 util.o 时从未读取 -> REDUNDANT
util.o: src/util.c include/util.h include/legacy.h
	$(CC) $(CFLAGS) -c $< -o $@

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

test: all
	@echo "== 1+2*3   => expect 7"
	$(RUN) "1+2*3"
	@echo "== 10-4/2  => expect 8"
	$(RUN) "10-4/2"
	@echo "== 3*(4+5) => expect 27"
	$(RUN) "3*(4+5)"

clean:
	$(RM) $(OBJS) $(EXE)
