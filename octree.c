#include <stdlib.h>

#define TREE_SIZE 19173961
#define COLORS 16777216

static int LOOKUP[8][8] = {
    {0, 1, 4, 5, 2, 3, 6, 7},
    {1, 0, 5, 4, 3, 2, 7, 6},
    {2, 3, 6, 7, 0, 1, 4, 5},
    {3, 2, 7, 6, 1, 0, 5, 4},
    {4, 5, 0, 1, 6, 7, 2, 3},
    {5, 4, 1, 0, 7, 6, 3, 2},
    {6, 7, 2, 3, 4, 5, 0, 1},
    {7, 6, 3, 2, 5, 4, 1, 0}
};

int *allocate() {
    return malloc(sizeof(int) * TREE_SIZE);
}

void deallocate(int *tree) {
    free(tree);
}

void _initialize(int *tree, int index, int value) {
    tree[index] = value;
    if (value == 1) {
        return;
    }
    value /= 8;
    for (int i = 0; i < 8; i++) {
        _initialize(tree, 8 * index + 1 + i, value);
    }
}

void initialize(int *tree) {
    _initialize(tree, 0, COLORS);
}

void pop(int *tree, int *r, int *g, int *b) {
    int path[8];
    int dr = *r;
    int dg = *g;
    int db = *b;
    for (int i = 7; i >= 0; i--) {
        int br = dr & 1;
        int bg = dg & 1;
        int bb = db & 1;
        path[i] = (br << 2) | (bg << 1) | (bb << 0);
        dr >>= 1;
        dg >>= 1;
        db >>= 1;
    }
    int index = 0;
    for (int i = 0; i < 8; i++) {
        int base = 8 * index + 1;
        for (int j = 0; j < 8; j++) {
            int child = LOOKUP[path[i]][j];
            int new_index = base + child;
            if (tree[new_index]) {
                path[i] = child;
                tree[new_index]--;
                index = new_index;
                break;
            }
        }
    }
    int pr = 0;
    int pg = 0;
    int pb = 0;
    for (int i = 0; i < 8; i++) {
        pr <<= 1;
        pg <<= 1;
        pb <<= 1;
        pr |= (path[i] >> 2) & 1;
        pg |= (path[i] >> 1) & 1;
        pb |= (path[i] >> 0) & 1;
    }
    *r = pr;
    *g = pg;
    *b = pb;
}

void apply(int *colors, int *indexes) {
    int *tree = allocate();
    initialize(tree);
    for (int i = 0; i < COLORS; i++) {
        int index = indexes[i];
        int color = colors[index];
        int r = 0xff & (color >> 16);
        int g = 0xff & (color >> 8);
        int b = 0xff & (color >> 0);
        pop(tree, &r, &g, &b);
        colors[index] = (r << 16) | (g << 8) | (b);
    }
    deallocate(tree);
}
