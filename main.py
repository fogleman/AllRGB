from math import hypot
import random
import sys
import wx

try:
    import octree_c as octree
    print 'using C octree'
except Exception:
    import octree
    print 'using Python octree'

SIZE = 4096

def load_target(path):
    target = wx.Image(path)
    data = target.GetData()
    data = [ord(x) for x in data]
    r, g, b = data[::3], data[1::3], data[2::3]
    return zip(r, g, b)

def load_indexes():
    points = [
        (SIZE / 2, SIZE / 2),
        # (2915, 1340),
        # (1115, 1760),
    ]
    def index_func(index):
        x, y = index % SIZE, index / SIZE
        offset = (random.random() - 0.5) * 512
        return min(hypot(x - a, y - b) for a, b in points) + offset
    indexes = range(SIZE * SIZE)
    random.shuffle(indexes)
    # indexes = sorted(indexes, key=index_func)
    return indexes

def load_indexes_mask(path):
    result = []
    mask = load_target(path)
    colors = sorted(set(mask))
    groups = dict((x, []) for x in colors)
    for index, color in enumerate(mask):
        groups[color].append(index)
    for color in colors:
        group = groups[color]
        random.shuffle(group)
        result.extend(group)
    return result

def create_image_data(colors):
    result = [None] * (SIZE * SIZE)
    for index, (r, g, b) in enumerate(colors):
        result[index] = chr(r) + chr(g) + chr(b)
    return ''.join(result)

def rgb_int(colors):
    return [(r << 16) | (g << 8) | (b) for r, g, b in colors]

def int_rgb(colors):
    result = []
    for color in colors:
        r = 0xff & (color >> 16)
        g = 0xff & (color >> 8)
        b = 0xff & (color >> 0)
        result.append((r, g, b))
    return result

def main(path):
    app = wx.App()
    print 'loading target image'
    target = load_target(path)
    print 'loading indexes'
    indexes = load_indexes()
    # indexes = load_indexes_mask('mask.png')
    print 'initializing octree'
    tree = octree.Octree()
    print 'picking colors'
    colors = [(0, 0, 0)] * (SIZE * SIZE)
    for i, index in enumerate(indexes):
        if i % 65536 == 0:
            pct = 100.0 * i / (SIZE * SIZE)
            print '%.1f%% percent complete' % pct
        colors[index] = tree.pop(*target[index])
    print 'creating output image'
    data = create_image_data(colors)
    image = wx.EmptyImage(SIZE, SIZE)
    image.SetData(data)
    image.SaveFile('output.png', wx.BITMAP_TYPE_PNG)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python main.py input.png'
    else:
        main(sys.argv[1])
