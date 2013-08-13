from tools import *
import images
import world##cross importing warning

class Building(images.Drawable):
    cost=(0,0,0)
    capacity=(0,0,0)
    place=None
    LOS=1
    image=None
    #metal,wood,food
    def __init__(self,player,builder,block,pos):
        rescources=[0,0,0]
        self.player=player
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
        for x,y in hexSpiral(self.LOS):
            things=world.getCell(x+x1,y+y1)
            for item in things:
                if item:item.seenby
    def draw(self,surface,x,y,scale):
        i=self.images[self.player.colnum][scale]
        if self.place=="vertex":
            surface.blit(i,(x-i.get_width()//2,y-i.get_height()//2))
        else:
            surface.blit(i,(x,y))


@images.perPlayerDec
class Settlement(Building):
    cost=(1,5,0)
    capacity=(100,100,100)
    place="vertex"
    LOS=100
    imageName="buildings\\settlement_p"

