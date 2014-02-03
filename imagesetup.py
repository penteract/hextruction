from tools import *
import sys,os

PLAYERCOLS=[(0,0,255),(0,255,0),(255,0,0)]

def scale(image,n):
    """scale an image down by 2**n, n must be an integer
    (123,45,67) is assumed to be transparent"""
    if n==0:
        image.set_colorkey(TRANSCOL)
        return image## add .copy() if funky stuff starts to happen with the old image
    sf=2**n
    sz=image.get_size()
    check(not (sz[0]%sf or sz[1]%sf),"dimensions are not multiples of "+str(sf))
    newsz=tuple(x//sf for x in sz)
    image.lock()
    newSurf=pygame.Surface(newsz)
    newSurf.lock()
    for x in range(newsz[0]):
        for y in range(newsz[1]):
            l=sum([[image.get_at((x*sf+dx,y*sf+dy)) for dx in range(sf)] for dy in range(sf)],[])
            l2=[val for val in l if val!=TRANSCOL]
            if len(l2)*2>=len(l): newSurf.set_at((x,y), tuple([int(mean(x)) for x in zip(*l2)]))
            else: newSurf.set_at((x,y),TRANSCOL)
                    
    
    image.unlock()
    newSurf.unlock()
    return newSurf
    
def replace(image,oldcol,newcol):
    newSurf=image.copy()
    newSurf.lock()
    for pos in itertools.product(range(newSurf.get_width()),range(newSurf.get_height())):
        if newSurf.get_at(pos)==oldcol:newSurf.set_at(pos,newcol)
    newSurf.unlock()
    return newSurf
    
def makeScales(name,image,resetall,mtime):
    for n in range(MAXZOOM):
        newname=name+"_"+str(n)+"_.png"
        if resetall or not os.path.isfile(newname) or os.path.getmtime(newname)<mtime:
            pygame.image.save(scale(image(),n),newname)
            
def perPlayer(name,image,resetall):
    return [(name+"_"+str(p),potential(lambda:replace(image(),PLAYERCOL,PLAYERCOLS[p])))for p in range(MAXPLAYERS)]


class potential:
    """a class which does not calculate a value until it is required"""
    def __init__(self,f):
        self.f=f
        self.x=None
    def __call__(self):
        if self.x==None:self.x=self.f()
        return self.x

def scaleims(resetall=False):
    for dir,dirs,files in os.walk("images"):
        for file in files:
            base,ext=os.path.splitext(file)
            if ext==".png" and not base[-1]=="_" and not base.endswith("_i"):
                file=os.path.join(dir,file)
                name=os.path.join(dir,base)
                mtime=os.path.getmtime(file)
                im=potential(lambda:pygame.image.load(file))
                if name.endswith("_p"):
                    l=perPlayer(name,im,resetall)
                else: l=[(name,im)]
                for name,image in l: makeScales(name,image,resetall,mtime)

scaleims(__name__=="__main__")
