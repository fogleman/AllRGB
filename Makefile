all: octree

octree: octree.c
	gcc -std=c99 -O3 -shared -o octree octree.c
