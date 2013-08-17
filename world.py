from tools import *
import images
import player,human
import buildings ##cross importing warning

BLOCKSIZE=3
VARIATIONS=[0.1,0.1,0.1]##a measure of how much terrain changes between blocks warning exponential
RM=[0.1,0.1,0.1]##reversion to mean, must be float>0
OCHANGE=1.1##>1

class Block():
    """a block of ~100 hexagons"""
    def __init__(self,pos):
        check(pos not in blocks,"this block "+str(pos)+" has already been initialised")
        blocks[pos]=self
        self.pos=x,y=pos
        self.neighbours={}
        for dx,dy in NLIST[:6]:
            if (x+dx,y+dy) in blocks:
                b=blocks[(x+dx,y+dy)]
                b.newNeighbour(-dx,-dy,self)
                self.neighbours[dx,dy]=b
        
        lent=len(Terrains)
        self.ratios=[RM[n]/lent+sum([b.ratios[n] for b in self.neighbours.values()])
                     for n in range(lent)]
        if len(self.neighbours)==0:self.ocean=0
        else:
            no=[b.ocean for b in self.neighbours.values()]
            self.ocean=mean(no)/OCHANGE if len(self.neighbours)!=0 else 0
            if all([x<0.8 for x in no]) or all([x>0.2 for x in no]):self.ocean+=random.choice([-0.5,-0.4,0,0.4,0.5])
        for n in range(lent):
            self.ratios[n]*=random.lognormvariate(0,VARIATIONS[n])
        s=sum(self.ratios)
        for n in range(lent):self.ratios[n]/=s
        
        self.cells=[[self.randT(dx,dy) for dy in range(BLOCKSIZE)]for dx in range(BLOCKSIZE)]
        self.verticies=[[[None,None] for dy in range(BLOCKSIZE)]for dx in range(BLOCKSIZE)]
        self.edges=[[[None,None,None] for dy in range(BLOCKSIZE)]for dx in range(BLOCKSIZE)]
                
    def newNeighbour(self,dx,dy,b):
        check((dx,dy) not in self.neighbours,"there is already a neighbour in this place!")
        self.neighbours[dx,dy]=b

    def randT(self,dx,dy):
        r=random.random()
        x,y=self.pos
        c=0
        if ((r*113)%1)<self.ocean:return Water(x*3+dx,y*3+dy)
        for n,ratio in enumerate(self.ratios):
            c+=ratio
            if r<c:return Terrains[n](x*3+dx,y*3+dy)

    def getHome(self):
        for x in range(BLOCKSIZE-1):
            for y in range(BLOCKSIZE-1):
                for n,ds in enumerate([{(0,0),(0,1),(1,0)},{(1,1),(0,1),(1,0)}]):
                    if {self.cells[x+dx][y+dy].__class__ for dx,dy in ds}==set(Terrains):
                        return [(x,y,n),(x+1,y,n)][n]

def makeTerrain(n,imgFile):
    @images.setupImage
    class Terrain():
        name=n
        imageName=os.path.join("terrains",imgFile)
        def __init__(self,x,y):
            self.pos=x,y
            self.verticies=[None,None]
            self.edges=[None,None,None]
        def draw(self,surface,ox,oy,layer,scale):
            x,y=self.pos
            if layer==0:
                pos=hexpos(x,y,scale)
                surface.blit(self.images[scale],(pos[0]-ox,pos[1]-oy))
            if layer==2:
                for n in range(3):
                    if self.edges[n]:
                        pos=edgepos(x,y,n,scale)
                        self.edges[n].draw(surface,pos[0]-ox,pos[1]-oy,scale)
            if layer==4:
                for n in range(2):
                    if self.verticies[n]:
                        pos=vertexpos(x,y,n,scale)
                        self.verticies[n].draw(surface,pos[0]-ox,pos[1]-oy,scale)
    return Terrain

def init():
    global blocks,wspi
    blocks={}
    wspi=sqaSpiral()
    for pos in wspi:
        p2=Block(pos).getHome()
        if p2:break
    return pos[0]*BLOCKSIZE+p2[0],pos[1]*BLOCKSIZE+p2[1],p2[2]
    
            
def getCell(x,y):
    if (x//BLOCKSIZE,y//BLOCKSIZE) in blocks:
        b=blocks[x//BLOCKSIZE,y//BLOCKSIZE]
    else:
        b=Block((x//BLOCKSIZE,y//BLOCKSIZE))
    return b.cells[x%BLOCKSIZE][y%BLOCKSIZE]


Terrains=[makeTerrain("Mountain","mountain"),
          makeTerrain("Forest","forest"),
          makeTerrain("Fields","field")]

Water=makeTerrain("Water","water")
