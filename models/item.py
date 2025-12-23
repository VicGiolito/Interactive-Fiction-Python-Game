
from constants import *

import random
import textwrap

class Item:

    # region Constructor event for item stats:
    def __init__(self ,item_enum):

        self.item_enum = item_enum

        self.stat_boost_list = []
        for i in range(0 ,ENUM_ITEM_STAT_BOOST_TOTAL_STATS):
            self.stat_boost_list.append(0)

        # Default values for instance vars for each item:
        self.dmg_min = 0
        self.dmg_max = 0
        self.requires_ammo_boolean = True
        self.accuracy_bonus = 0
        self.max_range = 0 #If any target is targeted beyond this max_range, a to-hit debuff will be applied to the attack
        self.melee_only_boolean = False
        self.max_targets = 1  # If == -1, will hit all targets in that distance group
        self.ammo_per_shot = 1

        self.single_use_boolean = False
        self.melee_debuff_boolean = False
        self.equippable_boolean = True
        self.usable_boolean = False
        self.changes_stats_boolean = False
        self.is_shield_boolean = False #Currently only used utils.py function check_for_equipped_weapon()

        # None of these are in use and are used within the stat_boost_list instead:
        self.vacuum_res = 0
        self.gas_res = 0
        self.fire_res = 0
        self.electrical_res = 0
        self.armor_bonus = 0
        self.evade_bonus = 0
        self.shield_bonus = 0

        self.item_name = "Not defined"
        self.item_desc = "Not defined"

        self.equip_slot_list = -1 # Default, this means that this item cannot be equipped: such as medkit, etc.

        self.slot_designation_str = ""

        #region Define item stats for each item:

        if self.item_enum == ENUM_ITEM_FLASHLIGHT:
            self.dmg_min = 1
            self.dmg_max = 1
            self.item_name = "FLASHLIGHT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_ACCESSORY]
        elif self.item_enum == ENUM_ITEM_SHOTGUN:
            self.dmg_min = 3
            self.dmg_max = 6
            self.max_range = 2
            self.ammo_per_shot = 5
            self.max_targets = 3
            self.item_name = "SHOTGUN"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 1
        elif self.item_enum == ENUM_ITEM_BALLISTIC_PISTOL:
            self.dmg_min = 1
            self.dmg_max = 4
            self.max_range = 2
            self.ammo_per_shot = 1
            self.item_name = "BALLISTIC PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 1
        elif self.item_enum == ENUM_ITEM_LASER_PISTOL:
            self.dmg_min = 1
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.max_range = 3
            self.item_name = "LASER PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 2
        elif self.item_enum == ENUM_ITEM_GRENADES:
            self.dmg_min = 4
            self.dmg_max = 8
            self.max_range = 2
            self.single_use_boolean = True
            self.item_name = "FRAGMENTATION GRENADE"
            self.max_range = 1
        elif self.item_enum == ENUM_ITEM_FLAME_THROWER:
            self.max_range = 1
            self.dmg_min = 3
            self.dmg_max = 6
            self.max_targets = -1
            self.item_name = "FLAMETHROWER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_ROCKET_LAUNCHER:
            self.max_range = 6
            self.dmg_min = 12
            self.dmg_max = 24
            self.max_range = 6
            self.single_use_boolean = True
            self.item_name = "ROCKET LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
        elif self.item_enum == ENUM_ITEM_LEAD_PIPE:
            self.dmg_min = 1
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.item_name = "LEAD PIPE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True
        elif self.item_enum == ENUM_ITEM_FIRE_AXE:
            self.dmg_min = 2
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "FIRE AXE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True
        elif self.item_enum == ENUM_ITEM_TASER:
            self.dmg_min = 1
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "TASER"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True
        elif self.item_enum == ENUM_ITEM_ASSAULT_RIFLE:
            self.dmg_min = 5
            self.dmg_max = 10
            self.max_range = 3
            self.requires_ammo_boolean = 3
            self.max_targets = 2
            self.item_name = "ASSAULT RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
        elif self.item_enum == ENUM_ITEM_SNIPER_RIFLE:
            self.dmg_min = 10
            self.dmg_max = 15
            self.max_range = 4
            self.requires_ammo_boolean = 1
            self.max_targets = 1
            self.melee_debuff_boolean = True
            self.item_name = "SNIPER RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
        elif self.item_enum == ENUM_ITEM_MEDKIT:
            self.max_targets = 1
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "MED KIT"
            self.equippable_boolean = False
        elif self.item_enum == ENUM_ITEM_SUIT_ENVIRONMENTAL:
            self.fire_res = 50
            self.electrical_res = 50
            self.gas_res = 100
            self.armor_bonus = 1
            self.evade_bonus = -1
            self.item_name = "HAZMAT SUIT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -1
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 1
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_FIRE_RES] = 50
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ELECTRIC_RES] = 50
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_GAS_RES] = 100
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_PRISONER_JUMPSUIT:
            self.item_name = "PRISONER JUMPSUIT"
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
        elif self.item_enum == ENUM_ITEM_ENGINEER_GARB:
            self.item_name = "ENGINEER GARB"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_SCIENTIST_LABCOAT:
            self.item_name = "SCIENTIST LABCOAT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_MEDICAL_SCRUBS:
            self.item_name = "MEDICAL SCRUBS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_OFFICER_JUMPSUIT:
            self.item_name = "OFFICER JUMPSUIT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_CIVILIAN_JUMPSUIT:
            self.item_name = "CIVILIAN JUMPSUIT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_FLAK_ARMOR:
            self.item_name = "FLAK ARMOR"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 2
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_SUIT_MARINE:
            self.item_name = "MARINE ARMOR"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 5
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ELECTRIC_RES] = 100
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -3
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_VACUUM_RES] = 50
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_GAS_RES] = 100
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_FIRE_RES] = 100
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_ADRENAL_PEN:
            self.max_targets = 1
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "ADRENAL PEN"
            self.equippable_boolean = False
        elif self.item_enum == ENUM_ITEM_DNA_TESTER:
            self.max_targets = 1
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "DNA ANALYZER"
            self.equippable_boolean = False
        elif self.item_enum == ENUM_ITEM_TARGETING_HUD:
            self.item_name = "TACTICAL MONOCLE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_ACCESSORY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ACCURACY] = 1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_RIOT_SHIELD:
            self.item_name = "RIOT SHIELD"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.changes_stats_boolean = True
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 1
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
            self.is_shield_boolean = True
        elif self.item_enum == ENUM_ITEM_FLAK_SHIELD:
            self.item_name = "FLAK SHIELD"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.changes_stats_boolean = True
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 2
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 2
            self.is_shield_boolean = True
        elif self.item_enum == ENUM_ITEM_PHASE_SHIELD:
            self.item_name = "PHASE SHIELD"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.changes_stats_boolean = True
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 3
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 4
            self.is_shield_boolean = True
        elif self.item_enum == ENUM_ITEM_FISTS_ADULT:
            self.dmg_min = 1
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True
        elif self.item_enum == ENUM_ITEM_FISTS_CHILD:
            self.dmg_min = 0
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "CHILD FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True
        elif self.item_enum == ENUM_ITEM_FISTS_GIANT:
            self.dmg_min = 2
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "GIANT FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.melee_only_boolean = True

        #Define slot_designation_str - currently only using the Accessory string, print_inv gets too cluttered otherwise
        if isinstance(self.equip_slot_list,list):
            if isinstance(self.equip_slot_list[0],list):
                self.slot_designation_str = "Both Hands"
            elif self.equip_slot_list[0] == ENUM_EQUIP_SLOT_RH or self.equip_slot_list[0] == ENUM_EQUIP_SLOT_RH:
                self.slot_designation_str = "One Hand"
            elif self.equip_slot_list[0] == ENUM_EQUIP_SLOT_ACCESSORY:
                self.slot_designation_str = "Accessory"
            elif self.equip_slot_list[0] == ENUM_EQUIP_SLOT_BODY:
                self.slot_designation_str = "Body"

        # endregion

    def print_item_desc(self):
        print(f"print_item_desc method called for item with name: {self.item_name}")
        wrapped_item_desc_str = textwrap.fill(self.item_desc, TOTAL_LINE_W)
        print(wrapped_item_desc_str)
        print("")

    def use_item(self):
        print(f"use_item method for item with name: {self.item_name} hasn't been completed yet.\n")





