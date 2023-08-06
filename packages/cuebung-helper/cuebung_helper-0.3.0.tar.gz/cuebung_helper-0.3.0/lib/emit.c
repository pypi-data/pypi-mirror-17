/* vim: ft=c:ts=4:sta:sw=4:et:ai
 ****************************************************************** C FILE ****
 *
 *   COPYRIGHT (C) 2016 by Sebastian Stigler
 *
 *   NAME
 *       emit.c -- emit to stderr or to a named pipe
 *
 *   FIRST RELEASE
 *       2016-07-15  Sebastian Stigler		sebastian.stigler@hs-aalen.de
 *
 *****************************************************************************/
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

void emit(const char* txt) {
    FILE *output;
    char *errorfifo = "error";
    struct stat status;
    if (stat(errorfifo, &status) != 0 || !S_ISFIFO(status.st_mode) ||
            (output = fopen(errorfifo, "a")) == NULL) {
        fprintf(stderr, "\n%s\n", txt);
    } else {
        fprintf(output, "%s\n", txt);
        fflush(output);
    }
}
/********************************************************************* END ***/
