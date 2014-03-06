from itertools import product
import sys
import wx

def verify(path):
    app = wx.App()
    image = wx.Image(path)
    data = image.GetData()
    data = [ord(x) for x in data]
    if any(x < 0 or x > 255 for x in data):
        raise Exception('Invalid: Values must be 0 <= x < 256.')
    rgb = zip(data[::3], data[1::3], data[2::3])
    if len(rgb) != len(set(rgb)):
        raise Exception('Invalid: There are duplicate colors.')
    print 'Valid!'

if __name__ == '__main__':
    verify(sys.argv[1])
