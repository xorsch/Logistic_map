# Variant que es poden passar arguments desde terminal
#

import sys, getopt
import threading
import time
import numpy as np
import logging
from PIL import Image


def main(argv):
    # Main program
    # ...
    version = '0.0.2'

    outputfile = "logistic_map"

    min_x = 3.54
    max_x = 3.84
    size_array = 1920
    iterations = 1920*5

    # Imatge
    width  = 1920
    height = 1080

    try:
        opts, args = getopt.getopt(argv,"h:o:s:i:m:n:w:h:", 
            ["ofile=","size_array=","iterations=","max_x=","min_x=","width=","height="] )
            
    except getopt.GetoptError:
        print ('test.py -o <outputfile> -s <size_array> -i <iterations> -w <width> -h <height> --help')
        print (f'version {(version)}')
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-s", "--size_array"):
            size_array = arg
        elif opt in ("-i", "--iterations"):
            iterations = arg  
        elif opt in ("-m", "--max_x"):
            max_x = arg
        elif opt in ("-n", "--min_x"):
            min_x = arg             
        elif opt in ("-w", "--width"):
            width = arg
        elif opt in ("-h", "--height"):
            height = arg     
        elif opt in ("--help"):
            print ('test.py -o <outputfile>')
            sys.exit()     

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    space_array  = np.arange(min_x,max_x,(max_x-min_x)/size_array,dtype='float64')
    random_array = np.random.random(size_array)
    temp_image   = np.zeros([width,height],dtype='float64')
    
    max_gray = 0

    logging.info("Calculating logistic_map.")
    logging.info("It take long time.")


    for _ in range (iterations):
        
        for n in range (size_array):

            random_array[n] = random_array[n] * space_array[n] * (1.0-random_array[n]) 

            x = int( (space_array[n]*width-min_x*width)/(max_x-min_x) )
            y = int( random_array[n]*height )

            if( ( (x>=0) & (x<width)) &
                ( (y>=0) & (y<height)) ):
                temp_image[(x,y)] = temp_image[(x,y)] + 2
                if( max_gray < temp_image[(x,y)]):
                    max_gray = temp_image[(x,y)]


    # # creating a image objec
    
    scale = int( 16581375//max_gray ) 

    logging.info('Processing image.')
    logging.info(f'Max gray {(max_gray)}')
    logging.info(f'Scale factor {(scale)}.') 

    image = Image.new('RGB', (width,height), color=0 )

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


    logging.info("Saving image.")

    ts = time.gmtime()
    image.save(f'{(outputfile)}_{(time.strftime("%y%m%d_%H%M", ts))}.png')    

if __name__ == "__main__":
    main(sys.argv[1:])


# Afegides sortides info
# Afegides opcions des de la línea de comandes
