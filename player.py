from tools import *
import world
import buildings

class Player:
    def __init__(self,block,homepos):
        buildings.Settlement(self,None,block,homepos)

    def seen(self,object):
        pass
