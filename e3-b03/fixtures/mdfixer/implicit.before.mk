CC = cc
CFLAGS = -std=c11 -Wall -Wextra -Werror
app: main.o
	$(CC) main.o -o app
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
clean:
	rm -f app main.o main.d
