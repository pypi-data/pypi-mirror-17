/* vim: ft=c:ts=4:sta:sw=4:et:ai
 ****************************************************************** C FILE ****
 *
 *   COPYRIGHT (C) 2014 by Sebastian Stigler
 *
 *   NAME
 *       forbidden.c
 *
 *   DESCRIPTION
 *       Faengt 'system', 'execl', 'execlp', 'execle', 'execv', 'execvp' oder
                'execvpe' ab.
 *
 *   FIRST RELEASE
 *       2014-01-29  Sebastian Stigler		sebastian.stigler@htw-aalen.de
 *
 *****************************************************************************/
void emit(const char*);

int execl(const char *path, const char *arg, ...) {
    emit(">>>Sie haben den 'execl' Aufruf verwendet!<<<");
    return -1;
}

int execlp(const char *file, const char *arg, ...) {
    emit(">>>Sie haben den 'execlp' Aufruf verwendet!<<<");
    return -1;
}
int execle(const char *path, const char *arg, ...) {
    emit(">>>Sie haben den 'execle' Aufruf verwendet!<<<");
    return -1;
}
int execv(const char *path, char *const argv[]) {
    emit(">>>Sie haben den 'execv' Aufruf verwendet!<<<");
    return -1;
}
int execvp(const char *file, char *const argv[]) {
    emit(">>>Sie haben den 'execvp' Aufruf verwendet!<<<");
    return -1;
}
int execvpe(const char *file, char *const argv[], char *const envp[]) {
    emit(">>>Sie haben den 'execvpe' Aufruf verwendet!<<<");
    return -1;
}

int system(const char *command) {
    emit(">>>Sie haben den 'system' Aufruf verwendet!<<<");
    return -1;
}

int getchar(void) {
    emit(">>>Sie haben den 'getchar' Aufruf verwendet!<<<");
    return -1;
}
/********************************************************************* END ***/
