/* vim: ft=c:ts=4:sta:sw=4:et:ai
 ****************************************************************** C FILE ****
 *
 *   COPYRIGHT (C) 2016 by Sebastian Stigler
 *
 *   NAME
 *       testat-0.c
 *
 *   FIRST RELEASE
 *       2016-07-06  Sebastian Stigler		sebastian.stigler@hs-aalen.de
 *
 *****************************************************************************/

/******************************************************************************
*** loading standard io include-file */
#include <stdio.h>
#include <unistd.h>

/******************************************************************************
*** XXX */

int main() {
    int a, b, res;
    scanf("%d %d", &a, &b);

    res = (a + b)/2;
    printf("%d\n", res);
//    getchar();
//    getchar();
    return 0;
}
/********************************************************************* END ***/
