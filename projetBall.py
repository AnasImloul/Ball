import pygame
import numpy as np
from random import random,randint
pygame.init()

size=800

screen=pygame.display.set_mode((size,size))
clock = pygame.time.Clock()



class Line:
    def __init__(self,p1,p2):
        self.p1=np.array(p1)
        self.p2=np.array(p2)

    def draw(self):
        pygame.draw.line(screen,(0,0,0),self.p1,self.p2,width=4)


class Points:
    def __init__(self,points=[]):
        self.listOfPoints=points

    def add(self,point):
        self.listOfPoints.append(point)

    def update(self,lines,dt):
        for point in self.listOfPoints:
            point.update(lines,dt)

class Lines:
    def __init__(self,lines=[]):
        self.listOfLines=lines

    def add(self,line):
        self.listOfLines.append(line)

    def draw(self):
        for line in self.listOfLines:
            line.draw()


class Point :
    def __init__(self,pos,speed):
        self.pos=np.array(pos)
        self.speed=np.array(speed)
        self.color=(randint(0,255),randint(0,255),randint(0,255))

    def collide(self,line,dt):
        x1,y1=self.pos
        x2,y2=self.pos+self.speed*dt
        x3,y3=line.p1
        x4,y4=line.p2

        A=np.array(((x2-x1,x3-x4),(y2-y1,y3-y4)))

        if np.linalg.det(A)!=0:
            Y=(x3-x1,y3-y1)
            inv=np.linalg.inv(A)
            t=(inv@Y)[0]
            return t
        return -1






    def reflectionDirection(self,line):
        u=self.speed
        u=u/(np.linalg.norm(u))
        v=line.p2-line.p1
        v=-v
        v=v/np.linalg.norm(v)
        return 2*(u@v)*v-u

    def nextPos(self,lines,dt):
        line=lines.listOfLines[0]
        closest=None
        min_t=float("inf")
        for line in lines.listOfLines:
            t=self.collide(line,dt)
            if t>=0 and t<min_t:
                min_t=t
                closest=line

        if 0<=min_t<=1:

            p=self.pos
            p1=p+min_t*self.speed*dt
            refl=self.reflectionDirection(closest)
            p2=p1+refl*(1-min_t)*self.speed*dt
            self.pos=p2
            self.speed=np.linalg.norm(self.speed)*refl
            #self.speed=0.8*self.speed
        self.pos=self.pos+self.speed*dt

    def draw(self):
        pygame.draw.circle(screen,self.color,self.pos,12)


    def update(self,lines,dt):
        self.speed[1]+=400*dt
        self.nextPos(lines,dt)



        self.draw()




p1=(0,0)
p2=(0,size-100)
p3=(size-100,size-100)
p4=(size-100,0)

line1=Line(p1,p2)
line2=Line(p2,p3)
line3=Line(p3,p4)
line4=Line(p4,p1)

lines=Lines([line1,line2,line3,line4])

points=Points()

for i in range(2+0):
    min=100
    max=size-200

    x,y = randint(min,max-1),randint(min,max-1)
    angle=random()*2*np.pi
    v=100*random()
    points.add(Point((x,y),(np.cos(angle)*v,np.sin(angle)*v)))

FPS=100
dt=0


while True:

    start=pygame.time.get_ticks()

    screen.fill((255, 255, 255))

    lines.draw()
    points.update(lines,dt)

    pygame.display.flip()
    for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running = False
    clock.tick(FPS)
    dt=(pygame.time.get_ticks()-start)/1000