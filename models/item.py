
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
        self.combat_usable_boolean = False #Used in conjunction with items that can ALSO be used by characters in combat, like adrenal pen.
        self.use_script  = -1 #For items or abilities that are 'used'
        self.use_requires_target_boolean = False #For items or abilities that are 'used', usually destroyed after, and require a target- such as the medkit, adrenal pen, healing nanites, etc.
        self.is_combat_abil_only_boolean = False #For abilities only; determines whether or not an ability is displayed on our list in the main game state.
        self.abil_passes_turn_boolean = False #And when I say 'passes turn', I mean the advance_cur_combat_char is immediately called after using it.

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

        self.ability_point_cost = 0
        self.ability_cost_str = ""
        self.non_attack_ability_boolean = False #Torvald's shield, cooper's buffs, Avia's summons, etc.
        self.abil_targets_enemies_boolean = True #If this == False, then we move to USE_ITEM game state.

        self.burn_chance = 0
        self.poison_chance = 0
        self.bleed_chance = 0
        self.stun_chance = 0
        self.compromised_chance = 0
        self.infection_chance = 0
        self.suppress_chance = 0

        self.always_checks_status_effect_boolean = False

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
            self.bleed_chance = 25
            self.item_desc = "Your standard issue military grade shotgun most commonly used by security personnel."
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_REVOLVER:
            self.dmg_min = 1
            self.dmg_max = 4
            self.max_range = 2
            self.item_name = "SEMI-AUTOMATIC PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.bleed_chance = 10
        elif self.item_enum == ENUM_ITEM_LASER_PISTOL:
            self.dmg_min = 2
            self.dmg_max = 5
            self.requires_ammo_boolean = False
            self.item_name = "PULSE PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 3
            self.item_verb = "fires the"
            self.item_dmg_str = "burned"
            self.can_overwatch_boolean = True
            self.burn_chance = 10
        elif self.item_enum == ENUM_ITEM_GRENADE:
            self.dmg_min = 8
            self.dmg_max = 12
            self.item_name = "FRAGMENTATION GRENADE"
            self.single_use_boolean = True
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.max_range = 2
            self.item_verb = "tosses the"
            self.item_dmg_str = "shredded"
            self.aoe_count = 6
            self.burn_chance = 25
            self.bleed_chance = 25
        elif self.item_enum == ENUM_ITEM_FLAME_THROWER:
            self.dmg_min = 3
            self.dmg_max = 6
            self.item_name = "FLAMETHROWER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 0
            self.item_verb = "spews fire with the"
            self.item_dmg_str = "burned"
            self.aoe_count = -1
            self.burn_chance = 75
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_HAND_FLAMER: #Torvald ability
            self.dmg_min = 2
            self.dmg_max = 5
            self.item_name = "PALM FLAMER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 1
            self.item_verb = "spews fire with the"
            self.item_dmg_str = "burned"
            self.aoe_count = -1
            self.burn_chance = 75
            self.always_checks_status_effect_boolean = True
            self.ability_point_cost = 3
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP"
            self.is_combat_abil_only_boolean = True
            self.requires_ammo_boolean = False

        elif self.item_enum == ENUM_ITEM_WRIST_ROCKETS: #Torvald ability
            self.dmg_min = 8
            self.dmg_max = 12
            self.item_name = "WRIST ROCKETS"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires"
            self.item_dmg_str = "shredded"
            self.aoe_count = 6
            self.burn_chance = 25
            self.bleed_chance = 25
            self.suppress_chance = 50
            self.stun_chance = 25
            self.always_checks_status_effect_boolean = True
            self.ability_point_cost = 5
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP"
            self.is_combat_abil_only_boolean = True
            self.requires_ammo_boolean = False

        elif self.item_enum == ENUM_ITEM_SHOCKING_GRASP: #Torvald ability
            self.dmg_min = 2
            self.dmg_max = 4
            self.item_name = "SHOCKING GRASP"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 0
            self.item_verb = "grabs with a"
            self.item_dmg_str = "burned"
            self.aoe_count = 1
            self.burn_chance = 10
            self.stun_chance = 75
            self.always_checks_status_effect_boolean = True
            self.ability_point_cost = 2
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP"
            self.is_combat_abil_only_boolean = True
            self.requires_ammo_boolean = False

        #This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_PERSONAL_SHIELD_GENERATOR: #Torvald ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "PERSONAL SHIELD GENERATOR"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY] #Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"This ability does not stack. Spend {self.ability_point_cost} AP to gain the following for 3 turns:"
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = ENUM_PERSONAL_SHIELD_BONUS
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = ENUM_PERSONAL_SHIELD_BONUS
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = False
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_HOLD_THE_LINE:  # Cooper ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "SMOKE GRENADE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"This ability does not stack. Spend {self.ability_point_cost} AP and pass your turn: every friendly unit in your party gains the following for next 3 turns:"
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 2
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_FIELD_MEDICINE:  # Doctor ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "FIELD MEDICINE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: target player character heals 5 hit points and is cleared of the following status effects: burning, bleeding, poisoned."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = False #This abil requires a target, so we don't use the execute_non_attack_ability() script, we use the item_id.use_item() script after targeting a pc
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False
            self.use_requires_target_boolean = True  # Brings us to the USE_ITEM game state if this ability is used from the combat game state CHOOSE_ATTACK

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_SPAWN_LIGHT_SENTRY_GUN:  # Engineer ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "LIGHT SENTRY GUN"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 4
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: spawn a LIGHT SENTRY GUN at your position. Sentry guns do not move, fire at enemies within their range, and set overwatch when enemies are beyond their range."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_SPAWN_LIGHT_SENTINEL_DROID:  # Engineer ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "WHIPSTITCH SENTINEL DROID"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 6
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: spawn a WHIPSTITCH SENTINEL DROID at your position. This hastily constructed bag of bolts uses a PULSE PISTOL and likes to set overwatch, but only if it has the ranged advantage over the enemy."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_SPAWN_LIGHT_SHOTGUN_DROID:  # Engineer ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "SPINNING SCATTERSHOT DROID"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 4
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: spawn a SPINNING SCATTERSHOT DROID at your position. This cowardly little droid likes to pepper enemies with its SHOTGUN."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_SPAWN_LIGHT_FLAMER_DROID:  # Engineer ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "FUMIGATING FLAMER DROID"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: spawn a FUMIGATING FLAMER DROID at your position. This fearless little droid would wheel itself through the gates of hell to protect you. It has been affixed with a FLAMETHROWER and is belching an unhealthy amount of smoke."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_SPAWN_BUZZSAW_DROID:  # Engineer ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "JITTERING BUZZSAW DROID"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP and pass your turn: spawn a JITTERING BUZZSAW DROID at your position. Its spinning BUZZSAW looks as though its about to bounce out of its frame! Better point this droid in the right direction..."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_ENERGIZING_STIM_PRICK:  # Avia ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "ENERGIZING STIMULANT"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP: target player character gains 2 ability points."
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = False #This abil requires a target, so we don't use the execute_non_attack_ability() script, we use the item_id.use_item() script after targeting a pc
            self.abil_passes_turn_boolean = False
            self.requires_ammo_boolean = False
            self.use_requires_target_boolean = True  # Brings us to the USE_ITEM game state if this ability is used from the combat game state CHOOSE_ATTACK

        # This skill uses utils execute_non_attack_ability()
        elif self.item_enum == ENUM_ITEM_HOLD_THE_LINE:  # Cooper ability
            self.dmg_min = 0
            self.dmg_max = 0
            self.item_name = "'HOLD THE LINE'"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_BODY]  # Indicates either hand can equip
            self.max_range = 0
            self.ability_point_cost = 3
            self.ability_cost_str = f"*This ability does not stack.* Spend {self.ability_point_cost} AP and pass your turn: every friendly unit in your party gains the following for the next 3 turns:"
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 2
            self.is_combat_abil_only_boolean = True
            self.non_attack_ability_boolean = True
            self.abil_passes_turn_boolean = True
            self.requires_ammo_boolean = False
        elif self.item_enum == ENUM_ITEM_ROCKET_LAUNCHER:
            self.dmg_min = 10
            self.dmg_max = 15
            self.single_use_boolean = True
            self.item_name = "ROCKET LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "exploded"
            self.aoe_count = 8
            self.bleed_chance = 75
            self.burn_chance = 75 #DEBUG
        elif self.item_enum == ENUM_ITEM_LEAD_PIPE:
            self.dmg_min = 1
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "LEAD PIPE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "blundgeoned"
            self.max_range = 0
            self.stun_chance = 50
        elif self.item_enum == ENUM_ITEM_MONSTROUS_CLAW:
            self.dmg_min = 4
            self.dmg_max = 8
            self.requires_ammo_boolean = False
            self.item_name = "MONSTROUS CLAWS"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swipes with"
            self.item_dmg_str = "slashed"
            self.max_range = 0
            self.bleed_chance = 50
            self.infection_chance = 10
        elif self.item_enum == ENUM_ITEM_LARVA_WRITHING_TENDRIL:
            self.dmg_min = 1
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "WRITHING TENDRIL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "whips with a"
            self.item_dmg_str = "slashed"
            self.max_range = 0
            self.stun_chance = 25
            self.bleed_chance = 0
            self.always_checks_status_effect_boolean = True
            self.infection_chance = 10
        elif self.item_enum == ENUM_ITEM_DESPERATE_CLAW:
            self.dmg_min = 1
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "DESPERATE CLAW"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH, ENUM_EQUIP_SLOT_LH]  # Indicates either hand can equip
            self.item_verb = "slashes with a"
            self.item_dmg_str = "slashed"
            self.max_range = 0
            self.bleed_chance = 25
            self.infection_chance = 10
        elif self.item_enum == ENUM_ITEM_LARVA_INJECTION_BARB:
            self.dmg_min = 4
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "INFECTED BARB"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "stabs with a"
            self.item_dmg_str = "punctured"
            self.max_range = 0
            self.infection_chance = 100
        elif self.item_enum == ENUM_ITEM_POLICE_TRUNCHEON:
            self.dmg_min = 3
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "POLICE TRUNCHEON"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "blundgeoned"
            self.max_range = 0
            self.stun_chance = 25
        elif self.item_enum == ENUM_ITEM_STUN_BATON: #Has a 100% chance of stunning enemies, minus their electric_res
            self.dmg_min = 1
            self.dmg_max = 2
            self.requires_ammo_boolean = False
            self.item_name = "STUN BATON"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "thrusts the"
            self.item_dmg_str = "zapped"
            self.max_range = 0
            self.stun_chance = 100
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_FIRE_AXE:
            self.dmg_min = 2
            self.dmg_max = 5
            self.requires_ammo_boolean = False
            self.item_name = "FIRE AXE"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "swings the"
            self.item_dmg_str = "mauled"
            self.max_range = 0
            self.bleed_chance = 25
        elif self.item_enum == ENUM_ITEM_CRUDE_BUZZSAW:
            self.dmg_min = 5
            self.dmg_max = 8
            self.requires_ammo_boolean = False
            self.item_name = "CRUDE BUZZSAW"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "spins the"
            self.item_dmg_str = "eviscerated"
            self.max_range = 0
            self.bleed_chance = 75
        elif self.item_enum == ENUM_ITEM_TASER: #High stun chance, extra damage to characters with weak electric_res
            self.dmg_min = 1
            self.dmg_max = 1
            self.requires_ammo_boolean = False
            self.item_name = "TASER"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "fires the"
            self.item_dmg_str = "zapped"
            self.max_range = 1
            self.stun_chance = 100
            self.always_checks_status_effect_boolean = True
            self.ability_point_cost = 2
            self.ability_cost_str = f"Spend {self.ability_point_cost} AP"
            self.is_combat_abil_only_boolean = True
            self.requires_ammo_boolean = False
        elif self.item_enum == ENUM_ITEM_ASSAULT_RIFLE:
            self.dmg_min = 4
            self.dmg_max = 6
            self.item_name = "ASSAULT RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.bleed_chance = 25
            self.can_overwatch_boolean = True
        elif self.item_enum == ENUM_ITEM_LIGHT_MG: #Light sentry gun weapon.
            self.dmg_min = 3
            self.dmg_max = 6
            self.item_name = "LIGHT MACHINE GUN"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.bleed_chance = 25
            self.suppress_chance = 33
        elif self.item_enum == ENUM_ITEM_SPINE_PROJECTILE:
            self.dmg_min = 3
            self.dmg_max = 6
            self.item_name = "SHOOTING SPINE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires a"
            self.item_dmg_str = "shot"
            self.bleed_chance = 25
            self.infection_chance = 10
            self.poison_chance = 25
        elif self.item_enum == ENUM_ITEM_SPINE_PROJECTILE_VENOMOUS:
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "VENOMOUS SPINE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires a"
            self.item_dmg_str = "shot"
        elif self.item_enum == ENUM_ITEM_ACID_SPIT:
            self.dmg_min = 4
            self.dmg_max = 8
            self.item_name = "ACID BILE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "spits with"
            self.item_dmg_str = "melted"
            self.aoe_count = 3
            self.can_overwatch_boolean = True
            self.poison_chance = 75
            self.infection_chance = 10
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_ACID_CLOUD:
            self.dmg_min = 1
            self.dmg_max = 3
            self.item_name = "ACID CLOUD"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "belches a massive"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
            self.poison_chance = 75
            self.bleed_chance = 20
            self.infection_chance = 10
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_STICKY_SLIME:
            self.dmg_min = 0
            self.dmg_max = 1
            self.item_name = "STICKY SLIME"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 5
            self.item_verb = "sprays"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
            self.suppress_chance = 75
            self.always_checks_status_effect_boolean = True
            self.infection_chance = 10
        elif self.item_enum == ENUM_ITEM_FILAMENT_SPRAY:
            self.dmg_min = 0
            self.dmg_max = 1
            self.item_name = "FILAMENT SPRAY"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 5
            self.item_verb = "spits a massive"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
            self.infection_chance = 10
            self.poison_chance = 10
            self.stun_chance = 20
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_TOXIC_GRENADE_LAUNCHER:
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "TOXIC GRENADE LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4 #Debug value
            self.item_verb = "fires the"
            self.item_dmg_str = "burned"
            self.aoe_count = -1
            self.poison_chance = 75
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_FRAG_GRENADE_LAUNCHER:
            self.dmg_min = 5
            self.dmg_max = 10
            self.item_name = "FRAGMENTAION GRENADE LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 5 #Debug value
            self.item_verb = "fires the"
            self.item_dmg_str = "shredded"
            self.aoe_count = 4
            self.burn_chance = 25
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_CONCUSSION_GRENADE_LAUNCHER:
            self.dmg_min = 0
            self.dmg_max = 1
            self.item_name = "CONCUSSION GRENADE LAUNCHER"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "concussed"
            self.aoe_count = -1
            self.stun_chance = 75
            self.suppress_chance = 75
            self.always_checks_status_effect_boolean = True
        elif self.item_enum == ENUM_ITEM_ACID_SACK: #Acts as a proximity mine
            self.dmg_min = 1
            self.dmg_max = 4
            self.item_name = "ACID SACK"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 2
            self.item_verb = "drops a"
            self.item_dmg_str = "melted"
            self.aoe_count = -1
            self.infection_chance = 10
        elif self.item_enum == ENUM_ITEM_SUB_MACHINE_GUN:
            self.dmg_min = 3
            self.dmg_max = 5
            self.item_name = "SUB MACHINE GUN"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 3
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.aoe_count = 4
            self.bleed_chance = 25
            self.suppress_chance = 50
        elif self.item_enum == ENUM_ITEM_MACHINE_PISTOL:
            self.dmg_min = 2
            self.dmg_max = 4
            self.item_name = "MACHINE PISTOL"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.max_range = 2
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.aoe_count = 3
            self.bleed_chance = 25
            self.suppress_chance = 25
        elif self.item_enum == ENUM_ITEM_SNIPER_RIFLE:
            self.dmg_min = 8
            self.dmg_max = 12
            self.melee_debuff_boolean = True
            self.item_name = "SNIPER RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 5
            self.item_verb = "fires the"
            self.item_dmg_str = "shot"
            self.can_overwatch_boolean = True
            self.bleed_chance = 50
        elif self.item_enum == ENUM_ITEM_LASER_RIFLE:
            self.dmg_min = 6
            self.dmg_max = 9
            self.requires_ammo_boolean = False
            self.melee_debuff_boolean = True
            self.item_name = "PULSE RIFLE"
            self.equip_slot_list = [[ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH]] #Indicates two-handed weapon
            self.max_range = 4
            self.item_verb = "fires the"
            self.item_dmg_str = "burned"
            self.can_overwatch_boolean = True
            self.burn_chance = 25
        elif self.item_enum == ENUM_ITEM_MEDKIT:
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "MEDICAL KIT"
            self.equippable_boolean = False
            self.combat_usable_boolean = True
        elif self.item_enum == ENUM_ITEM_HEALING_NANITE_INJECTOR:
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "PEN OF REGENERATION NANITES"
            self.equippable_boolean = False
            self.combat_usable_boolean = True
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
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 2
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = 0
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
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ARMOR] = 4
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_ELECTRIC_RES] = 100
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_EVASION] = -2
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_VACUUM_RES] = 50
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_GAS_RES] = 100
            self.stat_boost_list[ENUM_ITEM_STAT_BOOST_FIRE_RES] = 100
            self.changes_stats_boolean = True
        elif self.item_enum == ENUM_ITEM_ADRENAL_PEN:
            self.single_use_boolean = True
            self.usable_boolean = True
            self.item_name = "ADRENAL PEN"
            self.equippable_boolean = False
            self.combat_usable_boolean = True
        elif self.item_enum == ENUM_ITEM_DNA_TESTER:
            self.single_use_boolean = False
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
            self.stun_chance = 25

        elif self.item_enum == ENUM_ITEM_PLASMA_TORCH:
            self.dmg_min = 1
            self.dmg_max = 4
            self.requires_ammo_boolean = False
            self.item_name = "PLASMA TORCH"
            self.equip_slot_list = [ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH] #Indicates either hand can equip
            self.item_verb = "blazes the"
            self.item_dmg_str = "burns"
            self.max_range = 0
            self.burn_chance = 75

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

        #Build this item's 'status_effect_list':
        self.status_effect_list = []
        for i in range(0,ENUM_STATUS_EFFECT_TOTAL_EFFECTS):
            if i == ENUM_STATUS_EFFECT_FIRE:
                self.status_effect_list.append(self.burn_chance)
            elif i == ENUM_STATUS_EFFECT_INFECT:
                self.status_effect_list.append(self.infection_chance)
            elif i == ENUM_STATUS_EFFECT_POISON:
                self.status_effect_list.append(self.poison_chance)
            elif i == ENUM_STATUS_EFFECT_BLEED:
                self.status_effect_list.append(self.bleed_chance)
            elif i == ENUM_STATUS_EFFECT_STUN:
                self.status_effect_list.append(self.stun_chance)
            elif i == ENUM_STATUS_EFFECT_SUPPRESSED:
                self.status_effect_list.append(self.suppress_chance)

    def print_item_desc(self):
        #print(f"print_item_desc method called for item with name: {self.item_name}")
        wrapped_item_desc_str = textwrap.fill(self.item_desc, TOTAL_LINE_W)
        print(wrapped_item_desc_str)
        print("")

    #target_char_id: the char_id that we're 'u'sing the item on:
    def use_item(self,target_char_id):

        #Medkit or field medicine - they fucntion the same
        if self.item_enum == ENUM_ITEM_MEDKIT or self.item_enum == ENUM_ITEM_FIELD_MEDICINE:
            target_char_id.hp_cur += 5
            #cap:
            if target_char_id.hp_cur > target_char_id.hp_max:
                target_char_id.hp_cur = target_char_id.hp_max
            #Remove applicable debuffs:
            target_char_id.burning_count = 0
            target_char_id.poisoned_count = 0
            target_char_id.bleeding_count = 0
            #Print result:
            result_str = f"{target_char_id.name} has been healed for 5 hit points. They have also been cleared of the burning, poisoned, and bleeding status effects."
            wrapped_message = textwrap.fill(result_str, width=TOTAL_LINE_W)
            print(wrapped_message)
            print("")
            #If target was unconscious - 'wake' them up:
            if target_char_id.unconscious_boolean == True and target_char_id.hp_cur > 0:
                target_char_id.unconscious_boolean = False
                print(f"{target_char_id.name} has woken up!\n")

        elif self.item_enum == ENUM_ITEM_HEALING_NANITE_INJECTOR:
            target_char_id.healing_nanites_count += 3
            result_str = textwrap.fill(f"{target_char_id.name} has been injected with regeneration nanites. They will rapidly heal tissue damage for the next 3 turns.\n",TOTAL_LINE_W)
            print(result_str)
            print("")

        elif self.item_enum == ENUM_ITEM_ADRENAL_PEN:
            target_char_id.adrenal_pen_count += 3
            result_str = textwrap.fill(f"{target_char_id.name} has been injected with adrenaline. They will receive +2 accuracy and +2 speed for the next 3 turns.\n",TOTAL_LINE_W)
            print(result_str)
            print("")

        elif self.item_enum == ENUM_ITEM_ENERGIZING_STIM_PRICK:
            target_char_id.ability_points_cur += ENUM_STIM_PRICK_AP_BOOST
            if target_char_id.ability_points_cur > target_char_id.ability_points_max:
                target_char_id.ability_points_cur = target_char_id.ability_points_max
            result_str = textwrap.fill(f"{target_char_id.name} has been injected with the ENERGIZING STIM. They feel revitalized! (+2 Ability points)\n",TOTAL_LINE_W)
            print(result_str)
            print("")





