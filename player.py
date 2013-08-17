from tools import *
import buildings

class Player:
    def __init__(self,homepos,colnum):
        #pygame.mouse.set_cursor(*road)
        self.colnum=colnum
        self.buildings=[]
        self.vehicles=[]
        self.seen={}
        builder=type("",(),{"player":self,"resources":[100,100,100]})
        buildings.Settlement(builder,homepos)
        buildings.Road(builder,homepos)
    def go(self):
        pass