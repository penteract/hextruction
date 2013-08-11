import random
import math
import itertools
import pygame
from pygame.locals import *

NLIST=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1)]

#error handling
class Show(Exception):
    def __init__(self,s):
        self.s=s
    def __str__(self):
        return str(self.s)

class MyError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return str(self.msg)
        
def check(cond,msg):
    """raises an error if a condition is not True"""
    if not cond:raise MyError(msg)

#match event to keypress
class Key:
    """a class which can be used to check if an event is a particular keypress"""
    def __init__(self,key):
        self.key=key
        self.type=KEYDOWN
    def __eq__(self,event):
        return event.type==KEYDOWN and event.key==self.key

def sqaSpiral():
    pos=0,0
    direction=1,0
    wait=True
    while True:
        yield pos
        pos=pos[0]+direction[0],pos[1]+direction[1]
        
        if wait:
            direction=-direction[1],direction[0]
            wait=False
        if abs(pos[0])==abs(pos[1]):
            if direction==(1,0): wait=True
            else: direction=-direction[1],direction[0]

def hexSpiral(r=-1):
    pos=0,0
    yield pos
    for n in itertools.count():
        if n==r:break
        pos=pos[0]+1,pos[1]
        for dx,dy in [(-1,1),(-1,0),(0,-1),(1,-1),(1,0),(0,1)]:
            for m in range(n+1):
                yield pos
                pos=pos[0]+dx,pos[1]+dy

def vertcor(n,w,h):
    """returns the coordinates of a vertex relative to the top left of a hexagon"""
    return [(w//2,h),(w,h*3//4)][n]

def tupIndex(arr,tup):
    if len(tup)==0:return arr
    else:return tupIndex(arr[tup[0]],tup[1:])

def mean(l):
    return sum(l)/len(l)

def var(l):
    return mean([x*x for x in l])-mean(l)**2

sign=lambda x:math.copysign(1,x)


