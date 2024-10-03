import pygame
import time
import random
import os
import pygame.mixer

#dimensiones de la pantalla
alto=768
ancho=960

#colores
purpura=(255,0,255)
white=(255,255,255)

#inicializacion de la pantalla
pygame.init()
ventana=pygame.display.set_mode((ancho,alto))
drawing=pygame.Surface((ancho,alto))
pygame.display.set_caption("Save Your Live")

#imagenes
fondo=pygame.image.load(('fondo (1).png'))
nave=pygame.image.load(('nave (1).png'))
alien=pygame.image.load(('alien (1).png'))
bala=pygame.image.load(('bala.png'))
pausa=pygame.image.load(('pausa.png'))

#sonidos
disNave=pygame.mixer.Sound("disnave.mp3")
disAlien=pygame.mixer.Sound("disalien.mp3")
pygame.mixer.music.load("sonidoFondo.ogg")
pygame.mixer.music.play(-1)

tInicio=time.time()
tPausa= None

'''La funcion crearAliens crea una lista de aliens y los posiciona en la pantalla
    en forma de matriz, no recibe parametros y retorna una lista de aliens
    Ejemplo:
    crearAliens() retorna una lista de aliens de la forma:
    [alien1,alien2,alien3,alien4,alien5,alien6,alien7,alien8,alien9,alien10,alien11,alien12,alien13,alien14,alien15]'''
def crearAliens():
    aliens=[]
    for i in range(5):
        for j in range(3):
            alien=pygame.Rect(100+i*150,100+j*70,40,34)
            aliens.append(alien)
    return aliens

'''La funcion moverAliens recibe como parametro una lista de aliens y una velocidad de aliens,
    si el alien llega a los bordes de la pantalla, se cambia la direccion de los aliens y se baja
    20 pixeles, si no llega a los bordes de la pantalla, se mueve normalmente, y retorna la velocidad
    de los aliens para saber en que direccion se estan moviendo
    parametros:
    aliens: lista de aliens
    velAliens: velocidad de los aliens
    Ejemplo:
    moverAliens(aliens,velAliens) retorna la velocidad de los aliens'''

def moverAliens(aliens,velAliens):
    for alien in aliens:
        alien.x+=velAliens
        if alien.x>ancho-40 or alien.x<0:
            velAliens*=-1.1
            for alien in aliens:
                alien.y+=20
            break
    return velAliens

'''La funcion dispararAliens recibe como parametro una lista de aliens y una lista de disparos de aliens,
    si la lista de disparos de aliens esta vacia, se elige un alien al azar y se crea un disparo de alien
    en la posicion del alien, si la lista de disparos de aliens no esta vacia, se elige un alien al azar
    y se crea un disparo de alien en la posicion del alien, y retorna la lista de disparos de aliens
    parametros:
    aliens: lista de aliens
    disparosAliens: lista de disparos de aliens
    Ejemplo:
    dispararAliens(aliens,disparosAliens) retorna una lista de disparos de aliens de la forma:
    [disparoAlien1,disparoAlien2,disparoAlien3,disparoAlien4,disparoAlien5,disparoAlien6,disparoAlien7,disparoAlien8,disparoAlien9,disparoAlien10,disparoAlien11,disparoAlien12,disparoAlien13,disparoAlien14,disparoAlien15]'''

def dispararAliens(aliens,disparosAliens):
    if len(disparosAliens)==0:
        alien=random.choice(aliens)
        disparoAlien=pygame.Rect(alien.x+15,alien.y+20,10,10)
        disparosAliens.append(disparoAlien)
    else:
        alien=random.choice(aliens)
        disparoAlien=pygame.Rect(alien.x+15,alien.y+20,10,10)
        disparosAliens.append(disparoAlien)
    return disparosAliens



def colision(aliens,vidasAliens,vidasJugador,disparos, disparosAliens,nave):
    for disparo in disparos:
        for alien in aliens:
            if disparo.colliderect(alien):
                vidasAliens[aliens.index(alien)]-=1
                if vidasAliens[aliens.index(alien)]==0:
                    vidasAliens.pop(aliens.index(alien))
                    aliens.pop(aliens.index(alien))
                disparos.pop(disparos.index(disparo))
                break
    for alien in aliens:
        if alien.y>alto-40:
            vidasJugador-=1
            vidasAliens.pop(aliens.index(alien))
            aliens.pop(aliens.index(alien))

            break
    for disparoAlien in disparosAliens:
        if disparoAlien.colliderect(nave):
            vidasJugador-=1
            disparosAliens.pop(disparosAliens.index(disparoAlien))
            break
    return vidasJugador

