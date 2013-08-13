from tools import *
FPS=30

def changescale(x,y,s,ds,centre):
    if 0<=s+ds<MAXZOOM:
        l=[int(((x,y)[n]+centre[n])//(2**ds)-centre[n]) for n in [0,1]]
        return l[0],l[1],s+ds
    else: return x,y,s

def main():
    size=width,height=512,512
    pygame.init()
    #screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen=pygame.display.set_mode(size)
    size=width,height=screen.get_size()
    pygame.display.set_caption('Hextruction')
    ##loading screen
    screen.blit(pygame.transform.scale(pygame.image.load("images/loading/loading_.png"),size),(0,0))
    pygame.display.update()
    import imagesetup
    import world
    import player,AI
    clock=pygame.time.Clock()
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
                    x,y,scale=changescale(x,y,scale,event.button-4.5,event.pos)
            if event.type==MOUSEMOTION and event.buttons[2]:
                x-=event.rel[0]
                y-=event.rel[1]
        ##moving things
        ##coll checking
        ##painting the screen
        world.draw(screen,x,y,scale)
        pygame.display.update()
        clock.tick(FPS)
        time+=1

try: main()
finally:pygame.quit()
