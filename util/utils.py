
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
from models.room import Room


#region Define help funcs and essential funcs

def build_overwatch_list(moving_char_id,combat_initiative_list):
    overwatch_attacker_list = []
    moving_char_team = moving_char_id.char_team_enum

    #Iterate through combat_init_list, adding Chars to the overwatch_attacker_list if they're of the
    #opposing team, and their self.overwatch_rank == moving_char_id.current_rank
    for i in range(0,len(combat_initiative_list)):

        char_id = combat_initiative_list[i]

        if moving_char_team == ENUM_CHAR_TEAM_ENEMY:

            if char_id.char_team_enum == ENUM_CHAR_TEAM_PC or char_id.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:

                if char_id.overwatch_rank == moving_char_id.cur_combat_rank and char_id.will_overwatch_boolean:

                    overwatch_attacker_list.append(char_id)

        elif moving_char_team == ENUM_CHAR_TEAM_PC or moving_char_team == ENUM_CHAR_TEAM_NEUTRAL:

            if (char_id.char_team_enum == ENUM_CHAR_TEAM_ENEMY and
            char_id.overwatch_rank == moving_char_id.cur_combat_rank and char_id.will_overwatch_boolean):

                overwatch_attacker_list.append(char_id)

    return overwatch_attacker_list

#if check_overwatch_or_suppress_boolean == true: we check for overwatch; if false: we check for suppress.
#returns true if the specified wep ability is available; returns false otherwise
def return_overwatch_or_suppress_capable(char_id,check_overwatch_or_suppress_boolean):
    for i in range(ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH+1):
        if isinstance(char_id.inv_list[i], Item):
            item_id = char_id.inv_list[i]
            if check_overwatch_or_suppress_boolean:
                if item_id.can_overwatch_boolean:
                    #print(f"Debug: return_overwatch_or_suppress_capable: check_overwatch_or_suppress_boolean == {check_overwatch_or_suppress_boolean}, returning TRUE")
                    return True
            elif not check_overwatch_or_suppress_boolean:
                if item_id.can_suppress_boolean:
                    #print(f"Debug: return_overwatch_or_suppress_capable: check_overwatch_or_suppress_boolean == {check_overwatch_or_suppress_boolean}, returning TRUE")
                    return True
    #print(f"Debug: return_overwatch_or_suppress_capable: check_overwatch_or_suppress_boolean == {check_overwatch_or_suppress_boolean}, returning FALSE")
    return False

def advance_or_withdraw_char(move_dir,combat_rank_list,cur_combat_char):
    # Add to next rank in combat_rank_list
    combat_rank_list[cur_combat_char.cur_combat_rank + move_dir].append(cur_combat_char)
    # Remove from cur rank in combat_rank_list
    combat_rank_list[cur_combat_char.cur_combat_rank].remove(cur_combat_char)
    #Update rank:
    cur_combat_char.cur_combat_rank += move_dir
    #print results - whether a character is 'withdrawing' or 'advancing' depends upon their team perspective
    if move_dir == -1:
        if cur_combat_char.char_team_enum != ENUM_CHAR_TEAM_ENEMY:
            print(f"{cur_combat_char.name} advances...\n")
        else:
            print(f"{cur_combat_char.name} withdraws...\n")
    elif move_dir == 1:
        if cur_combat_char.char_team_enum != ENUM_CHAR_TEAM_ENEMY:
            print(f"{cur_combat_char.name} withdraws...\n")
        else:
            print(f"{cur_combat_char.name} advances...\n")
    else:
        print(f"advance_or_withdraw_char: move_dir != -1 or 1, something went wrong. move_dir == {move_dir}.")

    return combat_rank_list

    #Simply returns true if either the ENUM_EQUIP_SLOT_RH or ENUM_EQUIP_SLOT_LH are found in equip_slot_list

def check_equip_slot_list_for_rh_or_lh(equip_slot_list):
    for i in range(0,len(equip_slot_list)):
        if isinstance(equip_slot_list[i],list):
            for nested_i in range(0,len(equip_slot_list[i])):
                if (equip_slot_list[i][nested_i] == ENUM_EQUIP_SLOT_RH or
                        equip_slot_list[i][nested_i] == ENUM_EQUIP_SLOT_LH):
                    return True
        else:
            if equip_slot_list[i] == ENUM_EQUIP_SLOT_RH or equip_slot_list[i] == ENUM_EQUIP_SLOT_LH:
                return True

    return False

#Returns TRUE if the combat has concluded
def check_combat_end_condition(cur_combat_room_id):

    if isinstance(cur_combat_room_id.enemies_in_room_list, list):
        if len(cur_combat_room_id.enemies_in_room_list) <= 0:
            print("The last enemy in this room has either fled or been killed!\n")
            return True
    if isinstance(cur_combat_room_id.pcs_in_room_list, list):
        if len(cur_combat_room_id.pcs_in_room_list) <= 0:
            print("The last friendly character in this room has either fled or been killed!\n")
            return True

    return False

def return_fists_enum(char_inst_id):
    if char_inst_id.char_type_enum == ENUM_CHARACTER_GAMER:
        fists_item_enum = ENUM_ITEM_FISTS_CHILD
    elif char_inst_id.char_type_enum == ENUM_CHARACTER_OGRE:
        fists_item_enum = ENUM_ITEM_FISTS_GIANT
    else:
        fists_item_enum = ENUM_ITEM_FISTS_ADULT

    return fists_item_enum