'''La funcion pausa se mantiene en un ciclo while hasta que el usuario haga click en el boton de play
    o en el boton de salir, si el usuario hace click en el boton de play se sale del ciclo y se retorna
    a la funcion main, si el usuario hace click en el boton de salir se sale del ciclo y se termina el juego'''

def pausaJuego():
    pausado=True
    inicioPausa=round(time.time())
    while pausado:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if 370+210>pygame.mouse.get_pos()[0]>370 and 250+90>pygame.mouse.get_pos()[1]>250:
                    pausado=False
                if 370+210>pygame.mouse.get_pos()[0]>370 and 370+90>pygame.mouse.get_pos()[1]>370:
                    return 0, False
        ventana.blit(pausa,(0,0))
        pygame.display.update()
    finPausa=round(time.time())
    return finPausa-inicioPausa, True

def makeTime(tiempo):
    font = pygame.font.SysFont(None, 70)

    if (tiempo/60)<10 and (tiempo%60)<10:
        text= font.render("0"+str(tiempo//60)+":0"+str(tiempo%60), True, white)
    elif (tiempo/60)<10:
        text= font.render("0"+str(tiempo//60)+":"+str(tiempo%60), True, white)
    elif (tiempo%60)<10:
        text= font.render(str(tiempo//60)+":0"+str(tiempo%60),  True, white)
    else:
        text= font.render(str(tiempo//60)+":"+str(tiempo%60),  True, white)
    return text


def dibujarVentana(drawing,naveX,naveY, disparos, disparosVel, aliens,disparosAliens, naver):
    drawing.blit(fondo,(0,0))
    # pygame.draw.rect(drawing,(0,0,255),naver)
    drawing.blit(nave,(naveX,naveY))
    for disparo in disparos:
        #pygame.draw.rect(drawing,(255,0,0),disparo)
        drawing.blit(bala,(disparo.x,disparo.y))

        
        disparo.y-=disparosVel
        if disparo.y<0:
            disparos.remove(disparo)
    
    for alienijena in aliens:
        
       # pygame.draw.rect(drawing,(0,255,0),alienijena)
        drawing.blit(alien,(alienijena.x,alienijena.y))

    for disparoAlien in disparosAliens:
        pygame.draw.rect(drawing,purpura,disparoAlien)
        
        disparoAlien.y+=disparosVel
        if disparoAlien.y>alto:
            disparosAliens.pop(disparosAliens.index(disparoAlien))
    ventana.blit(drawing,(0,0))

    pygame.display.update()

def main():
    run=True
    FPS=60
    clock=pygame.time.Clock()
    naveX=ancho/2
    naveY=alto-70
    nave=pygame.Rect(naveX,naveY,40,48)
    vel=5
    disparos=[]
    disparosVel=5
    vidasJugador=3  

    aliens=crearAliens()
    vidasAliens=[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    velAliens=1
    disparosAliens=[]
    tiempodisparo=time.time()
    tPausa=0
    tInicio=round(time.time())
    tPausa1=0

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            drawing.blit(pausa,(0,0))
            pygame.display.update()
            tPausa1, run=pausaJuego()
            tPausa+=tPausa1
        if keys[pygame.K_a] and naveX>0:
            naveX-=vel
            nave.x-=vel
        if keys[pygame.K_d] and naveX<ancho-64:
            naveX+=vel
            nave.x+=vel
        if keys[pygame.K_SPACE]:
            if  time.time()-tiempodisparo>0.2:            
                    disparos.append(pygame.Rect(naveX+18,naveY-10,14,26))
                    disNave.play()
                    tiempodisparo=time.time()
                    
        dibujarVentana(ventana,naveX,naveY, disparos, disparosVel,aliens,disparosAliens, nave)
        #con un escala entre 1 y 10, con un numero aleatorio se decide si el alien dispara o no
        if random.randint(1,100)==1:
             disparosAliens=dispararAliens(aliens,disparosAliens)
             disAlien.play()

        vidasJugador= colision(aliens,vidasAliens,vidasJugador,disparos, disparosAliens,nave)
        if vidasJugador==0 or aliens==[]:
            tiempofinal=round(time.time())
            tTotal=makeTime(tiempofinal-tInicio-tPausa)
            ventana.fill((0,0,0))
            font=pygame.font.SysFont(None, 100)
            ventana.blit(tTotal,(ancho/2-100,alto/2-50))
            pygame.display.update()
            time.sleep(3)
            run=False
            return tiempofinal-tInicio-tPausa
        velAliens=moverAliens(aliens,velAliens)


