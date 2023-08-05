CC = gcc-4.4
CFLAGS = -Wall -g

SOURCE=$(wildcard *.c)
LIBS=$(SOURCE:.c=.so)

all : $(LIBS)

%.so : %.c
	@$(CC) $(CFLAGS) -shared -fPIC -rdynamic  $< -o $@