def destroy_combatant_inst(combat_rank_list, combat_initiative_list, filtered_enemy_list,destroyed_combatant_id,destroyed_combatant_rank_int,cur_combat_room_id, pc_char_list,enemy_char_list,neutral_char_list):
    # Remove from combat_rank_list:
    combat_rank_list[destroyed_combatant_rank_int].remove(destroyed_combatant_id)
    # Remove from combat_initiative_list:
    combat_initiative_list.remove(destroyed_combatant_id)
    # Remove from filtered_enemy_list:
    filtered_enemy_list.remove(destroyed_combatant_id)
    # Remove from corresponding list in room:
    if destroyed_combatant_id.char_team_enum == ENUM_CHAR_TEAM_PC:
        pc_char_list.remove(destroyed_combatant_id)
        cur_combat_room_id.pcs_in_room_list.remove(destroyed_combatant_id)
    elif destroyed_combatant_id.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
        enemy_char_list.remove(destroyed_combatant_id)
        cur_combat_room_id.enemies_in_room_list.remove(destroyed_combatant_id)
    elif destroyed_combatant_id.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:
        neutral_char_list.remove(destroyed_combatant_id)
        cur_combat_room_id.neutrals_in_room_list.remove(destroyed_combatant_id)
    #Not strictly necessary, but good practice:
    del destroyed_combatant_id
    #Always need to return the globals:
    return combat_rank_list, combat_initiative_list, filtered_enemy_list, pc_char_list, enemy_char_list,neutral_char_list

def advance_combat_cur_char(cur_combat_char,combat_initiative_list,cur_combat_room_id,cur_combat_round, prev_index_for_cur_combat_char):
    #Deliberately throw error is cur_combat_char is not even an instance of the char class:
    if isinstance(cur_combat_char,Character) == False:
        print(f"advance_combat_cur_char: ERROR: cur_combat_char did not even == an instance of Character. It == {cur_combat_char}. Throw error: {cur_combat_char.non_existant_attribute}")

    # Advance cur_combat_char global var:
    try:
        cur_index = combat_initiative_list.index(cur_combat_char)
    #If they died during the course of their turn (such as while withdrawing or advancing under overwatch),
    #then just use their previous index from when before they died as a reference:
    except ValueError:
        print(f"Debug: advance_combat_cur_char: cur_index for the {cur_combat_char.name} could not be found, which means they were killed and deleted from the combat_init_list; therefore we're using the prev_index_for_cur_combat_char: {prev_index_for_cur_combat_char} as reference instead. We'll attempt to adjust it by - 1 and use it, or 0.")
        #They were deleted from the list, so we need to adjust the cur_index appropriately:
        if prev_index_for_cur_combat_char - 1 >= 0:
            cur_index = prev_index_for_cur_combat_char-1
        else:
            cur_index = 0
        print(f"Debug: advance_combat_cur_char: cur_index now == {cur_index}. We had to adjust it b.c the {cur_combat_char.name} couldn't be found in the combat_init_list.")

    # check to see if we need to fill and reorganize the combat_initiative_list:
    if cur_index + 1 >= len(combat_initiative_list):
        # Setup combat init list
        combat_initiative_list = fill_combat_initiative_list(cur_combat_room_id)
        # Organize it by speed:
        combat_initiative_list = organize_initiative_list(combat_initiative_list)
        # Assign global cur_combat_char as the first index position:
        cur_combat_char = combat_initiative_list[0]
        #Increment round
        cur_combat_round += 1
        #Print round change:
        print(f"... Round {cur_combat_round} begins... \n")
    else:
        # Assign cur_combat_char as the next char in our initiative_list
        cur_combat_char = combat_initiative_list[cur_index + 1]

    #Now that the cur_combat_char has been defined, reset various 1-turn-only vars for them:
    # Reset their dodge_bonus_boolean
    cur_combat_char.dodge_bonus_boolean = False
    cur_combat_char.will_suppress_boolean = False
    cur_combat_char.will_overwatch_boolean = False

    # Move to assign commands or execute ai
    if cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_PC:
        cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
    else:
        cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION

    # Always need to return the globals:
    return cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list

def return_distance_between_ranks(rank_1,rank_2):
    dist_between_ranks = abs(rank_1 - rank_2)
    return dist_between_ranks

def check_for_equipped_weapon(char_id):
    if isinstance(char_id.inv_list,list):
        for i in range(0,len(char_id.inv_list)):
            if isinstance(char_id.inv_list[i],Item):
                if char_id.inv_list[i].is_shield_boolean == False:
                    #This char has at least 1 non-shield item, equipped return true
                    return True

    return False

def return_accuracy_debuff(coord_1, coord_2,item_max_range):
    accuracy_debuff = 0
    dist_to_target = abs(coord_1 - coord_2)
    if dist_to_target > item_max_range:
        accuracy_debuff = abs(dist_to_target - item_max_range)

    return accuracy_debuff

def print_combat_ranks(combat_rank_list,show_distance_debuff = False, item_max_range = 0,acting_char_rank = 0):

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

        # Defunct - no longer using this feature: Add accuracy debuff information if requested
        """
        if show_distance_debuff and item_max_range != -1:
            accuracy_debuff = return_accuracy_debuff(acting_char_rank, i, item_max_range)
            rank_str += f" - accuracy change: {-accuracy_debuff}"
        """

        #Add ' *BEYOND WEAPON'S RANGE* ' to positions beyond this character's item.max_range:
        if show_distance_debuff and item_max_range != -1:
            dist_between_ranks = return_distance_between_ranks(acting_char_rank,i)
            if dist_between_ranks > item_max_range:
                rank_str += f" **BEYOND WEAPON'S RANGE** "

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
