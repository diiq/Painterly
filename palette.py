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

import numpy as np 
import random
from color import *

# New plan! Pick the color on the list closest to aimed-for color.
def distance(cola, colb):    # eudclidean distance
    return pow(sum([x*x for x in (colb-cola).rgb]), .5)

def minimize(things, value_function):
    m = None
    ret = None
    for thing in things:
        val = value_function(thing)
        if not m or m > val:
            m = val
            ret = thing
    return ret

def closest_color(palette, color):
    return minimize(palette, lambda x: distance(x, color))

def n_closest(n, palette, color):
    ret = []
    cur = color
    for i in range(n):
        next = closest_color(palette, cur)
        err = next-cur
        cur_color = color+err

from Tkinter import *
def test_stroke():
    
    HEIGHT = 200 
    WIDTH = 255*3

    PALETTE = [Color("#b80011"),
               Color("#0027a7"),
               Color("#e3ab00")]

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
            self.create_swatch(Color([random.randint(0, 255), 
                                      random.randint(0, 255), 
                                      random.randint(0, 255)], "rgb") )

        def create_swatch(self, color):
            # lumins = color.luminosity()
            # lumin_palette = [Color([min(255, int(color.luminosity()/x.luminosity()*y))
            #                         for y in x.rgb], "rgb") for x in PALETTE] 
            # l = swatch_list(lumin_palette, 
            #                 palette_vector(color, PALETTE), 
            #                 (WIDTH/2)*(HEIGHT/2))
        
  
            # for i in range(WIDTH/2):
            #     for j in range(HEIGHT/2):
            #         if  (i*HEIGHT/2)+j < len(l):
            #             self.c.create_line(i, HEIGHT/2+j, i, HEIGHT/2+j+1, 
            #                                fill=l[(i*HEIGHT/2)+j].web)
            pal = closest_color(PALETTE, color)
            p = self.c.create_rectangle ( 0, HEIGHT/2, WIDTH/2, HEIGHT, 
                                          fill=pal.web, width = 0 )
            p = self.c.create_rectangle ( WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, 
                                          fill=color.web, width = 0 )

    app = Application()
    app.master.title("Sample application")
    app.mainloop()


if __name__=='__main__':
    test_stroke()
