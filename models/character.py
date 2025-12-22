
from constants import *
from models.item import Item
from util.utils import *

import random
import textwrap

class Character:

    # region Constructor event for character stats:
    def __init__(self, char_type_enum, spawn_grid_x, spawn_grid_y, spawn_grid, char_team_enum):

        # Default values for instance vars for this particularly character:
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.dexterity = 0
        self.accuracy = 0
        self.stealth = 0

        self.security = 0
        self.engineering = 0
        self.science = 0
        self.scavenging = 0 # Not currently used

        self.hp_cur = 0
        self.hp_max = 0
        self.ability_points_cur = 0
        self.ability_points_max = 0
        self.sanity_cur = 0
        self.sanity_max = 0

        self.armor = 0
        self.evasion = 0
        self.res_fire = 0
        self.res_vacuum = 0
        self.res_gas = 0
        self.res_electric = 0

        self.cur_action_points = 2
        self.max_action_points = 2

        self.inv_list = []

        self.char_team_enum = char_team_enum

        self.name = "Not defined"

        # Initialize inv_list and nested ENUM_EQUIP_BACKLIST_LIST:
        for i in range(0 ,ENUM_EQUIP_SLOT_TOTAL_SLOTS):
            self.inv_list.append(-1)

        self.char_type_enum = char_type_enum
        self.current_grid = spawn_grid
        self.cur_grid_x = spawn_grid_x
        self.cur_grid_y = spawn_grid_y

        if char_type_enum == ENUM_CHARACTER_OGRE:

            self.name = "Cragos, 'The Ogre'"
            self.hp_max = 16
            self.hp_cur = 16
            self.ability_points_cur = 5
            self.ability_points_max = 5
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 1
            self.security = 5
            self.science = 0
            self.scavenging = 0
            self.stealth = 0

            self.strength = 7
            self.intelligence = 0
            self.wisdom = 1
            self.dexterity = 0

            self.armor = 1

            # Starting equipment:
            # item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            # self.equip_item(item_to_equip,item_to_equip.equip_slot_enum,True)
            item_to_equip = Item(ENUM_ITEM_SUIT_MARINE)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)

        elif char_type_enum == ENUM_CHARACTER_BIOLOGIST:
            self.name = "Revita, 'The Biologist'"
            self.hp_max = 6
            self.hp_cur = 6
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 8
            self.sanity_max = 8

            self.engineering = 2
            self.security = 0
            self.science = 5
            self.scavenging = 0
            self.stealth = 2

            self.strength = 0
            self.intelligence = 5
            self.wisdom = 3
            self.dexterity = 0

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_MEDICAL_SCRUBS)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)
            item_to_equip = Item(ENUM_ITEM_MEDKIT)
            self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_ENGINEER:
            self.name = "Amos, 'The Engineer'"
            self.hp_max = 8
            self.hp_cur = 8
            self.ability_points_cur = 4
            self.ability_points_max = 4
            self.sanity_cur = 6
            self.sanity_max = 6

            self.engineering = 5
            self.security = 0
            self.science = 2
            self.scavenging = 0
            self.stealth = 1

            self.strength = 2
            self.intelligence = 2
            self.wisdom = 3
            self.dexterity = 1

            # Starting equipment
            # item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
            # self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
            item_to_equip = Item(ENUM_ITEM_SUIT_ENVIRONMENTAL)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)

        elif char_type_enum == ENUM_CHARACTER_JANITOR:
            self.name = "Johns, 'The Janitor'"
            self.hp_max = 7
            self.hp_cur = 7
            self.ability_points_cur = 5
            self.ability_points_max = 5
            self.sanity_cur = 6
            self.sanity_max = 6

            self.engineering = 2
            self.security = 0
            self.science = 0
            self.scavenging = 5
            self.stealth = 4

            self.strength = 2
            self.intelligence = 2
            self.wisdom = 2
            self.dexterity = 2

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_MECH_MAGICIAN:
            self.name = "Avia, 'The Mechanician'"
            self.hp_max = 5
            self.hp_cur = 5
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 3
            self.security = 1
            self.science = 2
            self.scavenging = 1
            self.stealth = 2

            self.strength = 1
            self.intelligence = 3
            self.wisdom = 3
            self.dexterity = 1

            self.res_fire = 50
            self.res_vacuum = 50
            self.res_gas = 50
            self.res_electric = -50

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_MERCENARY_MECH:
            self.name = "Torvald, 'The Cyborg'"
            self.hp_max = 12
            self.hp_cur = 12
            self.ability_points_cur = 8
            self.ability_points_max = 8
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 1
            self.security = 4
            self.science = 1
            self.scavenging = 1
            self.stealth = 1

            self.strength = 4
            self.intelligence = 2
            self.wisdom = 1
            self.dexterity = 1

            self.armor = 1

            self.res_fire = 50
            self.res_vacuum = 50
            self.res_gas = 50
            self.res_electric = -50

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_SOLDIER:
            self.name = "Cooper, 'The Security Guard'"
            self.hp_max = 10
            self.hp_cur = 10
            self.ability_points_cur = 14
            self.ability_points_max = 14
            self.sanity_cur = 9
            self.sanity_max = 9

            self.engineering = 1
            self.security = 4
            self.science = 0
            self.scavenging = 2
            self.stealth = 1

            self.strength = 3
            self.intelligence = 1
            self.wisdom = 2
            self.dexterity = 2

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_FLAK_ARMOR)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)
            item_to_equip = Item(ENUM_ITEM_ASSAULT_RIFLE)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)
            item_to_equip = Item(ENUM_ITEM_TARGETING_HUD)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum, True)
            item_to_equip = Item(ENUM_ITEM_BALLISTIC_PISTOL)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_TASER)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_FLASHLIGHT)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_ADRENAL_PEN)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_SUIT_MARINE)
            self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_SCIENTIST:
            self.name = "Darius, 'The Physicist'"
            self.hp_max = 5
            self.hp_cur = 5
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 6
            self.sanity_max = 6

            self.engineering = 0
            self.security = 0
            self.science = 6
            self.scavenging = 1
            self.stealth = 3

            self.strength = 3
            self.intelligence = 1
            self.wisdom = 2
            self.dexterity = 2

            item_to_equip = Item(ENUM_ITEM_SCIENTIST_LABCOAT)
            self.equip_item(item_to_equip ,item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_CRIMINAL:
            self.name = "Emeran, 'The Criminal'"
            self.hp_max = 9
            self.hp_cur = 9
            self.ability_points_cur = 12
            self.ability_points_max = 12
            self.sanity_cur = 9
            self.sanity_max = 9

            self.engineering = 0
            self.security = 3
            self.science = 0
            self.scavenging = 4
            self.stealth = 4

            self.strength = 4
            self.intelligence = 0
            self.wisdom = 0
            self.dexterity = 4

            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip ,item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_SERVICE_DROID:
            self.name = "RG-88, 'Service Droid'"
            self.hp_max = 14
            self.hp_cur = 14
            self.ability_points_cur = 15
            self.ability_points_max = 15
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 3
            self.security = 2
            self.science = 3
            self.scavenging = 0
            self.stealth = 0

            self.strength = 0
            self.intelligence = 4
            self.wisdom = 4
            self.dexterity = 0

            self.res_fire = 100
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = -100

        elif char_type_enum == ENUM_CHARACTER_CEO:
            self.name = "Jens, 'The CEO'"
            self.hp_max = 7
            self.hp_cur = 7
            self.ability_points_cur = 8
            self.ability_points_max = 8
            self.sanity_cur = 4
            self.sanity_max = 4

            self.engineering = 2
            self.security = 0
            self.science = 2
            self.scavenging = 3
            self.stealth = 2

            self.strength = 1
            self.intelligence = 3
            self.wisdom = 2
            self.dexterity = 1

            item_to_equip = Item(ENUM_ITEM_OFFICER_JUMPSUIT)
            self.equip_item(item_to_equip ,item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_GAMER:
            self.name = "Kira, 'The Gamer'"
            self.hp_max = 3
            self.hp_cur = 3
            self.ability_points_cur = 6
            self.ability_points_max = 6
            self.sanity_cur = 5
            self.sanity_max = 5

            self.engineering = 1
            self.security = 0
            self.science = 1
            self.scavenging = 5
            self.stealth = 5

            self.strength = 0
            self.intelligence = 2
            self.wisdom = 1
            self.dexterity = 5

            item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
            self.equip_item(item_to_equip ,item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_PLAYBOY:
            self.name = "Oberon, 'The Playboy'"
            self.hp_max = 8
            self.hp_cur = 8
            self.ability_points_cur = 6
            self.ability_points_max = 6
            self.sanity_cur = 3
            self.sanity_max = 3

            self.engineering = 0
            self.security = 0
            self.science = 0
            self.scavenging = 3
            self.stealth = 3

            self.strength = 2
            self.intelligence = 2
            self.wisdom = 1
            self.dexterity = 3

            item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
            self.equip_item(item_to_equip ,item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_INFECTED_SCIENTIST:
            self.name = "Gregos, 'The Researcher'"
            self.hp_max = 5
            self.hp_cur = 2
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 2
            self.sanity_max = 2

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_SCIENTIST_LABCOAT)
            self.equip_item(item_to_equip, item_to_equip.equip_slot_enum ,True)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_SKITTERING_LARVA:
            self.name = "Skittering Larva"
            self.hp_max = 3
            self.hp_cur = 3
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20

            self.armor = 0
            self.evasion = 3
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0

        elif char_type_enum == ENUM_CHARACTER_ENEMY_LUMBERING_MAULER:
            self.name = "Lumbering Mauler"
            self.hp_max = 18
            self.hp_cur = 18
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20

            self.armor = 1
            self.evasion = 0
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0

        elif char_type_enum == ENUM_CHARACTER_ENEMY_SPINED_SPITTER:
            self.name = "Spined Spitter"
            self.hp_max = 10
            self.hp_cur = 10
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20

            self.armor = 0
            self.evasion = 0
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0


    # endregion

    def print_char_inv(self):

        print(f"{self.name} is wearing and carrying the following items:")

        # Print body slot:
        item_slot_str = "Nothing"
        if isinstance(self.inv_list[ENUM_EQUIP_SLOT_BODY], Item):
            item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_BODY].item_name
        print(f"Wearing on body: 0.) {item_slot_str}")

        # Print accessory slot:
        item_slot_str = "Nothing"
        if isinstance(self.inv_list[ENUM_EQUIP_SLOT_ACCESSORY], Item):
            item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_ACCESSORY].item_name
        print(f"Also wearing: 1.) {item_slot_str}")

        # Print Hands slot:
        item_slot_str = "Nothing"
        if isinstance(self.inv_list[ENUM_EQUIP_SLOT_HANDS], Item):
            item_slot_str = self.inv_list[ENUM_EQUIP_SLOT_HANDS].item_name
        print(f"Wielding in hands: 2.) {item_slot_str}")

        # Print backpack items
        print("They are carrying on their person:")

        for i in range(ENUM_EQUIP_SLOT_TOTAL_SLOTS ,len(self.inv_list)):
            if isinstance(self.inv_list[i], Item): # If there's actually an item here
                print(f"{i}.) {self.inv_list[i].item_name}")
            else:
                # print for debug purposes:
                print(f"{self.inv_list[i]}")

        print("")
        print \
            ("Simply enter the associated number to use, equip, unequip, or swap an item; or enter 'BACK' to leave the inventory screen.")
        print("You can also enter 'L{ITEM NUMBER} to get a description of the corresponding item;")
        print("Or 'G{ITEM NUMBER} to give the corresponding item to another player;")
        print \
            ("Or 'D{ITEM NUMBER} to drop the item back into your current room (you could retrieve it again with 'SCAVENGE').")
        print("Enter your selection now >")

    def equip_item(self ,item_inst_id ,item_index ,starting_equip_boolean = False):
        if item_inst_id.equip_slot_enum != -1:
            self.inv_list[item_inst_id.equip_slot_enum] = item_inst_id
            # Only remove from backpack if item_index points to a backpack slot; this is necessary because when we're adding an item
            # for the first time as part of a character's starting kit, it doesn't yet exist as one of the 'backpack slots'
            if item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS and item_index < len(self.inv_list):
                # Remove corresponding position in list, this should be one of the 'backpack' indices:
                del self.inv_list[item_index]
        else:
            print \
                (f"equip_item method for {self.name} with item: {item_inst_id.item_name}, equip_slot_enum == -1, which means we're trying to equip an item that is not equippable, something went wrong.")
        if not starting_equip_boolean:
            print(f"{self.name} has equipped the {item_inst_id.item_name}")
        if item_inst_id.changes_stats_boolean:
            self.change_char_stats(item_inst_id, True ,starting_equip_boolean)

    def unequip_item(self ,item_inst_id ,starting_equip_boolean = False):
        # Remove from current list position, add to end of list:
        self.inv_list[item_inst_id.equip_slot_enum] = -1
        # add to end of list:
        self.inv_list.append(item_inst_id)
        print(f"{self.name} has unequipped the {item_inst_id.item_name}")
        if item_inst_id.changes_stats_boolean:
            self.change_char_stats(item_inst_id, False ,starting_equip_boolean)

    def swap_equip_item(self ,first_item_id ,first_item_index ,second_item_id ,second_item_index
                        ,starting_equip_boolean = False):
        self.inv_list[first_item_index] = second_item_id
        self.inv_list[second_item_index] = first_item_id
        print(f"{self.name} has unequipped the {first_item_id.item_name}, and equipped the {second_item_id.item_name}")
        if first_item_id.changes_stats_boolean:
            self.change_char_stats(first_item_id ,False ,starting_equip_boolean)
        if second_item_id.changes_stats_boolean:
            self.change_char_stats(second_item_id, True ,starting_equip_boolean)

    def add_item_to_backpack(self ,item_id_to_add ,starting_equip_boolean = False):
        self.inv_list.append(item_id_to_add)
        if not starting_equip_boolean:
            print(f"{self.name} has picked up the {item_id_to_add.item_name}")

    def drop_item_into_room(self ,item_id ,item_index ,room_inst_id):
        # Change stats:
        if item_id.changes_stats_boolean == True:
            self.change_char_stats(item_id ,False, False)
        if item_index < ENUM_EQUIP_SLOT_TOTAL_SLOTS:
            self.inv_list[item_index] = -1 # Change corresponding slot to 'empty'
        elif item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
            # Delete corresponding position in one of the 'backpack slots':
            del self.inv_list[item_index]
        # Add to room scavenge list:
        # Create scavenge_resource_list for room_inst_id:
        if isinstance(room_inst_id.scavenge_resource_list, list) == False:
            room_inst_id.scavenge_resource_list = []
            for i in range(0 ,ENUM_EQUIP_SLOT_TOTAL_SLOTS):
                room_inst_id.scavenge_resource_list.append(-1)
            room_inst_id.scavenge_resource_list.append(item_id)
        else:
            # Extend the length of the room_inst_id.scavenge_resource_list if necessary, adding -1 to non-existant indices:
            """
            if len(room_inst_id.scavenge_resource_list) <= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                # The '*' here is an overloaded operand and doesn't actually represent multiplcation; it represents 'copying' a list element that many times, in this case: [-1] is copied into the list a certain amount of times until the length is exactly where we want it
                room_inst_id.scavenge_resource_list.extend([-1] * (ENUM_EQUIP_SLOT_TOTAL_SLOTS - len(room_inst_id.scavenge_resource_list)))
            """
            # Now append item_id (which will be at either index ENUM_EQUIP_SLOT_TOTAL_SLOTS if we extended our list match, or beyond that at the end of the list, if the len of the list was already > ENUM_EQUIP_SLOT_TOTAL_SLOTS)
            room_inst_id.scavenge_resource_list.append(item_id)

        print \
            (f"{self.name} has dropped the {item_id.item_name}. It can be retrieved again from this room using the 'SCAVENGE' command.")
        print("")

    def change_char_stats(self ,item_id ,equipping_boolean ,starting_equip_boolean):
        # If equipping_boolean == false, we're ADDING the effect of the item stat
        # elif equipping_boolean == True, we're REMOVING the effect of the item stat
        addition_int = 1
        if not equipping_boolean:
            addition_int = -1
        # region Iterate through stat_boost_list, adding/removing the corresponding stat from the char_inst:
        mod_amount_list = []
        stat_str_list = []
        for i in range(0 ,len(item_id.stat_boost_list)):
            # Define mod amount:
            mod_amount = item_id.stat_boost_list[i] * addition_int

            if i == ENUM_ITEM_STAT_BOOST_HP and mod_amount != 0:
                stat_str_list.append("Maximum Hit Points")
                mod_amount_list.append(str(mod_amount))
                self.hp_max += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_SCAVENGING and mod_amount != 0:
                stat_str_list.append("Maximum Hit Points")
                mod_amount_list.append(str(mod_amount))
                self.scavenging += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ACCURACY and mod_amount != 0:
                stat_str_list.append("Accuracy")
                mod_amount_list.append(str(mod_amount))
                self.accuracy += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_SECURITY and mod_amount != 0:
                stat_str_list.append("Security")
                mod_amount_list.append(str(mod_amount))
                self.security += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ENGINEERING and mod_amount != 0:
                stat_str_list.append("Engineering")
                mod_amount_list.append(str(mod_amount))
                self.engineering += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_SCIENCE and mod_amount != 0:
                stat_str_list.append("Science")
                mod_amount_list.append(str(mod_amount))
                self.science += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_STEALTH and mod_amount != 0:
                stat_str_list.append("Stealth")
                mod_amount_list.append(str(mod_amount))
                self.stealth += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ABILITY_POINTS and mod_amount != 0:
                stat_str_list.append("Ability Points")
                mod_amount_list.append(str(mod_amount))
                self.ability_points_max += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ACTION_POINTS and mod_amount != 0:
                stat_str_list.append("Action Points")
                mod_amount_list.append(str(mod_amount))
                self.action_points += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_SANITY and mod_amount != 0:
                stat_str_list.append("Sanity")
                mod_amount_list.append(str(mod_amount))
                self.sanity_max += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_STRENGTH and mod_amount != 0:
                stat_str_list.append("Strength")
                mod_amount_list.append(str(mod_amount))
                self.strength += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_DEXTERITY and mod_amount != 0:
                stat_str_list.append("Dexterity")
                mod_amount_list.append(str(mod_amount))
                self.dexterity += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_INTELLIGENCE and mod_amount != 0:
                stat_str_list.append("Intelligence")
                mod_amount_list.append(str(mod_amount))
                self.intelligence += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_WISDOM and mod_amount != 0:
                stat_str_list.append("Wisdom")
                mod_amount_list.append(str(mod_amount))
                self.wisdom += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ARMOR and mod_amount != 0:
                stat_str_list.append("Armor")
                mod_amount_list.append(str(mod_amount))
                self.armor += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_EVASION and mod_amount != 0:
                stat_str_list.append("Evasion")
                mod_amount_list.append(str(mod_amount))
                self.evasion += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_VACUUM_RES and mod_amount != 0:
                stat_str_list.append("Vacuum Res.")
                mod_amount_list.append(str(mod_amount))
                self.res_vacuum += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_GAS_RES and mod_amount != 0:
                stat_str_list.append("Gas Res.")
                mod_amount_list.append(str(mod_amount))
                self.res_gas += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_FIRE_RES and mod_amount != 0:
                stat_str_list.append("Fire Res.")
                mod_amount_list.append(str(mod_amount))
                self.res_fire += mod_amount
            elif i == ENUM_ITEM_STAT_BOOST_ELECTRIC_RES and mod_amount != 0:
                stat_str_list.append("Electric Res.")
                mod_amount_list.append(str(mod_amount))
                self.res_electric += mod_amount

        # endregion
        if not starting_equip_boolean: # Only print any of this if the equipment was used after the game actually started:
            # Concatenate each element in the stat_str_list with each corresponding element in the mod_amount_list:
            joined_stat_str = ""
            for i in range(0 ,len(stat_str_list)):
                semicolon_str = ""
                if i < (len(stat_str_list) - 1):
                    semicolon_str = "; "
                joined_stat_str += stat_str_list[i ] +" by  " +mod_amount_list[i ] +semicolon_str
            # Combine into result string:
            result_str = f"{self.name} has had their following stats modified: {joined_stat_str}."
            # Wrap string based upon length:
            wrapped_result_str = textwrap.fill(result_str, TOTAL_LINE_W)
            print(wrapped_result_str)

    def print_char_stats(self):
        print(f"{self.name} has the following stats:")
        char_stats_str = f"Security: {self.security}, Engineering: {self.engineering}, Science: {self.science}, Stealth: {self.stealth}, Strength: {self.strength}, Intelligence: {self.intelligence}, Widsom: {self.wisdom}, Dexterity: {self.dexterity}, Accuracy: {self.accuracy}, Vacuum Res.: {self.res_vacuum}, Fire Res.: {self.res_fire}, Electric Res.: {self.res_fire}, Gas Res.: {self.res_gas}."
        char_stats_str = textwrap.fill(char_stats_str, TOTAL_LINE_W)
        print(char_stats_str)
        print("")
