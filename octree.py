LOOKUP = [
    [0, 1, 4, 5, 2, 3, 6, 7],
    [1, 0, 5, 4, 3, 2, 7, 6],
    [2, 3, 6, 7, 0, 1, 4, 5],
    [3, 2, 7, 6, 1, 0, 5, 4],
    [4, 5, 0, 1, 6, 7, 2, 3],
    [5, 4, 1, 0, 7, 6, 3, 2],
    [6, 7, 2, 3, 4, 5, 0, 1],
    [7, 6, 3, 2, 5, 4, 1, 0],
]

class Octree(object):
    def __init__(self):
        self.data = [0] * sum(8 ** i for i in xrange(9))
        self.initialize(0, 8 ** 8)
    def initialize(self, index, value):
        self.data[index] = value
        if value == 1:
            return
        value /= 8
        for i in xrange(8):
            self.initialize(8 * index + i + 1, value)
    def pop(self, r, g, b):
        r = bin(r | 256)[3:]
        g = bin(g | 256)[3:]
        b = bin(b | 256)[3:]
        desired_path = [int(''.join(x), 2) for x in zip(r, g, b)]
        actual_path = []
        index = 0
        for desired_child in desired_path:
            base = 8 * index + 1
            for child in LOOKUP[desired_child]:
                new_index = base + child
                if self.data[new_index]:
                    break
            actual_path.append(new_index - base)
            index = new_index
            self.data[index] -= 1
        bits = [bin(x | 8)[3:] for x in actual_path]
        r, g, b = [int(''.join(x), 2) for x in zip(*bits)]
        return r, g, b
