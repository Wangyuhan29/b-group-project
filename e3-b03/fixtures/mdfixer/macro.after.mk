CC = cc
CFLAGS = -std=c11 -Wall -Wextra -Werror
DEPS = main.c config.h
app: main.o
	$(CC) main.o -o app
main.o: $(DEPS)
	$(CC) $(CFLAGS) -c main.c -o main.o
clean:
	rm -f app main.o main.d
