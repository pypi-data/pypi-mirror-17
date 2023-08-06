#include <stdio.h>
#include "reboundx.h"

int main(){
    enum rebx_type a = REBX_TYPE_DOUBLE;
    enum rebx_type b = REBX_TYPE_INT;
    enum rebx_type c = REBX_TYPE_UINT32;
    enum rebx_type d = REBX_TYPE_PARTICLE;
    enum rebx_type e = REBX_TYPE_EFFECT;

    printf("%d\t%d\t%d\t%d\t%d\n", a, b, c, d, e);
    return 1;
}
