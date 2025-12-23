
"""

from models.item import Item
from models.room import Room
"""

#User defined modules
from models.character import Character
from constants import *

#Built in python modules
import random
import textwrap
from operator import attrgetter

from models.item import Item


#region Define help funcs and essential funcs

def check_for_equipped_weapon(char_id):
    if isinstance(char_id.inv_list,list):
        for i in range(0,len(char_id.inv_list)):
            if isinstance(char_id.inv_list[i],Item):
                if char_id.inv_list[i].is_shield_boolean == False:
                    #This char has at least 1 non-shield item, equipped return true
                    return True

    return False

def print_combat_ranks(combat_rank_list):
    for i in range(0, len(combat_rank_list)):
        rank_str = ""
        if i == ENUM_RANK_ENEMY_FAR:
            rank_str = f"Distant enemy position: {i}.) "
        elif i == ENUM_RANK_ENEMY_MIDDLE:
            rank_str = f"Middle enemy position: {i}.) "
        elif i == ENUM_RANK_ENEMY_NEAR:
            rank_str = f"Near enemy position: {i}.) "
        elif i == ENUM_RANK_PC_NEAR:
            rank_str = f"Near friendly position: {i}.) "
        elif i == ENUM_RANK_PC_MIDDLE:
            rank_str = f"Middle friendly position: {i}.) "
        elif i == ENUM_RANK_PC_FAR:
            rank_str = f"Distant friendly position: {i}.) "

        characters_at_rank = combat_rank_list[i]

        if len(characters_at_rank) > 0:
            # Count how many of each character name
            name_counts = {}
            for char in characters_at_rank:
                if char.name in name_counts:
                    name_counts[char.name] += 1
                else:
                    name_counts[char.name] = 1

            # Build the string: "Name (count); Name (count)"
            groups = [f"{name} ({count})" if count > 1 else name for name, count in name_counts.items()]
            rank_str += "; ".join(groups)

        rank_str = wrap_str(rank_str, TOTAL_LINE_W, False)

        print(rank_str)

def fill_combat_initiative_list(room_inst_id):
    combat_initiative_list = []

    if isinstance(combat_initiative_list, list) == False:
        combat_initiative_list = []
    else:
        combat_initiative_list.clear()
    if isinstance(room_inst_id.enemies_in_room_list,list):
        for enemy_i in range(0, len(room_inst_id.enemies_in_room_list)):
            combat_initiative_list.append(room_inst_id.enemies_in_room_list[enemy_i])
    if isinstance(room_inst_id.pcs_in_room_list, list):
        for pc_i in range(0, len(room_inst_id.pcs_in_room_list)):
            combat_initiative_list.append(room_inst_id.pcs_in_room_list[pc_i])
            room_inst_id.pcs_in_room_list[pc_i].participated_in_new_turn_battle = True
    if isinstance(room_inst_id.neutrals_in_room_list, list):
        for pc_i in range(0, len(room_inst_id.neutrals_in_room_list)):
            combat_initiative_list.append(room_inst_id.neutrals_in_room_list[pc_i])
            room_inst_id.neutrals_in_room_list[pc_i].participated_in_new_turn_battle = True

    return combat_initiative_list

#organize organize combat_rank_list by each char's starting_combat_rank:
def organize_combat_rank_list(initiative_ar_to_pass):
    #setup ranklist
    rank_list_to_return = []
    for i in range(0,ENUM_RANK_TOTAL_RANKS):
        rank_list_to_return.append([])

    for rank_i in range(0,len(rank_list_to_return)):
        for char_i in range(0,len(initiative_ar_to_pass)):
            combat_rank = initiative_ar_to_pass[char_i].starting_combat_rank
            if combat_rank == rank_i:
                rank_list_to_return[combat_rank].append(initiative_ar_to_pass[char_i])

    return rank_list_to_return

#Organizes the list and returns a new copy of it using character speed as the organizing factor:
#ar_to_pass should be the main.combat_initiative_list, and should already contain all of the combatants involved in the battle.
def organize_initiative_list(ar_to_pass):
    #Determine random values for each char's ran_init_val
    for i in range(0,len(ar_to_pass)):
        if isinstance(ar_to_pass[i],Character):
            char_inst = ar_to_pass[i]
            char_inst.ran_init_val = random.randint(0,ENUM_MAX_RAN_INITIATIVE_VAL) + char_inst.speed
        else:
            print(f"organize_initiative_list: ar_to_pass[i]: {ar_to_pass[i]} was not an instance of Character, something went very wrong.")
            return False

    #Shuffle first to ensure randomness of tie-breakers:
    random.shuffle(ar_to_pass)
    """
    print("organize_initiative_list: debug: before organizing, ar_to_pass looks like:")
    for i in range(0,len(ar_to_pass)):
        print(f"{ar_to_pass[i].name}, with ran_init_val of {ar_to_pass[i].ran_init_val}")
    """

    #Use method to organize ar_to_pass
    ar_to_pass.sort(key=attrgetter('ran_init_val'), reverse = True)

    """
    print("organize_initiative_list: debug: after organizing, ar_to_pass looks like:")
    for i in range(0, len(ar_to_pass)):
        print(f"{ar_to_pass[i].name}, with ran_init_val of {ar_to_pass[i].ran_init_val}")
    """

    return ar_to_pass

#Very simple func:
def return_val_in_list(ar_to_search,val_to_find):
    for i in ar_to_search:
        if i == val_to_find:
            return True

    return False

#Expects and returns a list if list_boolean == true
def wrap_str(string_to_wrap,max_len,list_boolean):

    if not list_boolean:
        wrapped_str = textwrap.fill(string_to_wrap, max_len)
    else:
        wrapped_str = []
        for i in string_to_wrap:
            wrapped_str.append(textwrap.fill(i, max_len))
    return wrapped_str

#endregion
