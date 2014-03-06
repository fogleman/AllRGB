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
    def index_func(index):
        x, y = index % SIZE, index / SIZE
        x, y = x - SIZE / 2, y - SIZE / 2
        x, y = x + random.random() * 512 - 256, y + random.random() * 512 - 256
        return x * x + y * y
    indexes = range(SIZE * SIZE)
    random.shuffle(indexes)
    # indexes = sorted(indexes, key=index_func)
    return indexes

def create_image_data(colors):
    result = [None] * (SIZE * SIZE)
    for index, (r, g, b) in enumerate(colors):
        result[index] = chr(r) + chr(g) + chr(b)
    return ''.join(result)

def main(path):
    app = wx.App()
    print 'loading target image'
    target = load_target(path)
    print 'loading indexes'
    indexes = load_indexes()
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
    main(sys.argv[1])
