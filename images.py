from tools import *
 
def makename(*parts,ext=".png"):
    return os.path.join("images","_".join([str(part) for part in parts]+[ext]))

def imageList(imageName):
    l=[pygame.image.load(makename(imageName,n)) for n in range(MAXZOOM)]
    for i in l: i.set_colorkey(TRANSCOL)
    return l
   
def setupImage(cls):
    """a decorator for classes with images, scales images when the class is created"""
    cls.images=imageList(cls.imageName)
    return cls

def perPlayer(imageName):
    return [imageName+"_p_"+str(p) for p in range(MAXPLAYERS)]


def perPlayerDec(cls):
    """a decorator for classes with images that need to be different for each player"""
    cls.images=[imageList(imageName) for imageName in perPlayer(cls.imageName)]
    return cls

def roadDec(cls):
    """a decorator for classes with road images"""
    imagesl=imageList(cls.imageName+"_l")
    imagesr=[pygame.transform.flip(im,True,False) for im in imagesl]
    imagesu=imageList(cls.imageName+"_u")
    cls.images=[[imagesu,imagesr,imagesl] for n in range(MAXPLAYERS)]
    return cls
    
def highlight(sur,x,y,r):
    s=pygame.Surface((2*r,2*r))
    pygame.draw.circle(s,(255,255,255),(r,r),r)
    s.set_colorkey((0,0,0))
    s.set_alpha(128)
    sur.blit(s,(x-r,y-r))
    
    
def highlight2(sur,x,y,r):
    s=pygame.Surface((2*r,2*r))
    s.set_colorkey((0,0,0))
    for n in range(r):
        pygame.draw.circle(s,(255,255,255),(r,r),n)
        s.set_alpha(int(256/r))
        sur.blit(s,(x-r,y-r))

bases=imageList(os.path.join("terrains","basehex"))
baseszs+=[i.get_size() for i in bases]