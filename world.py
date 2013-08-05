from tools import *
import buildings,player

BLOCKSIZE=3
NLIST=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
VARIATIONS=[0.5,0.1,0.1,0.1]##a measure of how much terrain changes between blocks warning exponential
RM=[0.05]*4##reversion to mean, must be float>0


class Block():
    """a block of ~100 hexagons"""
    def __init__(self,pos):
        check(pos not in blocks,"this block "+str(pos)+" has already been initialised")
        blocks[pos]=self
        self.pos=x,y=pos
        self.neighbours={}
        for dx,dy in NLIST:
            if (x+dx,y+dy) in blocks:
                b=blocks[(x+dx,y+dy)]
                b.newNeighbour(-dx,-dy,self)
                self.neighbours[dx,dy]=b
        
        lent=len(terrains)
        self.ratios=[RM[n]/lent+sum([b.ratios[n] for b in self.neighbours.values()])
                     for n in range(lent)]
        for n in range(lent):
            self.ratios[n]*=random.lognormvariate(0,VARIATIONS[n])
        s=sum(self.ratios)
        for n in range(lent):self.ratios[n]/=s
        
        self.cells=[[Cell(terrains[self.randT()]) for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
        self.verticies=[[[None,None] for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
        self.edges=[[[None,None,None] for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
                
    def newNeighbour(self,dx,dy,b):
        check((dx,dy) not in self.neighbours,"there is already a neighbour in this place!")
        self.neighbours[dx,dy]=b

    def randT(self):
        r=random.random()*0.8+0.2
        c=0
        for n,ratio in enumerate(self.ratios):
            c+=ratio
            if r<c:return n
        

    def drawCells(self,surface,dx,dy):
        for x,row in enumerate(self.cells):
            for y,cell in enumerate(row):
                cell.draw(surface,(x*2+y)*basesz[0]/2+dx,y*basesz[1]*3/4+dy)
    def drawEdges(self,surface,dx,dy):
        pass
    def drawVerticies(self,surface,dx,dy):
        for x,row in enumerate(zip(self.cells,self.verticies)):
            for y,(cell,vs) in enumerate(zip(*row)):
                tl=(x*2+y)*basesz[0]/2+dx,y*basesz[1]*3/4+dy
                for n in range(2):
                    if vs[n]:vs[n].draw(surface,(x*2+y+2-n)*basesz[0]/2+dx,(y*3+3+n)*basesz[1]/4+dy)

    def getHome(self):
        for x in range(BLOCKSIZE-1):
            for y in range(BLOCKSIZE-1):
                for n,ds in enumerate([{(0,0),(0,1),(1,0)},{(1,1),(0,1),(1,0)}]):
                    if {self.cells[x+dx][y+dy].terrain for dx,dy in ds}==set(terrains[1:]):
                        return [(x,y,n),(x+1,y,n)][n]

class Drawable:
    def draw(self,surface,x,y):
        abstract
    def drawBy(self,x,y,surface,player):
        if any(ob.player==player for ob in self.seenby):return self.draw(x,y,surface)

class Cell(Drawable):
    def __init__(self,terrain):
        self.terrain=terrain
    def draw(self,surface,x,y):
        self.terrain.draw(x,y,surface)


class Terrain():#there should be four of these
    def __init__(self,name,file):
        self.name=name
        self.image=pygame.image.load(file)
        self.image.set_colorkey((123,45,67))
        check(self.image.get_size()==basesz,"tile image wrong dimensions")
    def draw(self,x,y,surface):
        surface.blit(self.image,(x,y))

def init():
    global blocks,wspi
    blocks={}
    wspi=sqaSpiral()
    for pos in wspi:
        if Block(pos).getHome():break
    for n in range(2000):Block(next(wspi))
    return player.Player(pos,blocks[pos].getHome())
    
            
def getCell(x,y):
    if (x//BLOCKSIZE,y//BLOCKSIZE) in blocks:
        return blocks[x//BLOCKSIZE,y//BLOCKSIZE].cells[x%BLOCKSIZE][y%BLOCKSIZE]
    else:
        return Block((x//BLOCKSIZE,y//BLOCKSIZE)).cells[x%BLOCKSIZE][y%BLOCKSIZE]

def draw(sur,ox,oy,scale):
    """draws all of the world that is loaded onto a given screen"""
    bsz=(BLOCKSIZE*3*basesz[0]//2,basesz[1]*(BLOCKSIZE*3+1)//4)
    scalesz=(int(sur.get_width()//scale),int(sur.get_height()//scale))
    sox,soy=int(ox//scale),int(oy//scale)
    s2=pygame.Surface(scalesz)
    for y in range((soy*4//basesz[1]-1)//BLOCKSIZE//3-1,(scalesz[1]+soy)*4//basesz[1]//BLOCKSIZE//3+1):
        for x in range(((sox*2+1)//basesz[0]//BLOCKSIZE-y-3)//2,((scalesz[0]+sox)*2//basesz[0]//BLOCKSIZE-y)//2+1):
            if (x,y) in blocks:
                blocks[x,y].drawCells(s2,(x*2+y)*basesz[0]*BLOCKSIZE//2-sox,y*basesz[1]*BLOCKSIZE*3//4-soy)
    for y in range((soy*4//basesz[1]-1)//BLOCKSIZE//3-1,(scalesz[1]+soy)*4//basesz[1]//BLOCKSIZE//3+1):
        for x in range(((sox*2+1)//basesz[0]//BLOCKSIZE-y-3)//2,((scalesz[0]+sox)*2//basesz[0]//BLOCKSIZE-y)//2+1):
            if (x,y) in blocks:
                blocks[x,y].drawEdges(s2,(x*2+y)*basesz[0]*BLOCKSIZE//2-sox,y*basesz[1]*BLOCKSIZE*3//4-soy)
    for y in range((soy*4//basesz[1]-1)//BLOCKSIZE//3-1,(scalesz[1]+soy)*4//basesz[1]//BLOCKSIZE//3+1):
        for x in range(((sox*2+1)//basesz[0]//BLOCKSIZE-y-3)//2,((scalesz[0]+sox)*2//basesz[0]//BLOCKSIZE-y)//2+1):
            if (x,y) in blocks:
                blocks[x,y].drawVerticies(s2,(x*2+y)*basesz[0]*BLOCKSIZE//2-sox,y*basesz[1]*BLOCKSIZE*3//4-soy)
    pygame.transform.smoothscale(s2,sur.get_size(),sur)


#used for checking other images have the right dimensions
base=pygame.image.load("basehex.bmp")
basesz=base.get_size()

terrains=[Terrain("Water","water.bmp"),
          Terrain("Mountain","mountain.bmp"),
          Terrain("Forest","forest.bmp"),
          Terrain("Fields","field.bmp")]
    
