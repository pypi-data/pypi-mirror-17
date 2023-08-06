#include "funcs.h"
void inf_loop(void) {
    while(1) {}
}

void segfault(void) {
    *(char *)0 = 0;
}
