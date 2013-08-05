from tools import *
import world

class Building:
    cost=(0,0,0)
    capacity=(0,0,0)
    place=None
    LOS=0
    #metal,wood,food
    def __init__(self,player,builder,block,pos):
        if self.place=="vertex":
            world.blocks[block].verticies[pos[0]][pos[1]][pos[2]]=self
        elif self.place=="edge":
            world.blocks[block].edges[pos[0]][pos[1]][pos[2]]=self
        else:raise MyError("unknown place type: "+self.place)
        if builder:
            for n in range(3):
                builder.resources[n]-=self.cost[n]
        x1=pos[0]+block[0]*world.BLOCKSIZE
        y1=pos[1]+block[1]*world.BLOCKSIZE
        for x in range(-self.LOS,self.LOS+1):
            for y in range(-self.LOS,self.LOS+1):
                if abs(x+y)<=self.LOS:
                    world.getCell(x+x1,y+y1)
                    player.visible.add((x+x1,y+y1))
    def draw(self,x,y,surface):
        surface.blit(self.image,(x,y))
        

class Settlement(Building):
    cost=(1,5,0)
    capacity=(100,100,100)
    rescources=[0,0,0]
    place="vertex"
    LOS=3
    image=pygame.image.load("settlement.bmp")
    def draw(self,x,y,surface):
        surface.blit(self.image,(x,y))

