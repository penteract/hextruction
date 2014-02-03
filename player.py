from tools import *
import buildings

class Player:
    def __init__(self,homepos,colnum):
        #pygame.mouse.set_cursor(*road)
        self.colnum=colnum
        self.buildings=[]
        self.vehicles=[]
        self.seen={}
        builder=type("",(),{"player":self,"resources":[10000,10000,10000]})
        buildings.Settlement(builder,homepos)
        #for x in range(200):
        #    buildings.Settlement(builder,(0,100*x,0))
        buildings.Road(builder,homepos)
    def go(self):
        pass