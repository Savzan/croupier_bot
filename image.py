# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


im = Image.open('deck.png')

i = 0
length = im.size[0]
height = im.size[1]
arr = float(0)
while i < 52 :
    
    x = i%13 * np.floor(length/13)
    x2 = (i%13 + 1) * np.floor(length/13)
    y = np.floor(i/13) *  np.floor(height/4)
    y2 = (np.floor(i/13)+1) *  np.floor(height/4)
    
    print(i)
    box = (x,y, x2, y2)
    part = im.crop(box)
    plt.imshow(part)
    plt.show()
    i+=1


