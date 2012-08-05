#!/usr/bin/python 

# This is an experiment in a kind of dithering, I suppose --- but
# rather than dithering to make up for a too-small palette, I want to
# make blocks of plain color sparkle like a painter's
# brushstrokes. This is part of a larger project intended to mimick
# all the best parts of painting digitally. 

# My goal is to be able to add streaks of color to a solid swatch;
# streaks whose colors are built from a very small palette (6-8
# colors) and their subtractive admixtures. The tricks I've
# encountered so far: it would be nice to be able to find the probler
# mix of palette coors by means of a change of basis, from rgb to
# palette-space. As long as my desire is to have the colors optically
# mix to match the desired swatch, that is impossible: optically mixed
# colors neither add to white nor mix to black; values average. It is
# also not possible to perform a simple change of basis when my
# palette contains more than three colors --- some are linearly
# dependant.

from Tkinter import *
import numpy as np 
import random
from time import sleep

HEIGHT = 200 
WIDTH = 255*3

#A color's gonna be a list of three bits, for now.
class Color():
    spaces = {}
    def __init__(self, color, space="web"):
        self.rgb = Color.spaces[space].to_rgb(color)

    def luminosity(self):
        return pow(sum(map(lambda x: pow(x/(1.732*255), 2), self.rgb)), .5)

    def __getattr__(self, name):
        return Color.spaces[name].from_rgb(self.rgb)

class Colorspace():
    def __init__(self, name, from_rgb, to_rgb):
        self.from_rgb = from_rgb
        self.to_rgb = to_rgb
        Color.spaces[name] = self

Colorspace("rgb", lambda x: x, lambda x: x)

def web_to_rgb(web):
    return [int(web[1:3], 16),
            int(web[3:5], 16),
            int(web[5:], 16)][:]

def rgb_to_web(rgb):
    return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])
    
Colorspace("web", rgb_to_web, web_to_rgb)

def rgb_to_cmy(col):
    return [255-x for x in col]

Colorspace("cmy", rgb_to_cmy, rgb_to_cmy)

def test_Color():    
    c = Color([255, 255, 255], "rgb")
    print c.rgb
#    assert Color("#123456").web == "#123456" #shortcut only while self.enweb happens last!
#    assert Color("#ffffff").cmy == [0, 0, 0] #shortcut only while self.enweb happens last!
    print Color("#00aa00").cmy

def palette_vector_pure(color, palette):
    col = np.matrix(color.rgb + [1.0]*(len(palette)-3)).transpose()/255.0
    transmatrix = np.linalg.inv(np.matrix([c.rgb + [1.0]*(len(palette)-3) for c in palette]).transpose()/255.0)
    newcol = transmatrix*col
    return newcol.T.tolist()[0]

def palette_vector(color, palette):
    pure = palette_vector_pure(color, palette)
    if min(pure) < 0:
        print "OUT:", pure
        pure = map(lambda x: max(x, 0), pure)
    if max(pure) > 1:
        print "OUTSIDE"
    if sum(pure):
        pure = map(lambda x: x*(100/(sum(pure))), pure)
    return map(int, pure)

def test_palette_vector():
#    assert palette_vector(Color("#ffffff"), PALETTE) == [0,0,0]
    print palette_vector(Color("#b80011"), PALETTE)
    print palette_vector(Color("#0027a7"), PALETTE)
    print palette_vector(Color("#e3ab00"), PALETTE)

def swatch_list(palette, vector, l):
    ret = []
    for i in range(len(palette)):
        ret.extend([palette[i]]*(vector[i]*l/100))
    random.shuffle(ret)
    return ret



#PALETTE = [Color("#b80011"),
#           Color("#0027a7"),
#           Color("#e3ab00")]

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        # canvas
        self.c = Canvas (self, height=HEIGHT, width=WIDTH)
        self.c.grid()
        
        # quit button
        self.quitButton = Button ( self, text='Quit',
                                   command=self.quit )
        self.quitButton.grid()

        self.renderButton = Button ( self, text='Render',
                                   command= self.create_swatch_a) 
        self.renderButton.grid()

        self.create_palette(self.c, *PALETTE)

    def create_palette(self, c, *s):
        for i in range(len(s)):
            p = c.create_rectangle ( i*WIDTH/len(s), 0, (i+1)*WIDTH/len(s), HEIGHT/2, 
                                     fill=s[i].web, width = 0 )

    def create_swatch_a(self):
        self.create_swatch(Color(rgb=[random.randint(0, 255), 
                                      random.randint(0, 255), 
                                      random.randint(0, 255)]) )

    def create_swatch(self, color):
        lumins = color.luminosity()
        lumin_palette = [Color(rgb = [min(255, int(color.luminosity()/x.luminosity() * y)) for y in x.rgb]) for x in PALETTE] 
        l = swatch_list(lumin_palette, palette_vector(color, PALETTE), (WIDTH/2)*(HEIGHT/2))
        
  
        for i in range(WIDTH/2):
            for j in range(HEIGHT/2):
                if  (i*HEIGHT/2)+j < len(l):
                    self.c.create_line(i, HEIGHT/2+j, i, HEIGHT/2+j+1, fill=l[(i*HEIGHT/2)+j].web)
        p = self.c.create_rectangle ( WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, 
                                 fill=color.web, width = 0 )


test_Color()
#test_palette_vector()


#app = Application()
#app.master.title("Sample application")
#app.mainloop()
