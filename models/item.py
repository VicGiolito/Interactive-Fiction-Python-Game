
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
        self.max_range = 0 #If 0=melee only

        self.single_use_boolean = False
        self.melee_debuff_boolean = False
        self.equippable_boolean = True
        self.usable_boolean = False
        self.changes_stats_boolean = False

        self.is_shield_boolean = False #Currently only used utils.py function check_for_equipped_weapon()
        self.can_suppress_boolean = False
        self.can_overwatch_boolean = False

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
        self.item_dmg_str = "Not defined"

        self.equip_slot_list = -1 # Default, this means that this item cannot be equipped: such as medkit, etc.

        self.slot_designation_str = ""
        self.item_verb = "fires"
        self.aoe_count = 1 #indicates max targets item will hit; -1 indicates it hits the entire mob, flamers only

        #region Define item stats for each item:

        if self.item_enum == ENUM_ITEM_FLASHLIGHT:
            self.dmg_min = 1
            self.dmg_max = 1
            self.item_name = "FLASHLIGHT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_ACCESSORY]
        elif self.item_enum == ENUM_ITEM_SHOTGUN:
            self.dmg_min = 3
            self.dmg_max = 6
            self.item_name = "SHOTGUN"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "pumps the"
            self.item_dmg_str = "shot"
            self.aoe_count = 3
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_REVOLVER:
            self.dmg_min = 1
            self.dmg_max = 4
            self.max_range = 2
            self.item_name = "REVOLVER"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_LASER_PISTOL:
            self.dmg_min = 1
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.item_name = "LASER PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 3
            self.item_verb = "fires the"
            self.item_dmg_str = "burned"
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_GRENADES:
            self.dmg_min = 4
            self.dmg_max = 8
            self.single_use_boolean = True
            self.item_name = "FRAGMENTATION GRENADE"
            self.max_range = 2
            self.item_verb = "tosses the"
            self.item_dmg_str = "shredded"
            self.aoe_count = 6
        elif self.item_enum == ENUM_ITEM_FLAME_THROWER:
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "FLAMETHROWER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 1
            self.item_verb = "spews fire with the"
            self.item_dmg_str = "burned"
            self.aoe_count = -1
        elif self.item_enum == ENUM_ITEM_ROCKET_LAUNCHER:
            self.dmg_min = 12
            self.dmg_max = 24
            self.single_use_boolean = True
            self.item_name = "ROCKET LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 6
            self.item_verb = "fires the"
            self.item_dmg_str = "exploded"
            self.aoe_count = -1
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_LEAD_PIPE:
            self.dmg_min = 1
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "LEAD PIPE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "blundgeoned"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_MONSTROUS_CLAW:
            self.dmg_min = 2
            self.dmg_max = 5
            self.requires_ammo_boolean = False
            self.item_name = "MONSTROUS CLAWS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swipes with"
            self.item_dmg_str = "slashed"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_LARVA_WRITHING_TENDRIL:
            self.dmg_min = 1
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.item_name = "WRITHING TENDRIL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "whips with a"
            self.item_dmg_str = "slashed"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_DESPERATE_CLAW:
            self.dmg_min = 1
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.item_name = "DESPERATE CLAW"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.item_verb = "slashes with a"
            self.item_dmg_str = "slashed"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_LARVA_INJECTION_BARB:
            self.dmg_min = 3
            self.dmg_max = 3
            self.requires_ammo_boolean = False
            self.item_name = "INFECTED BARB"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "stabs with a"
            self.item_dmg_str = "punctured"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_POLICE_TRUNCHEON:
            self.dmg_min = 3
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "POLICE TRUNCHEON"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "blundgeoned"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_STUN_BATON: #Has a 50% chance of stunning enemies, minus their electric_res
            self.dmg_min = 1
            self.dmg_max = 2
            self.requires_ammo_boolean = False
            self.item_name = "STUN BATON"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "thrusts the"
            self.item_dmg_str = "zapped"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_FIRE_AXE:
            self.dmg_min = 2
            self.dmg_max = 5
            self.requires_ammo_boolean = False
            self.item_name = "FIRE AXE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "mauled"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_TASER: #High stun chance, extra damage to characters with weak electric_res
            self.dmg_min = 1
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "TASER"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "fires the"
            self.item_dmg_str = "zapped"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_ASSAULT_RIFLE:
            self.dmg_min = 5
            self.dmg_max = 10
            self.requires_ammo_boolean = 3
            self.item_name = "ASSAULT RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_suppress_boolean = True
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_SPINE_PROJECTILE:
            self.dmg_min = 2
            self.dmg_max = 6
            self.item_name = "SHOOTING SPINE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires a"
            self.item_dmg_str = "shot"
            self.can_suppress_boolean = True
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_SPINE_PROJECTILE_VENOMOUS:
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "VENOMOUS SPINE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires a"
            self.item_dmg_str = "shot"
            self.can_suppress_boolean = True
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_ACID_SPIT:
            self.dmg_min = 3
            self.dmg_max = 8
            self.item_name = "ACID BILE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "spits with"
            self.item_dmg_str = "melted"
            self.aoe_count = 3
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_ACID_CLOUD:
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "ACID CLOUD"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "belches a massive"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
        elif self.item_enum == ENUM_ITEM_ACID_SACK: #Acts as a proximity mine
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "ACID SACK"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "drops a"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
        elif self.item_enum == ENUM_ITEM_SUB_MACHINE_GUN:
            self.dmg_min = 3
            self.dmg_max = 6
            self.requires_ammo_boolean = 3
            self.item_name = "SUB MACHINE GUN"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_suppress_boolean = True
            self.can_overwatch_boolean = True
            self.aoe_count = 3
        elif self.item_enum == ENUM_ITEM_MACHINE_PISTOL:
            self.dmg_min = 2
            self.dmg_max = 4
            self.requires_ammo_boolean = 3
            self.item_name = "MACHINE PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 2
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_suppress_boolean = True
            self.can_overwatch_boolean = True
            self.aoe_count = 3
        elif self.item_enum == ENUM_ITEM_SNIPER_RIFLE:
            self.dmg_min = 10
            self.dmg_max = 15
            self.requires_ammo_boolean = 1
            self.melee_debuff_boolean = True
            self.item_name = "SNIPER RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 5
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_LASER_RIFLE:
            self.dmg_min = 6
            self.dmg_max = 10
            self.requires_ammo_boolean = False
            self.melee_debuff_boolean = True
            self.item_name = "PULSE RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "burned"
            self.can_overwatch_boolean = True
            self.can_suppress_boolean = True
            self.aoe_count = 2
        elif self.item_enum == ENUM_ITEM_MEDKIT:
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "MED KIT"
            self.equippable_boolean = False
        elif self.item_enum == ENUM_ITEM_KIRAS_NOISY_GAME:
            self.single_use_boolean = False
            self.usable_boolean = True
            self.item_name = "KIRA'S NOISY GAME"
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
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 3
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -1
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_SECURITY_VEST:
            self.item_name = "SECURITY VEST"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 1
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 1
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
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "ADRENAL PEN"
            self.equippable_boolean = False
        elif self.item_enum == ENUM_ITEM_DNA_TESTER:
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
            self.dmg_max = 2
            self.requires_ammo_boolean = False
            self.item_name = "FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "punches with their"
            self.item_dmg_str = "battered"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_FISTS_CHILD:
            self.dmg_min = 0
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "CHILD FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "punches with their"
            self.item_dmg_str = "battered"
            self.max_range = 0
        elif self.item_enum == ENUM_ITEM_FISTS_GIANT:
            self.dmg_min = 2
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "GIANT FISTS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "punches with their"
            self.item_dmg_str = "battered"
            self.max_range = 0

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





