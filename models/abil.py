
#user defined modules
from constants import *
from models.character import Character
from util.utils import *

#Built in python modules
import random
import textwrap
from operator import attrgetter

class Abil:

    def __init__(self):
        self.item_name = "" #I'm calling this 'item_name' as opposed to abil_name or 'name' b.c it shares an array with the char's inv_list in the GAME_STATE_COMBAT_CHOOSE_ATTACK, so just for ease of use.
        pass