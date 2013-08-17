import random
import math
import itertools
from operator import *
import pygame
from pygame.locals import *
import os.path

NLIST=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1)]
MAXZOOM=5
TRANSCOL=(123,45,67)##colour used to indicate pixels should go transparent
PLAYERCOL=(0,0,255)##colour used to indicate that the region should change colour by player
MAXPLAYERS=3
LAYERS=5
baseszs=[]#set in images
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
        
def gridList(x1,x2,y1,y2):
    return sum([[(x,y) for x in range(x1,x2)]for y in range(y1,y2)],[])

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

def hexpos(x,y,scale):
    """returns the position of hexagon (x,y) at a given scale"""
    return (x*2+y)*baseszs[scale][0]//2,(y*baseszs[scale][1]*3)//4
def vertexpos(x,y,n,scale):
    """returns the position of a vertex at a given scale"""
    check(n in (0,1),"invalid vertex number")
    return (x*2+y+2-n)*baseszs[scale][0]//2,(y*3+3+n)*baseszs[scale][1]//4
def edgepos(x,y,n,scale):
    """returns the position of a edge at a given scale"""
    check(n in (0,1,2),"invalid edge number")
    if n==0:return vertexpos(x+1,y-1,1,scale)
    if n==2:return vertexpos(x-1,y,0,scale)
    return (x*2+y+1)*baseszs[scale][0]//2,(y*3+3)*baseszs[scale][1]//4

def dist(x,y):
    return math.sqrt(x**2+y**2)

def tupIndex(arr,tup):
    if len(tup)==0:return arr
    else:return tupIndex(arr[tup[0]],tup[1:])

def mean(l):
    return sum(l)/len(l)

def var(l):
    return mean([x*x for x in l])-mean(l)**2

def any(it,func=lambda x:x):
	return __builtins__["any"]((func(x) for x in it))

sign=lambda x:math.copysign(1,x)

def printcur(cur):
	w=cur[0][0]//8
	for y in range(cur[0][1]):
		for x in range(w):
			h=bin(cur[2][y*w+x])[2:].rjust(8,"0")
			a=bin(cur[3][y*w+x])[2:].rjust(8,"0")
			print(*map(lambda a,b:(a=="1")+2*(b=="1"),h,a),end="",sep="")
		print()

def makecur(s,hotspot):
    """3 black, 2 white, 0 transparent, 1 invert"""
    l=[x for x in s.split("\n") if x]
    h=len(l)
    w=len(l[0])
    assert not w%8
    a=[]
    o=[]
    for row in l:
        assert len(row)==w
        for x in range(w//8):
            byte=list(map(int,row[x*8:(x+1)*8]))
            a.append(sum([2**(7-p)*(v>=2) for p,v in enumerate(byte)]))
            o.append(sum([2**(7-p)*(v%2) for p,v in enumerate(byte)]))
    return ((h,w),hotspot,tuple(o),tuple(a))

road=makecur("""
0000000000000000
0000000000000000
0000000000000000
0000000000000111
0000000000111333
0000000111333333
0000111333333333
0111333333333331
1333333333331110
3333333331110000
3333331110000000
3331110000000000
1110000000000000
0000000000000000
0000000000000000
0000000000000000
""",(8,8))
show=[None]