from ctypes import CDLL, POINTER, c_int, byref

dll = CDLL('octree')

dll.allocate.restype = POINTER(c_int)
dll.allocate.argtypes = []
def dll_allocate():
    return dll.allocate()

dll.deallocate.restype = None
dll.deallocate.argtypes = [POINTER(c_int)]
def dll_deallocate(tree):
    dll.deallocate(tree)

dll.initialize.restype = None
dll.initialize.argtypes = [POINTER(c_int)]
def dll_initialize(tree):
    dll.initialize(tree)

dll.pop.restype = None
dll.pop.argtypes = [
    POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
def dll_pop(tree, r, g, b):
    r, g, b = c_int(r), c_int(g), c_int(b)
    dll.pop(tree, byref(r), byref(g), byref(b))
    return (r.value, g.value, b.value)

dll.apply.restype = None
dll.apply.argtypes = [POINTER(c_int), POINTER(c_int)]
def dll_apply(colors, indexes):
    colors = (c_int * len(colors))(*colors)
    indexes = (c_int * len(indexes))(*indexes)
    dll.apply(colors, indexes)
    return list(colors)

class Octree(object):
    def __init__(self):
        self.tree = dll_allocate()
        dll_initialize(self.tree)
    def __del__(self):
        dll_deallocate(self.tree)
    def pop(self, r, g, b):
        return dll_pop(self.tree, r, g, b)
