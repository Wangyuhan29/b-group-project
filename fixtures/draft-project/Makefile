.PHONY: all clean test
all: app
app: main.o
	$(CC) main.o -o app
main.o: main.c
	$(CC) -c main.c -o main.o
test: app
	@test "$$(./app)" = "$(EXPECTED)"
clean:
	rm -f app main.o
