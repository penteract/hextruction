import random
import math
import pygame
from pygame.locals import *

#error handling
class Show(Exception):
    def __init__(self,s):
        self.s=s
    def __str__(self):
        return str(self.s)

class MyError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return str(self.msg)
        
def check(cond,msg):
    """raises an error if a condition is not True"""
    if not cond:raise MyError(msg)
