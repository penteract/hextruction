from tools import *
FPS=10

def main():
    global players,l
    screen.blit(pygame.transform.scale(loading,size),(0,0))
    pygame.display.update()
    clock=pygame.time.Clock()
    l=[]
    time=0
    random.seed(52)
    pos=world.init()
    numplayers=0
    players=[human.Human(pos,numplayers,screen)]
    numplayers+=1
    while True:
        for n,plyr in enumerate(players):
            if plyr.go():return n
        x=clock.tick(FPS)
        l.append(x)
        
        time+=1

loading=pygame.image.load("images/loading/loading_i.png")

if __name__=="__main__":
    try:
        size=1024,1024
        pygame.init()
        #screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        screen=pygame.display.set_mode(size)
        size=screen.get_size()
        pygame.display.set_caption('Hextruction')
        ##loading screen
        screen.blit(pygame.transform.scale(loading,size),(0,0))
        pygame.display.update()
        import imagesetup
        import world,human
        main()
    finally:pygame.quit()
