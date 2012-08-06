#!/usr/bin/python 

# This is an experiment in a kind of dithering, I suppose --- but
# rather than dithering to make up for a too-small palette, I want to
# make blocks of plain color sparkle like a painter's
# brushstrokes. This is part of a larger project intended to mimick
# all the best parts of painting digitally. 

# Right now I pick colors from the palette proportionally, based on
# the number of times they appear in a super-naive error-propogation
# scheme. This is silly. Also missing: gamma correction.

import numpy as np 
import random
from color import *

def distance(cola, colb):    # eudclidean distance
    return pow(sum([x*x for x in (colb-cola).rgb]), .5)

def minimize(things, value_function): # something python needs (?)
    m = ret = None
    for thing in things:
        val = value_function(thing)
        if not m or m > val:
            m = val
            ret = thing
    return ret

def closest_color(palette, color):
    return minimize(palette, lambda x: distance(x, color))



def n_closest(n, palette, color):
    ret = {}
    for c in palette: ret[c] = 0
    cur = color
    for i in range(n): # 1D error diffusion
        next = closest_color(palette, cur)
        cur = color+cur-next
        ret[next] += 1
    return ret

from Tkinter import *
def test_stroke():
    
    HEIGHT = 400 
    WIDTH = 600

    PALETTE = [Color("#b80011"),
               Color("#0027a7"),
               Color("#e3ab00"),
               Color("#00ab11"),
               Color("#ffffee")]

    class Application(Frame):
        def create_palette(self, c, *s):
            for i in range(len(s)):
                p = c.create_rectangle(i*WIDTH/len(s), 
                                       0, 
                                       (i+1)*WIDTH/len(s), 
                                       HEIGHT/2, 
                                       fill=s[i].web, 
                                       width = 0)

        def create_swatch_a(self):
            self.create_swatch(Color([random.randint(0, 255), 
                                      random.randint(0, 255), 
                                      random.randint(0, 255)], "rgb"))

        def create_swatch(self, color):
            p = self.c.create_rectangle(0, 
                                        HEIGHT/2, 
                                        WIDTH/2, 
                                        HEIGHT, 
                                        fill=color.web, 
                                        width = 0)

            streak_counts = n_closest(self.streaking.get(), PALETTE, color)
            # Draw val lines of key color, randomly:
            mixing = self.mixing.get()
            for streak in PALETTE:
                count = 0
                while count < streak_counts[streak]:
                    col = (streak*(1-mixing) + color*(mixing)) #weighted avg
                    loc = random.randint(0, WIDTH/2)
                    width = random.randint(0, streak_counts[streak]-count)
                    count += width
                    self.c.create_line(loc, 
                                       HEIGHT/2,
                                       loc,
                                       HEIGHT,
                                       width = width,
                                       fill=col.web)


            p = self.c.create_rectangle(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, 
                                        fill=color.web, width = 0)

        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.grid()
            
            # canvas for swatches
            self.c = Canvas (self, height=HEIGHT, width=WIDTH)
            self.c.grid(column = 0, columnspan=2, row=0)
            self.create_palette(self.c, *PALETTE)
        
            # render 
            self.renderButton = Button ( self, text='Render',
                                         command= self.create_swatch_a) 
            self.renderButton.grid(column=1, row=1, rowspan=2, ipadx=20)

            # Mixing scale
            self.mixing = DoubleVar()
            self.mix_scale = Scale(self, 
                                   from_=0.0, 
                                   to=1.0, 
                                   label="Mixing: How mixed in are the streaks?",
                                   variable=self.mixing, 
                                   resolution=-1, 
                                   orient = HORIZONTAL,
                                   length=WIDTH-200)
            self.mix_scale.grid(column=0, row=2, ipady=10)

            # Streaking scale
            self.streaking = IntVar()
            self.streak_scale = Scale(self,
                                      from_=0, 
                                      to=WIDTH/2, 
                                      label="Streaking: how much remains unmixed?", 
                                      variable=self.streaking, 
                                      resolution=1, 
                                      orient = HORIZONTAL, 
                                      length=WIDTH-200)
            self.streak_scale.grid(column=0, row=1, ipady=10)

            


    app = Application()
    app.master.title("Streaky Paint")
    app.mainloop()


if __name__=='__main__':
    test_stroke()
