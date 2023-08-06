main = testat-0
CC = gcc-4.4
CFLAGS = -Wall -g

FORBIDDENSOURCE   = forbidden.c
FORBIDDENSHDLIB   = $(FORBIDDENSOURCE:.c=.so)
test: all
all : $(main) $(FORBIDDENSHDLIB)

$(main) : $(main).c
	@$(CC) $(CFLAGS) $< -o $(main)

$(FORBIDDENSHDLIB): $(FORBIDDENSOURCE)
	@$(CC) $(CFLAGS) -shared -fPIC -rdynamic  $< -o $@

.PHONY : clean
clean :
	@rm -f $(main)
