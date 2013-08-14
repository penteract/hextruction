from tools import *
import images
import buildings,player ##cross importing warning

BLOCKSIZE=3
VARIATIONS=[0.1,0.1,0.1]##a measure of how much terrain changes between blocks warning exponential
RM=[0.1,0.1,0.1]##reversion to mean, must be float>0
OCHANGE=1.1##>1
LAYERS=5

drawby=None

def hexpos(x,y,scale):
    """returns the position of hexagon (x,y) at a given scale"""
    return (x*2+y)*baseszs[scale][0]//2,(y*baseszs[scale][1]*3)//4
def vertexpos(x,y,n,scale):
    """returns the position of a vertex at a given scale"""
    return (x*2+y+2-n)*baseszs[scale][0]//2,(y*3+3+n)*baseszs[scale][1]//4

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
        #print(self.ocean)-
        #+random.gauss(0,0.5)
        for n in range(lent):
            self.ratios[n]*=random.lognormvariate(0,VARIATIONS[n])
        s=sum(self.ratios)
        for n in range(lent):self.ratios[n]/=s
        
        self.cells=[[self.randT() for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
        self.verticies=[[[None,None] for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
        self.edges=[[[None,None,None] for col in range(BLOCKSIZE)]for n in range(BLOCKSIZE)]
                
    def newNeighbour(self,dx,dy,b):
        check((dx,dy) not in self.neighbours,"there is already a neighbour in this place!")
        self.neighbours[dx,dy]=b

    def randT(self):
        r=random.random()
        c=0
        if ((r*113)%1)<self.ocean:return Water()
        for n,ratio in enumerate(self.ratios):
            c+=ratio
            if r<c:return Terrains[n]()
        

    def drawLayer(self,surface,dx,dy,layer,scale):
        bsz=baseszs[scale]
        for x in range(BLOCKSIZE):
            for y in range(BLOCKSIZE):
                if any(self.cells[x][y].seenby,lambda x:x.player==drawby):
                    if layer==0:
                        pos=hexpos(x,y,scale)
                        self.cells[x][y].draw(surface,pos[0]+dx,pos[1]+dy,scale)
                    if layer==4:
                        for n in range(2):
                            vs=self.verticies[x][y]
                            pos=vertexpos(x,y,n,scale)
                            if vs[n]:vs[n].draw(surface,pos[0]+dx,pos[1]+dy,scale)

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
        def __init__(self):
            self.seenby=set()
        def draw(self,surface,x,y,scale):
            surface.blit(self.images[scale],(x,y))
    return Terrain

def init(scale):
    global blocks,wspi
    blocks={}
    wspi=sqaSpiral()
    for pos in wspi:
        p2=Block(pos).getHome()
        if p2:break
    #for n in range(2000):Block(next(wspi))
    global drawby
    drawby=player.Player(pos,p2,0)
    return vertexpos(pos[0]*BLOCKSIZE+p2[0],pos[1]*BLOCKSIZE+p2[1],p2[2],scale)+(drawby,)
    
            
def getCell(x,y):
    if (x//BLOCKSIZE,y//BLOCKSIZE) in blocks:
        b=blocks[x//BLOCKSIZE,y//BLOCKSIZE]
    else:
        b=Block((x//BLOCKSIZE,y//BLOCKSIZE))
    return b.cells[x%BLOCKSIZE][y%BLOCKSIZE]

def draw(sur,ox,oy,scale):
    """draws all of the world that is loaded onto a given screen"""
    BLKSZ=BLOCKSIZE
    s1=int(scale)
    s2=2**(scale-s1)
    
    scalesz=(int(sur.get_width()*s2),int(sur.get_height()*s2))
    sox,soy=int(ox*s2),int(oy*s2)
    sur2=pygame.Surface(scalesz)
    blocksOnScreen=[]
    bsz=baseszs[s1]
    for y in range((soy*4//bsz[1]-1)//BLKSZ//3-1,(scalesz[1]+soy)*4//bsz[1]//BLKSZ//3+1):
        for x in range(((sox*2+1)//bsz[0]//BLKSZ-y-3)//2,((scalesz[0]+sox)*2//bsz[0]//BLKSZ-y)//2+1):
            if (x,y) in blocks:
                pos=hexpos(x*BLKSZ,y*BLKSZ,s1)
                blocksOnScreen.append((x,y,pos[0]-sox,pos[1]-soy))
    for layer in range(LAYERS):
        for x,y,dx,dy in blocksOnScreen:
            blocks[x,y].drawLayer(sur2,dx,dy,layer,s1)
    pygame.transform.smoothscale(sur2,sur.get_size(),sur)


#used for checking other images have the right dimensions

img=os.path.join("terrains","basehex")
bases=images.imageList(img)
baseszs=[i.get_size() for i in bases]

"""terrains=[Terrain("Mountain","mountain.bmp"),
          Terrain("Forest","forest.bmp"),
          Terrain("Fields","field.bmp")]

water=Terrain("Water","water.bmp")"""
Terrains=[makeTerrain("Mountain","mountain"),
          makeTerrain("Forest","forest"),
          makeTerrain("Fields","field")]

Water=makeTerrain("Water","water")
