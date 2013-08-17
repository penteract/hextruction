from tools import *
import images
import world##cross importing warning

class Vehicle():
    cost=(0,0,0)##metal,wood,food
    capacity=(0,0,0)
    LOS=1
    image=None
    def __init__(self,player,builder,block,pos):
        rescources=[0,0,0]
        self.player=player
        if self.place=="vertex":
            world.blocks[block].verticies[pos[0]][pos[1]][pos[2]]=self
        elif self.place=="edge":
            world.blocks[block].edges[pos[0]][pos[1]][pos[2]]=self
        else:raise MyError("unknown place type: "+self.place)
        self.n=pos[2]
        if builder:
            for n in range(3):
                builder.resources[n]-=self.cost[n]
                check(builder.resources[n]>0,"does not have enough resources to build this")
        x1=pos[0]+block[0]*world.BLOCKSIZE
        y1=pos[1]+block[1]*world.BLOCKSIZE
        for x,y in hexSpiral(self.LOS):
            world.getCell(x+x1,y+y1).seenby.add(self)
    def draw(self,surface,x,y,scale):
        if self.place=="vertex":
            i=self.images[self.player.colnum][scale]
            surface.blit(i,(x-i.get_width()//2,y-i.get_height()//2))
        elif self.place=="edge":
            i=self.images[self.player.colnum][self.n][scale]
            if self.n==0: surface.blit(i,(x-i.get_width()//2,y))
            else: surface.blit(i,(x,y))

