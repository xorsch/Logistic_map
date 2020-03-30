##
## Crea una imatge de la funció de bifurcació
## 

import sys, getopt
import threading
import time
import numpy as np
import logging
from PIL import Image


# Crea una imatge buida de width per height
#
def set_temp_image( width, height ):

    logging.info("Creating void image")    
    temp_array = np.zeros( [width,height], dtype='float64' )
    
    return temp_array


# Crea un array de longitud size_array desde min fins max
#
def set_space_array( size_array, min_x, max_x ):

    logging.info("Set space array")
    step = (max_x-min_x)/size_array
    temp_array = np.arange( min_x, max_x, step, dtype='float64' )
    
    return temp_array


# Crea un array de longitud size_array de longitud
#
def set_random_array( size_array ):

    logging.info("Set random array")
    temp_array = np.random.random( size_array ) 
    
    return temp_array


# Calcula el array amb la funció logística 
#
def calculate_logistic_map( random_array, space_array, temp_image, iterations, max_x, min_x ):
    
    width  = temp_image.shape[0]
    height = temp_image.shape[1]

    max_gray = 0

    logging.info("Calculating logistic_map.")
    logging.info("It take long time.")

    for i in range (iterations):
    
        sys.stdout.write(f'\rIteration {(round(i*100/iterations))}%   ' )
        sys.stdout.flush()

        for n in range (random_array.size):
        
            random_array[n] = random_array[n]*space_array[n]*(1.0-random_array[n])
        
            x = int( (space_array[n]*width-min_x*width)/(max_x-min_x) )
            y = int( random_array[n]*height )

            if ( ( (x>=0) & (x<width)) &
                 ( (y>=0) & (y<height)) ):
                temp_image[(x,y)] = temp_image[(x,y)] + 2
                if (max_gray < temp_image[(x,y)]):
                    max_gray = temp_image[(x,y)]
    
    return temp_image

# Calcula quin és el valor més alt de l'array
#
def calculate_max_gray( temp_image ):
    
    width  = temp_image.shape[0]
    height = temp_image.shape[1]

    max_gray = 0

    for ny in range (height):
        for nx in range (width):
             if ( max_gray < temp_image[(nx,ny)]):
                  max_gray = temp_image[(nx,ny)]
    
    return max_gray

# Retorna un color desde un valor de gris
# 
def convert_to_color( color ):
    # Convert gray scale to color
    colorRGB = (0,0,0)

    if( color<255 ):
        colorRGB = (color,0,0)
    elif( color<65025 ):
        colorRGB = ( 255, int((color-255)/255), 0 )
    elif( color<16581375 ):
        colorRGB = ( 255, 255, int((color-65025)/(65025)) )

    return colorRGB


# Desa la imatge en un arxiu
#
def save_image( temp_image, file_name ):
    
    width  = temp_image.shape[0]
    height = temp_image.shape[1]

    image = Image.new('RGB', (width,height), color=0 )

    max_gray = calculate_max_gray( temp_image )
    scale = int(16581375/max_gray)
    colorRGB = np.zeros( (0,0,0) ,dtype='uint16')
        
    logging.info('Processing image.')
    logging.info(f'Max gray {(max_gray)}')
    logging.info(f'Scale factor {(scale)}.') 

    for ny in range(height):
        for nx in range (width):
            color = int( (temp_image[(nx,ny)]) *scale )
            colorRGB = convert_to_color( color )
            image.putpixel( (nx,ny) , colorRGB )

    logging.info("Saving image.")

    ts = time.gmtime()
    image.save(f'{(file_name)}_{(time.strftime("%y%m%d_%H%M", ts))}.png') 


# Funcio principal
#
# crea una matriu de tamany size_array de min a max
# crea una altre matriu d'igual longuitud que la matriu amb números aleatoris
# creem una imatge de alt x ample
# genera la gràfica calculant la funció logistica i pintant-la
# guarda la imatge
def create_logistic_map_image( size_array, iterations, min_x, max_x, width, height, filename ):
    
    space_array  = set_space_array( size_array, min_x, max_x )
    random_array = set_random_array( space_array.size )
    temp_image   = set_temp_image( width, height )

    temp_image   = calculate_logistic_map( random_array, space_array, temp_image, iterations, max_x, min_x )

    save_image( temp_image, filename )


## Script principal comença aquí
# variables per generar les gràfiques

def main(argv):

    version ="0.0.3"
    outputfile = "logistic_map"

    # Imatge
    width  = 1920
    height = 1080
    
    # Logistic_map
    min_x = 3.54
    max_x = 3.80
    size_array = 1920 * 4 
    iterations = 1920 * 50


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


    # TODO: per fer
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    # Funcio principal que vull dividir
    #
    create_logistic_map_image( size_array, iterations, min_x, max_x, width, height, outputfile )
    
    logging.info("Done")


if __name__ == "__main__":

    main(sys.argv[1:])