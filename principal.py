'''

        DISCLAIMER: el siguiente código fue basado en el python raycaster engine
        realizado por Mariano Lambir, extraído de: https://github.com/mlambir/Pygame-FPS.
        Créditos al autor. 
        
'''

import pygame
from pygame.locals import *
import math
import gameController as gc
import time
from playsound import playsound

mapa =[
  [8,8,8,8,8,8,8,8,8,8,8,4,4,6,4,4,6,4,6,4,4,4,6,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
  [8,0,3,3,0,0,0,0,0,8,8,4,0,0,0,0,0,0,0,0,0,0,0,4],
  [8,0,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,6,6,6,0,6,4,6],
  [8,8,8,8,0,8,8,8,8,8,8,4,4,4,4,4,4,6,0,0,0,0,0,6],
  [7,7,7,7,0,7,7,7,7,0,8,0,8,0,8,0,8,4,0,4,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,0,0,0,0,0,6],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,0,0,0,0,4],
  [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,6,0,6,0,6,0,6],
  [7,7,0,0,0,0,0,0,7,8,0,8,0,8,0,8,8,6,4,6,0,6,6,6],
  [7,7,7,7,0,7,7,7,7,8,8,4,0,6,8,4,8,3,3,3,0,3,3,3],
  [2,2,2,2,0,2,2,2,2,4,6,4,0,0,6,0,6,3,0,0,0,0,0,3],
  [2,2,0,0,0,0,0,2,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [2,0,0,0,0,0,0,0,2,4,0,0,0,0,0,0,4,3,0,0,0,0,0,3],
  [1,0,0,0,0,0,0,0,1,4,4,4,4,4,6,0,6,3,3,0,0,0,3,3],
  [2,0,0,0,0,0,0,0,2,2,2,1,2,2,2,6,6,0,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
  [2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,5,0,5,0,5,0,5,0,5],
  [2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,0,5,0,5,0,0,0,5,5],
  [2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,5,5,5,5,5,5,5,5,5]
]

## ubicaciones de los sprites en el mundo 
sprites = [

    (20.5, 11.5, 2), #green light en la habitacion del start del personaje
  #green lights en cada habitacion
    (18.5,4.5, 2),
    (10.0,4.5, 2),
    (10.0,12.5,2),
    (3.5, 6.5, 2),
    (3.5, 20.5,2),
    (3.5, 14.5,2),
    (14.5,20.5,2),

  #mesa en el cuarto de inicio
    (19.5, 9.5, 7),
  #demás mesas
    (15.0, 6.5, 7),

  #pilares (potes de plantas) en el primer cuarto 
    (18.5, 10.5, 1),
    (18.5, 12.5, 1),

  #botes de plantas
    (3.5, 6.5, 2),
    (14.5,12.5,2),
  
  #barriles en el mapa
    (21.5, 1.5, 0),
    (15.5, 1.5, 0),
    (16.0, 1.8, 0),
    (16.2, 1.2, 0),
    (3.5,  2.5, 0),
    (9.5, 15.5, 0),
    (10.5, 15.8,0),

    #animalitos en el mapa
    (18.8, 11.5, 10), 
    (10.0, 15.1,11),
    (15.0, 2.5, 12),
    (10.0,2.5, 13),
    (14.5,21.5,14),
]


# imagen: archivo de la imagen, opaco: valor alpha, color: color que tiene la imagen de fondo (que no se toma en cuenta al renderizar)
def cargar_imagen(imagen, opaco, color = None):
    ret = []
    if color is not None:
        imagen.set_colorkey(color)
    if opaco:
        imagen.set_alpha(127)
    for n in range(imagen.get_width()):
        s = pygame.Surface((1, imagen.get_height())).convert()
        s.blit(imagen, (-n, 0))
        if color is not None:
            s.set_colorkey(color)
        ret.append(s)
    return ret

def keyManagement(wc, moveSpeed, rotSpeed, weapon_numbers, weapons):

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        # move forward if no wall in front of you
        moveX = wc.camara.x + wc.camara.dirx * moveSpeed
        if(mapa[int(moveX)][int(wc.camara.y)]==0 and mapa[int(moveX + 0.1)][int(wc.camara.y)]==0):wc.camara.x += wc.camara.dirx * moveSpeed
        moveY = wc.camara.y + wc.camara.diry * moveSpeed
        if(mapa[int(wc.camara.x)][int(moveY)]==0 and mapa[int(wc.camara.x)][int(moveY + 0.1)]==0):wc.camara.y += wc.camara.diry * moveSpeed
    if keys[K_DOWN]:
        # move backwards if no wall behind you
        if(mapa[int(wc.camara.x - wc.camara.dirx * moveSpeed)][int(wc.camara.y)] == 0):wc.camara.x -= wc.camara.dirx * moveSpeed
        if(mapa[int(wc.camara.x)][int(wc.camara.y - wc.camara.diry * moveSpeed)] == 0):wc.camara.y -= wc.camara.diry * moveSpeed
    if (keys[K_RIGHT] and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
        # rotate to the right
        # both camara direction and camara plane must be rotated
        oldDirX = wc.camara.dirx
        wc.camara.dirx = wc.camara.dirx * math.cos(- rotSpeed) - wc.camara.diry * math.sin(- rotSpeed)
        wc.camara.diry = oldDirX * math.sin(- rotSpeed) + wc.camara.diry * math.cos(- rotSpeed)
        oldPlaneX = wc.camara.planex
        wc.camara.planex = wc.camara.planex * math.cos(- rotSpeed) - wc.camara.planey * math.sin(- rotSpeed)
        wc.camara.planey = oldPlaneX * math.sin(- rotSpeed) + wc.camara.planey * math.cos(- rotSpeed)
    if (keys[K_LEFT] and not keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_DOWN]): 
        # rotate to the left
        # both camara direction and camara plane must be rotated
        oldDirX = wc.camara.dirx
        wc.camara.dirx = wc.camara.dirx * math.cos(rotSpeed) - wc.camara.diry * math.sin(rotSpeed)
        wc.camara.diry = oldDirX * math.sin(rotSpeed) + wc.camara.diry * math.cos(rotSpeed)
        oldPlaneX = wc.camara.planex
        wc.camara.planex = wc.camara.planex * math.cos(rotSpeed) - wc.camara.planey * math.sin(rotSpeed)
        wc.camara.planey = oldPlaneX * math.sin(rotSpeed) + wc.camara.planey * math.cos(rotSpeed)

def main():
    frame0 = time.clock() #tiempo del frame actual 
    oldTime = 0.
    size = w, h = 640, 480 #tamaño de la ventana 

    #configuracion de ventana 
    pygame.init()
    window = pygame.display.set_mode(size)
    pygame.display.set_caption("Spot the pet :)")
    screen = pygame.display.get_surface()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    #font 
    f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    #controlador del mundo (world controller)
    wc = gc.GameController(mapa, sprites, x= 22, y=11.5, dirx=-1, diry=0, planex=0, planey=0.66)
        # armas disponibles


    weapons = [
            Weapon("fist"),
            Weapon("pistol"),
            Weapon("shotgun"),
            Weapon("dbshotgun"),
            Weapon("chaingun"),
            Weapon("plasma"),
            Weapon("rocket"),
            Weapon("bfg"),
            Weapon("chainsaw")
            ]
    weapon_numbers = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_0]
    weapon = weapons[0]
    while(True):
        clock.tick(60) #a cuantos fps
        wc.draw(screen)

        #tiempos para contador fps
        frametime = float(clock.get_time()) / 1000.0
        frame0 = time.clock()
        text = f.render(str(clock.get_fps()), False, (255, 255, 0))
        #screen.blit(text, text.get_rect(), text.get_rect())
        weapon.draw(screen, frame0)
        pygame.display.flip()


        #modificadores de la velocidad del jugador

        moveSpeed = frametime * 5.0 # la dimensional de la constante debe ser de frames/seg
        rotSpeed = frametime * 3.0 # la dimensional de la constante debe ser de radianes/seg

        for event in pygame.event.get(): 
            if event.type == QUIT: 
                return 
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_SPACE:
                    #shoot
                    weapon.play()
                elif event.key in weapon_numbers:
                    weapon.stop()
                    weapon = weapons[weapon_numbers.index(event.key)]
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    weapon.stop()
            else:
                pass 
        keyManagement(wc, moveSpeed, rotSpeed, weapon_numbers, weapons)

fps = 8
class Weapon(object):
    
    def __init__(self, weaponName="shotgun", frameCount = 5):
        self.images = []
        self.loop = False
        self.playing = False
        self.frame = 0
        self.oldTime = 0
        for i in range(frameCount):
            img = pygame.image.load("pics/weapons/%s%s.bmp" % (weaponName, i+1)).convert()
            img = pygame.transform.scale2x(img)
            img = pygame.transform.scale2x(img)
            img.set_colorkey(img.get_at((0,0)))
            self.images.append(img)
    def play(self):
        self.playing = True
        self.loop = True
    def stop(self):
        self.playing = False
        self.loop = False
    def draw(self, surface, time):
        if(self.playing or self.frame > 0):
            if(time > self.oldTime + 1./fps):
                self.frame = (self.frame+1) % len(self.images)
                if self.frame == 0: 
                    if self.loop:
                        self.frame = 1
                    else:
                        self.playing = False
                        
                self.oldTime = time
        img = self.images[self.frame]
        surface.blit(img, (surface.get_width()/2 - img.get_width()/2, surface.get_height()-img.get_height()))



if __name__ == '__main__':
    main()