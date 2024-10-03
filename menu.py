'''Este programa es el menú del juego. En él se puede elegir entre jugar o salir del juego.
asi como tambien se puede ver lo mejores puntajes en un tabla de posiciones que es alamcenada en un archivo
de texto'''

import pygame
import time
import juegov2 as juego

#dimensiones de la pantalla
ancho=960
alto=768

#colores 
white=(255,255,255)
black=(0,0,0)

pygame.init()

#inicializacion de la pantalla
pantalla=pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Save Your Live")
drawing=pygame.Surface((ancho,alto))

#importacion de imagenes
pMenu=pygame.image.load("menu.png")
puntajes=pygame.image.load("score.png")
cargar=pygame.image.load("carga.png")

#mostramos la pantalla de menu por 3 segundos
pantalla.blit(cargar,(0,0))
pygame.display.flip()
time.sleep(3)

'''esta funcion  recibe un puntaje y abre un archivo de texto que contiene los mejores puntajes,
si el archivo no existe lo crea y si el archivo ya existe lo lee y lo guarda en una lista, luego
ordena la lista de mayor a menor y si el puntaje recibido es mayor que el ultimo puntaje de la lista
lo agrega a la lista y lo guarda en el archivo de texto, si el puntaje recibido es menor que el ultimo
puntaje de la lista no lo agrega a la lista y no lo guarda en el archivo de texto, luego crea un render 
de la lista y lo retorna'''

def guardarPuntaje(puntaje):
    archivo=open("puntajes.txt","a+")
    archivo.seek(0)
    lista=archivo.readlines()
    if len(lista)==0:
        lista.append(str(puntaje)+"\n")
        archivo.writelines(lista)
    else:
        lista.append(str(puntaje)+"\n")
        lista.sort(reverse=True)
        archivo.seek(0)
        archivo.truncate()
        archivo.writelines(lista)
    archivo.close()
    fuente=pygame.font.Font(None,50)
    listaPuntajes=[]
    for i in lista:
        listaPuntajes.append(fuente.render(i,True,black))
    return listaPuntajes

def score(puntos):
    pantalla.blit(puntajes,(0,0))
    pygame.display.update()
    listaPuntajes=guardarPuntaje(puntos)
    y=200
    for i in listaPuntajes:
        pantalla.blit(i,(400,y))
        y+=60
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                if pos[0]>410 and pos[0]<530 and pos[1]>680 and pos[1]<730:
                    return
        pygame.display.update()


def menu():
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        pantalla.blit(pMenu,(0,0))
        pygame.display.flip()
        #leemos el mouse para saber si se hizo click en alguna de las opciones
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            if pos[0]>410 and pos[0]<530 and pos[1]>530 and pos[1]<580:
                punto=juego.main()
                score(punto)

            if pos[0]>650 and pos[0]<780 and pos[1]>530 and pos[1]<580:
                run=False
            if pos[0]>180 and pos[0]<310 and pos[1]>530 and pos[1]<580:
                score(0)     

        pygame.display.update()

menu()
