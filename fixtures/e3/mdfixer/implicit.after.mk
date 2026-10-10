CC = cc
CFLAGS = -std=c11 -Wall -Wextra -Werror
app: main.o
	$(CC) main.o -o app
%.o: %.c
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
-include main.d
clean:
	rm -f app main.o main.d
