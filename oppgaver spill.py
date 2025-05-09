import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math as m
import random as rd


pg.init()
lever = True
poenger = 0
VINDU_BREDDE = 500
VINDU_HØYDE = 500
vindu = pg.display.set_mode((VINDU_BREDDE, VINDU_HØYDE))
font = pg.font.SysFont("comic sans", 50)

class Ball:
    def __init__(self, x, y, radius, farge, vindusobjekt):
        self.x = x
        self.y = y
        self.radius = radius
        self.farge = farge
        self.vindusobjekt = vindusobjekt

    def tegn(self):
        pg.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius)

    def finnAvstand(self, annenBall):
        xAvstand2 = (self.x - annenBall.x)**2  
        yAvstand2 = (self.y - annenBall.y)**2  
        sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

        radiuser = self.radius + annenBall.radius

        avstand = sentrumsavstand - radiuser

        return avstand
    
class Hinder(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, xFart, yFart):
        super().__init__(x, y, radius, farge, vindusobjekt)
        self.xFart = xFart
        self.yFart = yFart

    def flytt(self):
        global poenger
        self.x += self.xFart
        self.y += self.yFart 

        if self.x - self.radius > self.vindusobjekt.get_width():
            self.x = -self.radius  # kan bruke 0; men blir mer hoppete
            poenger += 1
        elif self.x + self.radius < 0:  
            self.x = self.vindusobjekt.get_width() + self.radius 
            poenger += 1

        
        if self.y - self.radius > self.vindusobjekt.get_height():  
            self.y = -self.radius  
            poenger += 1
        elif self.y + self.radius < 0:  
            self.y = self.vindusobjekt.get_height() + self.radius
            poenger += 1  

            


class Spiller(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart, ):
        super().__init__(x, y, radius, farge, vindusobjekt)
        self.fart = fart

    def flytt(self, taster):
        global lever
        if taster[K_UP]:
            self.y -= self.fart 
        if taster[K_DOWN]:
            self.y += self.fart 
        if taster[K_LEFT]:
            self.x -= self.fart 
        if taster[K_RIGHT]:
            self.x += self.fart 

        if self.x - self.radius >= self.vindusobjekt.get_width():
            self.x = -self.radius
        elif self.x + self.radius <= 0:
            self.x = self.vindusobjekt.get_width() + self.radius

        if self.y - self.radius >= self.vindusobjekt.get_height():
            self.y = -self.radius
        elif self.y + self.radius <= 0:
            self.y = self.vindusobjekt.get_height() + self.radius


def finnAvstand(obj1, obj2):
    xAvstand2 = (obj1.x - obj2.x)**2  # x-avstand i andre
    yAvstand2 = (obj1.y - obj2.y)**2  # y-avstand i andre
    avstand = m.sqrt(xAvstand2 + yAvstand2)
    return avstand

def kolisjon(spiller, hinder):
    global lever
    avstand = finnAvstand(spiller, hinder)  
    if avstand <= (spiller.radius + hinder.radius):
        bilde = font.render("GAME OVER!", True, (250, 250, 250))
        vindu.blit(bilde, (110, 250))
        lever = False

              

spiller = Spiller(200, 200, 20, (255, 69, 0), vindu, 0.1)

hinder = Hinder(150, 250, 20, (0, 0, 255), vindu, 0.08, 0.12)

hinder_liste = []
ANTALL_HINDERE = 3

for ANTALL_HINDERE in range(ANTALL_HINDERE):
    x = rd.randint(20, VINDU_BREDDE - 20)
    y = rd.randint(20, VINDU_HØYDE - 20)
    xFart = rd.uniform(0.05, 0.15) * rd.choice([-1, 1])
    yFart = rd.uniform(0.05, 0.15) * rd.choice([-1, 1])
    hinder_liste.append(Hinder(x, y, 20, (0, 0, 255), vindu, xFart, yFart))

fortsett = True
while fortsett:

    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print (f"Poeng: {poenger}")
            fortsett = False

    if lever:
        trykkede_taster = pg.key.get_pressed()

        
        vindu.fill((135, 206, 235))

        
        spiller.tegn()
        spiller.flytt(trykkede_taster)
        for hinder in hinder_liste:
            hinder.tegn()
            hinder.flytt()
            kolisjon(spiller, hinder)
        

        
        
        
        pg.display.flip()

pg.quit()