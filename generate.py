from itertools import izip, product
import random
import wx

BITS = 6
SIZE = int(((2 ** BITS) ** 3) ** 0.5)
STEP = 2 ** (8 - BITS)

def color_func(color):
    r, g, b = color
    r, g, b = 0.30 * r, 0.59 * g, 0.11 * b
    return r + g + b

# def index_func(index):
#     x = index % SIZE
#     y = index / SIZE
#     bx = bin(x | SIZE)[3:]
#     by = bin(y | SIZE)[3:]
#     bz = ''.join(b + a for a, b in izip(bx, by))
#     z = int(bz, 2)
#     return z

def index_func(index):
    x, y = index % SIZE, index / SIZE
    x, y = x - SIZE / 2, y - SIZE / 2
    return x * x + y * y

def create_data(indexes, colors):
    result = [None] * (SIZE * SIZE)
    for index, color in izip(indexes, colors):
        r, g, b = color
        result[index] = chr(r) + chr(g) + chr(b)
    return ''.join(result)

def main():
    indexes = sorted(xrange(SIZE * SIZE), key=index_func)
    colors = sorted(product(range(0, 256, STEP), repeat=3), key=color_func)
    data = create_data(indexes, colors)
    app = wx.App()
    image = wx.EmptyImage(SIZE, SIZE)
    image.SetData(data)
    image.SaveFile('output.png', wx.BITMAP_TYPE_PNG)

if __name__ == '__main__':
    main()
