# Modificació
# 

import numpy as np
import time
from PIL import Image

version = '0.0.1'
outputfile = "logistic_map"

width  = 1920
height = 1080

min_x = 3.54
max_x = 3.84
size_array = 1920
iterations = 1920*5


space_array  = np.arange( min_x, max_x, (max_x-min_x)/size_array, dtype='float64' )
random_array = np.random.random( size_array )
temp_image   = np.zeros( [width,height], dtype='float64' )
    
max_gray = 0

for _ in range (iterations):        
    for n in range (size_array):

        random_array[n] = random_array[n] * space_array[n] * ( 1.0 - random_array[n] ) 

        x = int( (space_array[n]*width-min_x*width)/(max_x-min_x) )
        y = int( random_array[n]*height )

        if( ( (x>=0) & (x<width)) &
            ( (y>=0) & (y<height)) ):
            temp_image[(x,y)] = temp_image[(x,y)] + 2
            if( max_gray < temp_image[(x,y)]):
                max_gray = temp_image[(x,y)]

image = Image.new('RGB', (width,height), color=0 )
scale = int( 16581375//max_gray ) 

for ny in range(height):
    for nx in range (width):

        color = int( temp_image[(nx,ny)] * scale )

        if( color<255 ):
            colorRGB = (color,0,0)
        elif( color<65025 ):
            colorRGB = ( 255, int((color-255)/255), 0 )
        elif( color<16581375 ):
            colorRGB = ( 255, 255, int((color-65025)/(65025)) )

        image.putpixel( (nx,ny) , colorRGB )

ts = time.gmtime()
image.save(f'{(outputfile)}_{(time.strftime("%y%m%d_%H%M", ts))}.png')    

# Pujat a GitHub