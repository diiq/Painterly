#!/usr/bin/python

# This is a simple color class for use by my digital painter.

# I'm calling these things color spaces, but really they're color
# *representations* -- some of them are spaces, and some aren't.
#
# NOTE THAT ALL COLOR-ARITHMETIC WILL BE IN RGB!1111!!

class Color(object):
    spaces = {}
    def __init__(self, color, space="web"):
        # All colors are stored as RGB.
        self.rgb = Color.spaces[space].to_rgb(color)

    def __sub__(self, color):
        diff = [x[0]-x[1] for x in zip(self.rgb, color.rgb)]
        return Color(diff, "rgb")

    def __add__(self, color):
        diff = [sum(x) for x in zip(self.rgb, color.rgb)]
        return Color(diff, "rgb")

    def __mul__(self, num):
        diff = [int(x*num) for x in self.rgb]
        return Color(diff, "rgb")

    def __div__(self, num):
        diff = [int(x/num) for x in self.rgb]
        return Color(diff, "rgb")

    def __getattr__(self, name):
        return Color.spaces[name].from_rgb(self.rgb)

# A colorspace/representation is stored just as way of converting to and from
# RGB.
class Colorspace():
    def __init__(self, name, from_rgb, to_rgb):
        self.from_rgb = from_rgb
        self.to_rgb = to_rgb
        Color.spaces[name] = self

# RGB colorspace is default

Colorspace("rgb", lambda x: x, lambda x: x)

# Hex representation: #ffc035

def web_to_rgb(web):
    return [int(web[1:3], 16), int(web[3:5], 16), int(web[5:], 16)][:]

def rgb_to_web(rgb):
    return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])
    
Colorspace("web", rgb_to_web, web_to_rgb)

# CMY colorspace --- It's useful 'cause it's subtractive.

def rgb_to_cmy(col):
    return [255-x for x in col]

Colorspace("cmy", rgb_to_cmy, rgb_to_cmy)



def test_Color():    
    c = Color([255, 255, 255], "rgb")
    assert c.rgb == [255, 255, 255]
    assert c.cmy == [0, 0, 0]
    assert c.web == "#ffffff"
    assert Color("#123456").web == "#123456"
    print (c-Color("#203948")).rgb

if __name__ == '__main__':
    test_Color()
