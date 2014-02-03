from tools import *
import images
import world##cross importing warning

class Building():
    cost=(0,0,0)##metal,wood,food
    capacity=(0,0,0)
    place=None
    LOS=1
    image=None
    def __init__(self,builder,pos):
        rescources=[0,0,0]
        self.player=builder.player
        if self.place=="vertex":
            world.getCell(pos[0],pos[1]).verticies[pos[2]]=self
        elif self.place=="edge":
            world.getCell(pos[0],pos[1]).edges[pos[2]]=self
        else:raise MyError("unknown place type: "+self.place)
        self.pos=pos
        
        if builder:
            for n in range(3):
                builder.resources[n]-=self.cost[n]
                check(builder.resources[n]>=0,"does not have enough resources to build this")
        
        for x,y,cell in self.visible():
            self.player.seen[x,y]=cell
        self.player.buildings.append(self)
            
    def visible(self):
        for dx,dy in hexSpiral(self.LOS):
            x,y=self.pos[0]+dx,self.pos[1]+dy
            yield x,y,world.getCell(x,y)
            
    def cansee(self,s):
        return True
        
    def draw(self,surface,x,y,scale):
        if self.place=="vertex":
            i=self.images[self.player.colnum][scale]
            surface.blit(i,(x-i.get_width()//2,y-i.get_height()//2))
        elif self.place=="edge":
            i=self.images[self.player.colnum][self.pos[2]][scale]
            if self.pos[2]==0: surface.blit(i,(x-i.get_width()//2,y))
            else: surface.blit(i,(x,y))


@images.perPlayerDec
class Settlement(Building):
    cost=(1,5,0)
    capacity=(100,100,100)
    place="vertex"
    LOS=20
    imageName=os.path.join("buildings","settlement")

@images.roadDec
class Road(Building):
    cost=(0,0.1,0)
    place="edge"
    LOS=0
    imageName=os.path.join("roads","road")

