from tools import *
import buildings
import world##cross importing warning

class Player:
    def __init__(self,block,homepos,colnum):
        self.colnum=colnum
        buildings.Settlement(self,None,block,homepos)

    def seen(self,object):
        pass
