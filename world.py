from tools import *
import buildings

BLOCKSIZE=7
NLIST=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
VARIATIONS=[0.5,0.1,0.1,0.1]##a measure of how much terrain changes between blocks warning exponential
RM=[0.1,0.1,0.1,0.1]##reversion to mean, must be float>0

class Block():
    """a block of ~100 hexagons"""
    def __init__(self,pos):
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
        
        self.cells=[[]for n in range(BLOCKSIZE)]
        for row in self.cells:
            for col in range(BLOCKSIZE):
                row.append(terrains[self.randT()])
                
    def newNeighbour(self,dx,dy,b):
        check((dx,dy) not in self.neighbours,"there is already a neighbour in this place!")
        self.neighbours[dx,dy]=b

    def randT(self):
        r=random.random()
        c=0
        for n in range(len(self.ratios)):
            c+=self.ratios[n]
            if r<c:return n

    def draw(self,surface,dx,dy):
        for x,row in enumerate(self.cells):
            for y,cell in enumerate(row):
                cell.draw((x*2+y)*basesz[0]/2+dx,y*basesz[1]*3/4+dy,surface)
            
        



class Terrain():#there should be four of these
    def __init__(self,name,file):
        self.name=name
        self.image=pygame.image.load(file)
        self.image.set_colorkey((123,45,67))
        check(self.image.get_size()==basesz,"tile image wrong dimensions")
    def draw(self,x,y,surface):
        surface.blit(self.image,(x,y))

def init():
    global blocks
    blocks={}
    blocks[0,0]=Block((0,0))
    
    for pos in NLIST:
        blocks[pos]=Block(pos)
        

def draw(sur,ox,oy,scale):
    bsz=(BLOCKSIZE*3*basesz[0]//2,basesz[1]*(BLOCKSIZE*3+1)//4)
    scalesz=(int(sur.get_width()//scale),int(sur.get_height()//scale))
    dx,dy=int(ox//scale),int(oy//scale)
    s2=pygame.Surface(scalesz)
    for y in range((dy*4//basesz[1]-1)//BLOCKSIZE//3-1,(scalesz[1]+dy)*4//basesz[1]//BLOCKSIZE//3+1):
        for x in range(((dx*2+1)//basesz[0]//BLOCKSIZE-y-3)//2,((scalesz[0]+dx)*2//basesz[0]//BLOCKSIZE-y)//2+1):
            if (x,y) in blocks:
                blocks[x,y].draw(s2,(x*2+y)*basesz[0]*BLOCKSIZE//2-dx,y*basesz[1]*BLOCKSIZE*3//4-dy)
    pygame.transform.smoothscale(s2,sur.get_size(),sur)


#used for checking other images have the right dimensions
base=pygame.image.load("basehex - copy.png")
basesz=base.get_size()

terrains=[Terrain("Water","water.bmp"),
          Terrain("Mountain","mountain.bmp"),
          Terrain("Forest","forest.bmp"),
          Terrain("Fields","field.bmp")]
    
