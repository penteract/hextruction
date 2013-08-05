from tools import *
import world
import buildings

class Player:
    def __init__(self,block,homepos):
        self.visible=set()
        buildings.Settlement(self,None,block,homepos)

    def seen(self,object):
        pass
