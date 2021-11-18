import os
import time

import math
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib_scalebar.scalebar import ScaleBar, SI_LENGTH
from IPython.display import Image as Imageshow
import numpy as np
from raytracing import *

def ray_tracing(width, height, rayo, so, n1, R, si, obj, pixels):

    #focular = R1*R2/((R2-R1)*(nl-1))
    
    #siocular = (focular*socular)/(socular-focular)
       
    #Ocular
    D1 = (nl - 1)/R1
    D2 = (nl - 1)/(-R2)

    #Matriz del ocular
    a1 = (1 - (D2*dl)/nl)
    a2 = -D1-D2+(D1*D2*dl/nl)
    a3 = dl/nl
    a4 = (1 - (D1*dl)/nl)
    Matrizocular = np.array([[a1,a2],[a3,a4]])
    
    #Matriz del sistema

    
    EspejoPlano= np.array([[1,0],[0,1]])
    P3 = np.array([[1,0],[2*si/3,1]])
    P2 = np.array([[1,0],[1*si/3,1]])
    P1 = np.array([[1,0],[so,1]])

    for i in range(width):
        for j in range(height):
            
            #Get pixel value
            pos_x = i
            pos_y = j
            pixel = obj.getpixel((pos_x, pos_y))
            
            x = pos_x - width/2
            y = pos_y - height/2
            

            r = math.sqrt( x*x + y*y ) + 1 #Corrección de redondeo
        
            #Vector rayo de entrada (punto en el objeto)
            y_objeto = r*1
            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/so) #Entra en dirección del centro de la lente
            elif rayo == 1: #paralelo
                alpha_entrada = 0 #Entra paralelo al eje del sistema óptico

            c=((-1-1)/R)+(pow(y_objeto,2)*((3.555555556e-9)+(-1.037037037e-9)))
            EspejoCircular = np.array([[1,c],[0,1]])
                
            V_entrada = np.array([alpha_entrada,y_objeto]) 
            
            V_salida = Matrizocular.dot(P3.dot(EspejoPlano.dot(P2.dot(EspejoCircular.dot(P1.dot(V_entrada))))))
                
            #Transversal magnification
            y_imagen = V_salida[1]
            if rayo == 0: #principal
                Mt = (1)*y_imagen/y_objeto #atan correction
            elif rayo == 1: #paralelo
                Mt = y_imagen/y_objeto

            #Conversion from image coordintes to lens coordinates        
            x_prime = Mt*x
            y_prime = Mt*y
            
            pos_x_prime = int(x_prime + width_output/2)
            pos_y_prime = int(y_prime + height_output/2)
            
            if  pos_x_prime < 0 or pos_x_prime >= width_output:
            	continue
            	
            if  pos_y_prime < 0 or pos_y_prime >= height_output:
            	continue
                     
            if rayo == 0: #principal   
                pixels[pos_x_prime, pos_y_prime] = (int(pixel), int(pixel), int(pixel))
            elif rayo == 1: #paralelo    
                new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0])/2
                pix_fin = ( int(new_gray), int(new_gray), int(new_gray) )        
                pixels[pos_x_prime, pos_y_prime] = pix_fin
    

    if rayo==1:
        print("Magnificacion calculada:" , Mt)
    
    return pixels

R1 = 3
R2 = -3
dl=0.1 

so = 1000 
f=300 #cm
R=2*f #cm

#Distancia al plano imagen
si = (f*so)/(so-f)

print("Distancia Imagen espejo primario: ", si)

nl=1.5

focular = R1*R2/((R2-R1)*(nl-1))
    
#Ocular
D1 = (nl - 1)/R1
D2 = (nl - 1)/(-R2)
    
#Matriz del ocular
a1 = (1 - (D2*dl)/nl)
a2 = -D1-D2+(D1*D2*dl/nl)
a3 = dl/nl
a4 = (1 - (D1*dl)/nl)
Matrizocular = np.array([[a1,a2],[a3,a4]])

P3 = np.array([[1,0],[2*si/3,1]])
P2 = np.array([[1,0],[1*si/3,1]])
P1 = np.array([[1,0],[so,1]])
EspejoPlano= np.array([[1,0],[0,1]])
EspejoCircular = np.array([[1,-2/R],[0,1]])

Mt=Matrizocular.dot(P3.dot(EspejoPlano.dot(P2.dot(EspejoCircular.dot(P1.dot([0,1]))))))[1]

Imageshow(filename='snowman.jpg')

obj = Image.open("snowman.jpg")
width, height = obj.size
width_output = int(width*(abs(Mt)))     
height_output = int(height*(abs(Mt)))
# Create new Image and a Pixel Map
image_b = Image.new("RGB", (width_output, height_output),"white")
pixels = image_b.load()
pixels = ray_tracing(width, height, 0, so, nl, R, si, obj, pixels)
pixels = ray_tracing(width, height, 1, so, nl, R, si, obj, pixels)

image_b.save('snowman_output.png', format='PNG')
Imageshow(filename='snowman_output.png')

