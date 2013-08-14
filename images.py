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
    return [imageName+"_"+str(p) for p in range(MAXPLAYERS)]


def perPlayerDec(cls):
    """a decorator for classes with images that need to be different for each player"""
    cls.images=[imageList(imageName) for imageName in perPlayer(cls.imageName)]
    return cls