'''

        DISCLAIMER: el siguiente código fue basado en el python raycaster engine
        realizado por Mariano Lambir, extraído de: https://github.com/mlambir/Pygame-FPS.
        Créditos al autor. 
        
'''

import pygame
from pygame.locals import *
import math

#para el texto que se desea poner el pantalla
texWidth = 64
texHeight = 64


class Camara(object):
    def __init__(self,x,y,dirx,diry,planex,planey):
        self.x = float(x)
        self.y = float(y)
        self.dirx = float(dirx)
        self.diry = float(diry)
        self.planex = float(planex)
        self.planey = float(planey)

class GameController(object):
    def __init__(self, mapa, sprites, **kwargs):
        x = kwargs["x"]
        y = kwargs["y"]
        dirx = kwargs["dirx"]
        diry = kwargs["diry"]
        planex = kwargs["planex"]
        planey = kwargs["planey"]
        self.stext = [  
            cargar_imagen(pygame.image.load("pics/items/barrel2.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/fern.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/greenlight.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/pillar.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/barrel.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/pillar2.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/greenlight.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/table.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/fern.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/items/stone_pillar.png").convert(), False, color = (0,0,0)),
            #10: texturas de animalitos
            cargar_imagen(pygame.image.load("pics/pets/doggo.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/pets/sdoggo.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/pets/bigdoggo.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/pets/grumpycat.png").convert(), False, color = (0,0,0)),
            cargar_imagen(pygame.image.load("pics/pets/pusheen.png").convert(), False, color = (0,0,0)),
        ]
        self.background = None
        self.texturas = [
            cargar_imagen(pygame.image.load("pics/walls/bricks.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/bricks.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/purplestone.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/greystone.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/realbrick.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/mossy.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/wood.png").convert(), False),
            cargar_imagen(pygame.image.load("pics/walls/colorstone.png").convert(), False),

            cargar_imagen(pygame.image.load("pics/walls/bricks.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/bricks.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/purplestone.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/greystone.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/realbrick.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/mossy.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/wood.png").convert(), True),
            cargar_imagen(pygame.image.load("pics/walls/colorstone.png").convert(), True),  
        ]
        self.camara = Camara(x,y,dirx,diry,planex,planey)
        self.mapa = mapa
        self.sprites = sprites

    def draw(self, surface):
        w = surface.get_width()
        h = surface.get_height()
        #draw background
        if self.background is None:
            self.background = pygame.transform.scale(pygame.image.load("pics/background.png").convert(), (w,h))
        surface.blit(self.background, (0,0))
        zBuffer = []
        for x in range(w):
            #calculate ray position and direction 
            camaraX = float(2 * x / float(w) - 1) #x-coordinate in camara space
            rayPosX = self.camara.x
            rayPosY = self.camara.y
            rayDirX = self.camara.dirx + self.camara.planex * camaraX
            rayDirY = self.camara.diry + self.camara.planey * camaraX
            #which box of the map we're in  
            mapX = int(rayPosX)
            mapY = int(rayPosY)
       
            #length of ray from current position to next x or y-side
            sideDistX = 0.
            sideDistY = 0.
       
            #length of ray from one x or y-side to next x or y-side
            deltaDistX = math.sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
            if rayDirY == 0: rayDirY = 0.00001
            deltaDistY = math.sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
            perpWallDist = 0.
       
            #what direction to step in x or y-direction (either +1 or -1)
            stepX = 0
            stepY = 0

            hit = 0 #was there a wall hit?
            side = 0 # was a NS or a EW wall hit?
            
            # calculate step and initial sideDist
            if rayDirX < 0:
                stepX = - 1
                sideDistX = (rayPosX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
                
            if rayDirY < 0:
                stepY = - 1
                sideDistY = (rayPosY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY
                
            # perform DDA
            while hit == 0:
                # jump to next map square, OR in x - direction, OR in y - direction
                if sideDistX < sideDistY:
        
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1

                # Check if ray has hit a wall
                if (self.mapa[mapX][mapY] > 0): 
                    hit = 1
            # Calculate distance projected on camara direction (oblique distance will give fisheye effect !)
            if (side == 0):
                #perpWallDist = fabs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX)
                perpWallDist = (abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX))
            else:
                perpWallDist = (abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY))
      
            # Calculate height of line to draw on surface
            if perpWallDist == 0:perpWallDist = 0.000001
            lineHeight = abs(int(h / perpWallDist))
       
            # calculate lowest and highest pixel to fill in current stripe
            drawStart = - lineHeight / 2 + h / 2
            drawEnd = lineHeight / 2 + h / 2
        
            #texturing calculations
            texNum = self.mapa[mapX][mapY] - 1; #1 subtracted from it so that texture 0 can be used!
           
            #calculate value of wallX
            wallX = 0 #where exactly the wall was hit
            if (side == 1):
                wallX = rayPosX + ((mapY - rayPosY + (1 - stepY) / 2) / rayDirY) * rayDirX
            else:
                wallX = rayPosY + ((mapX - rayPosX + (1 - stepX) / 2) / rayDirX) * rayDirY;
            wallX -= math.floor((wallX));
           
            #x coordinate on the texture
            texX = int(wallX * float(texWidth))
            if(side == 0 and rayDirX > 0): 
                texX = texWidth - texX - 1;
            if(side == 1 and rayDirY < 0): 
                texX = texWidth - texX - 1;

            if(side == 1):
                texNum +=8
            if lineHeight > 10000:
                lineHeight=10000
                drawStart = -10000 /2 + h/2
            if texNum == 9:
                surface.blit(pygame.transform.scale(self.texturas[texNum][texX], (1, lineHeight)), (x, drawStart))
            else:
                surface.blit(pygame.transform.scale(self.texturas[texNum][texX], (1, lineHeight)), (x, drawStart))
            zBuffer.append(perpWallDist)

        #function to sort sprites
        def sprite_compare(s1, s2):
            import math
            s1Dist = math.sqrt((s1[0] -self.camara.x) ** 2 + (s1[1] -self.camara.y) ** 2)
            s2Dist = math.sqrt((s2[0] -self.camara.x) ** 2 + (s2[1] -self.camara.y) ** 2)  
            if s1Dist>s2Dist:
                return -1
            elif s1Dist==s2Dist:
                return 0
            else:
                return 1
        #draw sprites
        
        #self.sprites.sort(sprite_compare)
        self.sprites.sort()
        for sprite in self.sprites:
            #translate sprite position to relative to camara
            spriteX = sprite[0] - self.camara.x;
            spriteY = sprite[1] - self.camara.y;
             
            #transform sprite with the inverse camara matrix
            # [ self.camara.planex   self.camara.dirx ] -1                                       [ self.camara.diry      -self.camara.dirx ]
            # [               ]       =  1/(self.camara.planex*self.camara.diry-self.camara.dirx*self.camara.planey) *   [                 ]
            # [ self.camara.planey   self.camara.diry ]                                          [ -self.camara.planey  self.camara.planex ]
          
            invDet = 1.0 / (self.camara.planex * self.camara.diry - self.camara.dirx * self.camara.planey) #required for correct matrix multiplication
          
            transformX = invDet * (self.camara.diry * spriteX - self.camara.dirx * spriteY)
            transformY = invDet * (-self.camara.planey * spriteX + self.camara.planex * spriteY) #this is actually the depth inside the surface, that what Z is in 3D       
                
            spritesurfaceX = int((w / 2) * (1 + transformX / transformY))
          
            #calculate height of the sprite on surface
            spriteHeight = abs(int(h / (transformY))) #using "transformY" instead of the real distance prevents fisheye
            #calculate lowest and highest pixel to fill in current stripe
            drawStartY = -spriteHeight / 2 + h / 2
          
            #calculate width of the sprite
            spriteWidth = abs( int (h / (transformY)))
            drawStartX = int(-spriteWidth / 2 + spritesurfaceX)
            drawEndX = int(spriteWidth / 2 + spritesurfaceX)
            
            if spriteHeight < 1000:
                for stripe in range(drawStartX, drawEndX):
                    texX = int((256 * (stripe - (-spriteWidth / 2 + spritesurfaceX)) * texWidth / spriteWidth) / 256)
                    #the conditions in the if are:
                    ##1) it's in front of camara plane so you don't see things behind you
                    ##2) it's on the surface (left)
                    ##3) it's on the surface (right)
                    ##4) ZBuffer, with perpendicular distance
                    if(transformY > 0 and stripe > 0 and stripe < w and transformY < zBuffer[stripe]):
                        surface.blit(pygame.transform.scale(self.stext[sprite[2]][texX], (1, spriteHeight)), (stripe, drawStartY))

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