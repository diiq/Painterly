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



def palette_vector_pure(color, palette):
    col = np.matrix(color.rgb).transpose()/255.0
    transmatrix = np.linalg.inv(np.matrix([c.rgb for c in palette]).transpose()/255.0)
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
            lumins = color.luminosity()
            lumin_palette = [Color([min(255, int(color.luminosity()/x.luminosity()*y))
                                    for y in x.rgb], "rgb") for x in PALETTE] 
            l = swatch_list(lumin_palette, 
                            palette_vector(color, PALETTE), 
                            (WIDTH/2)*(HEIGHT/2))
        
  
            for i in range(WIDTH/2):
                for j in range(HEIGHT/2):
                    if  (i*HEIGHT/2)+j < len(l):
                        self.c.create_line(i, HEIGHT/2+j, i, HEIGHT/2+j+1, 
                                           fill=l[(i*HEIGHT/2)+j].web)
            p = self.c.create_rectangle ( WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, 
                                          fill=color.web, width = 0 )

    app = Application()
    app.master.title("Sample application")
    app.mainloop()


if __name__=='__main__':
    test_stroke()
