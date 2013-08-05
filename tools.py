import random
import math
import pygame
from pygame.locals import *

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

def vertcor(n,w,h):
    """returns the coordinates of a vertex relative to the top left of a hexagon"""
    return [(w//2,h),(w,h*3//4)][n]

def tupIndex(arr,tup):
    if len(tup)==0:return arr
    else:return tupIndex(arr[tup[0]],tup[1:])

sign=lambda x:math.copysign(1,x)


