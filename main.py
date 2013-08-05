from tools import *

import world
import player,AI

FPS=30

def changescale(x,y,s,ds,centre):
    if s+ds>-3 and s+ds<3:
        l=[int(((x,y)[n]+centre[n])*(2**ds)-centre[n]) for n in [0,1]]
        return l[0],l[1],s+ds
    else: return x,y,s

def main():
    size=width,height=512,512
    pygame.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption('Hextruction')
    ##stick any loading screen here
    time=0
    random.seed(52)
    global plyr
    plyr=world.init()
    x,y,scale=0,0,0##logscale
    while True:
        ##event checking
        for event in pygame.event.get():
            if event.type==pygame.QUIT or Key(K_ESCAPE)==event:
                return
            if event.type==MOUSEBUTTONDOWN and event.button in {4,5}:
                    x,y,scale=changescale(x,y,scale,4.5-event.button,event.pos)
            if event.type==MOUSEMOTION and event.buttons[2]:
                x-=event.rel[0]
                y-=event.rel[1]
        ##moving things
        ##coll checking
        ##painting the screen
        world.draw(screen,x,y,2**scale)
        pygame.display.update()
        clock.tick(FPS)
        time+=1

try: main()
finally:pygame.quit()
