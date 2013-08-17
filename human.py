from tools import *
import player,images

def changescale(x,y,s,ds,centre):
    if 0<=s+ds<MAXZOOM:
        l=[int(((x,y)[n]+centre[n])//(2**ds)-centre[n]) for n in [0,1]]
        return l[0],l[1],s+ds
    else: return x,y,s
    
def mousevertex(x,y,bsz):
    x-=bsz[0]//4
    y-=bsz[1]//2
    y=math.floor(y/(bsz[1]*3/4))
    x=math.floor(x/(bsz[0]/2))-y
    return x//2,y,1-x%2

class Human(player.Player):
    def __init__(self,homepos,colnum,screen):
        self.scale=2##logscale
        spos=vertexpos(*homepos,scale=self.scale)
        self.screenpos=spos[0]-screen.get_width()//2,spos[1]-screen.get_height()//2
        self.screen=screen
        super().__init__(homepos,colnum)
    def go(self):
        ox,oy=self.screenpos
        scale=self.scale
        sur=self.screen
        for event in pygame.event.get():
            if event.type==pygame.QUIT or Key(K_ESCAPE)==event:
                return True
            elif event.type==MOUSEBUTTONDOWN and event.button in {4,5}:
                ox,oy,scale=changescale(ox,oy,scale,event.button-4.5,event.pos)
            elif event.type==MOUSEBUTTONDOWN and event.button==1:
                pass
            elif event.type==MOUSEMOTION and event.buttons[2]:
                ox-=event.rel[0]
                oy-=event.rel[1]
        self.screenpos=ox,oy
        self.scale=scale
        
        s1=int(scale)
        s2=2**(scale-s1)
        
        mx,my=pygame.mouse.get_pos()
        mx+=ox;my+=oy
        mx*=s2
        my*=s2
        mouseVertex=mousevertex(mx,my,baseszs[s1])
        
        scalesz=(int(sur.get_width()*s2),int(sur.get_height()*s2))
        sox,soy=int(ox*s2),int(oy*s2)
        sur2=pygame.Surface(scalesz)
        cellsOnScreen=set()
        visible=set()
        
        bsz=baseszs[s1]
        
        #draw background cells
        for y in range((soy*4//bsz[1]-1)//3-1,(scalesz[1]+soy)*4//bsz[1]//3+1):
            for x in range(((sox*2+1)//bsz[0]-y-3)//2,((scalesz[0]+sox)*2//bsz[0]-y)//2+1):
                if (x,y) in self.seen:
                    self.seen[x,y].draw(sur2,sox,soy,0,s1)
                    cellsOnScreen.add((x,y))
        show[0]=[]
        for ob in self.vehicles+self.buildings:
            if ob.cansee(None):
                for x,y,cell in ob.visible():
                    if (x,y) in cellsOnScreen:
                        show[0].append((x,y))
                        visible.add(cell)
        for layer in range(LAYERS):
            for cell in visible:
                cell.draw(sur2,sox,soy,layer,s1)
        mvx,mvy=vertexpos(*mouseVertex,scale=s1)
        if dist(mvx-mx,mvy-my)<2**(6-s1):
            mvx-=sox;mvy-=soy
            images.highlight2(sur2,mvx,mvy,2**(6-s1))
        pygame.transform.smoothscale(sur2,sur.get_size(),sur)
        pygame.display.update()
        
        super().go()
