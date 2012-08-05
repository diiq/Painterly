#!/usr/bin/python

# This is a simple color class for use by my digital painter.

# I'm calling these things color spaces, but really they're color
# *representations* -- some of them are spaces, and some aren't.

class Color():
    spaces = {}
    def __init__(self, color, space="web"):
        self.rgb = Color.spaces[space].to_rgb(color)

    def __getattr__(self, name):
        return Color.spaces[name].from_rgb(self.rgb)

class Colorspace():
    def __init__(self, name, from_rgb, to_rgb):
        self.from_rgb = from_rgb
        self.to_rgb = to_rgb
        Color.spaces[name] = self

Colorspace("rgb", lambda x: x, lambda x: x)

# Hex representation

def web_to_rgb(web):
    return [int(web[1:3], 16),
            int(web[3:5], 16),
            int(web[5:], 16)][:]

def rgb_to_web(rgb):
    return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])
    
Colorspace("web", rgb_to_web, web_to_rgb)

# CMY colorspace

def rgb_to_cmy(col):
    return [255-x for x in col]

Colorspace("cmy", rgb_to_cmy, rgb_to_cmy)



def test_Color():    
    c = Color([255, 255, 255], "rgb")
    print c.rgb
#    assert Color("#123456").web == "#123456" #shortcut only while self.enweb happens last!
#    assert Color("#ffffff").cmy == [0, 0, 0] #shortcut only while self.enweb happens last!
    print Color("#00aa00").cmy

if __name__ == '__main__':
    test_Color()