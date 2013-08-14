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
    
def scaleims(resetall=False):
    for dir,dirs,files in os.walk("images"):
        for file in files:
            fname,ext=os.path.splitext(file)
            if ext==".png" and not fname[-1]=="_":
                dname=os.path.join(dir,file)
                mtime=os.path.getmtime(dname)
                image=None
                if fname.endswith("_p"):
                    for p in range(MAXPLAYERS):
                        imcol=None
                        for n in range(MAXZOOM):
                            newname=os.path.join(dir,fname+"_"+str(p)+"_"+str(n)+"_.png")
                            if resetall or not os.path.isfile(newname) or os.path.getmtime(newname)<mtime:
                                if not image:image=pygame.image.load(dname)
                                if not imcol:imcol=replace(image,PLAYERCOL,PLAYERCOLS[p])
                                pygame.image.save(scale(imcol,n),newname)
                else:
                    for n in range(MAXZOOM):
                        newname=os.path.join(dir,fname+"_"+str(n)+"_.png")
                        if resetall or not os.path.isfile(newname) or os.path.getmtime(newname)<mtime:
                            if not image:image=pygame.image.load(dname)
                            pygame.image.save(scale(image,n),newname)

scaleims(__name__=="__main__")