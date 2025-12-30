
from constants import *
from models.item import Item
from models.room import Room

import random
import textwrap

class Character:

    # region Constructor event for character stats:
    def __init__(self, char_type_enum, spawn_grid_x, spawn_grid_y, spawn_grid, char_team_enum,add_to_room_list_boolean,wep_loadout_int = 0):

        self.add_to_room_list_boolean = add_to_room_list_boolean

        self.wep_loadout_int = wep_loadout_int #Only a debug var used for certain enemies to change their wep loadout, for debug purposes

        # Default values for instance vars for this particularly character:
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.dexterity = 0
        self.accuracy = ENUM_AVERAGE_ACCURACY_SCORE
        self.stealth = 0 #When you consider that rooms add or subtract to this value based upon their cover amount, the average here can be lower than 7
        self.speed = 0 #9 is current max, so a char with with 9 base speed would have to roll a 0, and a character with a base speed of 0 would have to roll a 9 to beat them.

        self.ran_init_val = 0 #A random value assigned that helps determine when characters act in combat

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
        self.evasion = ENUM_AVERAGE_EVASION_SCORE
        self.res_fire = 0
        self.res_vacuum = 0
        self.res_gas = 0
        self.res_electric = 0
        self.res_poison = 0
        self.res_bleed = 0
        self.res_stun = 0
        self.res_infect = 0
        self.res_compromised = 0
        self.res_suppress = 0

        self.suppress_immune_boolean = False
        self.stun_immune_boolean = False

        self.cur_action_points = 2
        self.max_action_points = 2

        self.accuracy_debuff = 0 #Used in conjunction with return_accuracy_debuff to determine accuracy debuff for characters in combat

        self.inv_list = []
        self.ability_list = -1

        self.char_team_enum = char_team_enum

        self.name = "Not defined"
        self.subjective_pronoun = "he"
        self.possessive_pronoun = "his"

        self.starting_combat_rank = ENUM_RANK_PC_MIDDLE
        self.cur_combat_rank = 0
        self.participated_in_new_turn_battle = False
        self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD
        self.chosen_weapon = -1
        self.targeted_rank = -1
        self.ai_inferior_alternate_wep = -1

        self.enemy_ai_move_boolean = False
        self.enemy_ai_fight_boolean = False

        self.ai_is_suppressor_boolean = False #Just a sub-set of the ENUM_AI_COMBAT_RANGED_COWARD, this enemy chooses an item with suppression instead, and resorts to a weaker melee weapon when pcs finally close with it in melee; otherwise it behaves exactly the same as Spined Spitters.

        self.dist_to_enemy = 0 #Used for enemy ai

        # Initialize inv_list and nested ENUM_EQUIP_BACKLIST_LIST:
        for i in range(0 ,ENUM_EQUIP_SLOT_TOTAL_SLOTS):
            self.inv_list.append(-1)

        self.char_type_enum = char_type_enum
        self.cur_grid = spawn_grid
        self.cur_room_id = spawn_grid[spawn_grid_y][spawn_grid_x]
        self.cur_grid_x = spawn_grid_x
        self.cur_grid_y = spawn_grid_y

        self.dodge_bonus_boolean = False

        self.randomly_chosen_move_dir = random.choice([-1,1])
        self.overwatch_rank = -1
        self.will_overwatch_boolean = False

        self.infection_count = 0
        self.burning_count = 0
        self.poisoned_count = 0
        self.bleeding_count = 0
        self.unconscious_count = 0
        self.inside_toxic_gas_boolean = False
        self.inside_vacuum_boolean = False
        self.healing_nanites_count = 0
        self.suppressed_count = 0
        self.stun_count = 0
        self.spawn_minion_count = 0

        self.resolve_dot_effects_boolean = True
        self.healing_passive_boolean = False
        self.unconscious_boolean = False
        self.completely_dead_boolean = False

        self.healing_factor_boolean = False
        self.healing_factor_cd = 0

        self.revived_dialogue_str_list = -1

        #region Define char stats....
        if char_type_enum == ENUM_CHARACTER_OGRE:

            self.name = "Cragos, 'The Ogre'"
            self.hp_max = 16
            self.hp_cur = 16
            self.ability_points_cur = 5
            self.ability_points_max = 5
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 1
            self.security = 9
            self.science = 0
            self.scavenging = 0
            self.stealth = 0

            self.strength = 10
            self.intelligence = 1
            self.wisdom = 2
            self.dexterity = 0
            self.speed = -1

            self.armor = 1
            self.healing_factor_boolean = True
            self.revived_dialogue_str_list = [
                f"*{self.name} dusts himself off, grumbling: 'How do you kill a dead man?'*",
                f"*'Shit,' {self.name} mumbles. 'Must've died again.'",
                f"{self.name} clambers to his feet, spitting a gob of blood from his mouth. It's congealed before it hits the ground. 'Now you've really pissed me off.'",
                f"'I've still got a few debts left to pay,' {self.name} grumbles. He grins maliciously, cracking his knuckles. 'And a few skulls left to split...'"
            ]

            self.starting_combat_rank = ENUM_RANK_PC_FAR #debug only

            self.accuracy = ENUM_AVERAGE_ACCURACY_SCORE-1 #Worse than average accuracy, only hits about 50% of the time, on average
            self.evasion = ENUM_AVERAGE_EVASION_SCORE-1 #Worse than average evasion

            # Starting equipment:
            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip, -1, True)
            item_to_equip = Item(ENUM_ITEM_ASSAULT_RIFLE)
            self.add_item_to_backpack(item_to_equip, True)
            #item_to_equip = Item(ENUM_ITEM_CONCUSSION_GRENADE_LAUNCHER)
            #self.equip_item(item_to_equip, -1, True)
            item_to_equip = Item(ENUM_ITEM_MACHINE_PISTOL)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_SHOTGUN)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_POLICE_TRUNCHEON)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_RIOT_SHIELD)
            self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_BIOLOGIST:
            self.name = "Chavrita, 'The Biologist'"
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
            self.stealth = 5

            self.strength = 0
            self.intelligence = 8
            self.wisdom = 6
            self.dexterity = 2
            self.speed = 2

            self.subjective_pronoun = "she"
            self.possessive_pronoun = "her"

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_MEDICAL_SCRUBS)
            self.equip_item(item_to_equip, -1,True)
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
            self.stealth = 5

            self.strength = 2
            self.intelligence = 6
            self.wisdom = 6
            self.dexterity = 1
            self.speed = 3

            # Starting equipment
            # item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
            # self.equip_item(item_to_equip, item_to_equip.equip_slot_enum,True)
            item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
            self.equip_item(item_to_equip, -1, True)

        elif char_type_enum == ENUM_CHARACTER_JANITOR:
            self.name = "Johns, 'The Janitor'"
            self.hp_max = 7
            self.hp_cur = 7
            self.ability_points_cur = 5
            self.ability_points_max = 5
            self.sanity_cur = 6
            self.sanity_max = 6

            self.engineering = 2
            self.security = 2
            self.science = 2
            self.scavenging = 5
            self.stealth = 7

            self.strength = 2
            self.intelligence = 4
            self.wisdom = 4
            self.dexterity = 2
            self.speed = 4

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_ENGINEER_GARB)
            self.equip_item(item_to_equip, -1,True)

        elif char_type_enum == ENUM_CHARACTER_MECH_MAGICIAN:
            self.name = "Avia, 'The Mechanician'"
            self.hp_max = 5
            self.hp_cur = 5
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 7
            self.security = 1
            self.science = 2
            self.scavenging = 1
            self.stealth = 5

            self.strength = 1
            self.intelligence = 7
            self.wisdom = 7
            self.dexterity = 3
            self.speed = 5

            self.res_fire = 50
            self.res_vacuum = 50
            self.res_gas = 50
            self.res_electric = -50

            self.subjective_pronoun = "she"
            self.possessive_pronoun = "her"

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip, -1,True)

        elif char_type_enum == ENUM_CHARACTER_MERCENARY_MECH:
            self.name = "Torvald, 'The Cyborg'"
            self.hp_max = 12
            self.hp_cur = 12
            self.ability_points_cur = 8
            self.ability_points_max = 8
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 3
            self.security = 8
            self.science = 1
            self.scavenging = 1
            self.stealth = 4

            self.strength = 8
            self.intelligence = 3
            self.wisdom = 3
            self.dexterity = 3
            self.speed = 4

            self.armor = 1

            self.res_fire = 50
            self.res_vacuum = 50
            self.res_gas = 50
            self.res_electric = -50

            #debug only:
            self.starting_combat_rank = ENUM_RANK_PC_FAR  # debug only

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.add_item_to_backpack(item_to_equip, True)
            #item_to_equip = Item(ENUM_ITEM_CONCUSSION_GRENADE_LAUNCHER)
            #self.equip_item(item_to_equip, -1,True)
            #item_to_equip = Item(ENUM_ITEM_TOXIC_GRENADE_LAUNCHER)
            #self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_LASER_PISTOL)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_REVOLVER)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_SUIT_MARINE)
            self.equip_item(item_to_equip, -1,True)
            item_to_equip = Item(ENUM_ITEM_ASSAULT_RIFLE)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_FLAME_THROWER)
            self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_SOLDIER:
            self.name = "Cooper, 'The Security Guard'"
            self.hp_max = 10
            self.hp_cur = 10
            self.ability_points_cur = 14
            self.ability_points_max = 14
            self.sanity_cur = 8
            self.sanity_max = 8

            self.engineering = 1
            self.security = 7
            self.science = 0
            self.scavenging = 2
            self.stealth = 3

            self.strength = 7
            self.intelligence = 1
            self.wisdom = 2
            self.dexterity = 2
            self.speed = 2

            self.starting_combat_rank = ENUM_RANK_PC_FAR  # debug only

            # Starting equipment
            item_to_equip = Item(ENUM_ITEM_TARGETING_HUD)
            self.equip_item(item_to_equip, -1, True)
            item_to_equip = Item(ENUM_ITEM_FLAK_ARMOR)
            self.equip_item(item_to_equip, -1,True)
            item_to_equip = Item(ENUM_ITEM_RIOT_SHIELD)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_MACHINE_PISTOL)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_FIRE_AXE)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_ASSAULT_RIFLE)
            self.equip_item(item_to_equip, -1, True)
            item_to_equip = Item(ENUM_ITEM_REVOLVER)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_STUN_BATON)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_FLASHLIGHT)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_ADRENAL_PEN)
            self.add_item_to_backpack(item_to_equip ,True)
            item_to_equip = Item(ENUM_ITEM_POLICE_TRUNCHEON)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_GRENADES)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_TASER)
            self.add_item_to_backpack(item_to_equip, True)
            item_to_equip = Item(ENUM_ITEM_SECURITY_VEST)
            self.add_item_to_backpack(item_to_equip, True)
            #item_to_equip = Item(ENUM_ITEM_CONCUSSION_GRENADE_LAUNCHER)
            #self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_SCIENTIST:
            self.name = "Darius, 'The Physicist'"
            self.hp_max = 5
            self.hp_cur = 5
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 6
            self.sanity_max = 6

            self.engineering = 2
            self.security = 0
            self.science = 9
            self.scavenging = 1
            self.stealth = 4

            self.strength = 0
            self.intelligence = 9
            self.wisdom = 9
            self.dexterity = 2
            self.speed = 3

            item_to_equip = Item(ENUM_ITEM_SCIENTIST_LABCOAT)
            self.equip_item(item_to_equip ,-1,True)

        elif char_type_enum == ENUM_CHARACTER_CRIMINAL:
            self.name = "Emeran, 'The Criminal'"
            self.hp_max = 9
            self.hp_cur = 9
            self.ability_points_cur = 12
            self.ability_points_max = 12
            self.sanity_cur = 9
            self.sanity_max = 9

            self.engineering = 2
            self.security = 6
            self.science = 2
            self.scavenging = 4
            self.stealth = 8
            self.speed = 2

            self.strength = 4
            self.intelligence = 0
            self.wisdom = 0
            self.dexterity = 4
            self.speed = 7

            self.evasion = ENUM_AVERAGE_EVASION_SCORE + 1  # Better than average at evading

            item_to_equip = Item(ENUM_ITEM_PRISONER_JUMPSUIT)
            self.equip_item(item_to_equip ,-1,True)

        elif char_type_enum == ENUM_CHARACTER_SERVICE_DROID:
            self.name = "RG-88, 'Service Droid'"
            self.hp_max = 14
            self.hp_cur = 14
            self.ability_points_cur = 15
            self.ability_points_max = 15
            self.sanity_cur = 10
            self.sanity_max = 10

            self.engineering = 6
            self.security = 6
            self.science = 6
            self.scavenging = 0
            self.stealth = 4

            self.strength = 9
            self.intelligence = 4
            self.wisdom = 8
            self.dexterity = 2
            self.speed = 5

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

            self.engineering = 3
            self.security = 0
            self.science = 3
            self.scavenging = 3
            self.stealth = 6

            self.strength = 1
            self.intelligence = 3
            self.wisdom = 4
            self.dexterity = 2
            self.speed = 4

            item_to_equip = Item(ENUM_ITEM_OFFICER_JUMPSUIT)
            self.equip_item(item_to_equip ,-1,True)

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
            self.stealth = 10

            self.strength = 0
            self.intelligence = 2
            self.wisdom = 1
            self.dexterity = 7
            self.speed = 8

            self.evasion = ENUM_AVERAGE_EVASION_SCORE+1 #Better than average at evading

            self.subjective_pronoun = "she"
            self.possessive_pronoun = "her"

            item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
            self.equip_item(item_to_equip ,-1,True)
            item_to_equip = Item(ENUM_ITEM_KIRAS_NOISY_GAME)
            self.add_item_to_backpack(item_to_equip, True)

        elif char_type_enum == ENUM_CHARACTER_PLAYBOY:
            self.name = "Oberon, 'The Playboy'"
            self.hp_max = 8
            self.hp_cur = 8
            self.ability_points_cur = 6
            self.ability_points_max = 6
            self.sanity_cur = 3
            self.sanity_max = 3

            self.engineering = 1
            self.security = 1
            self.science = 1
            self.scavenging = 3
            self.stealth = 6

            self.strength = 3
            self.intelligence = 2
            self.wisdom = 1
            self.dexterity = 5
            self.speed = 6

            item_to_equip = Item(ENUM_ITEM_CIVILIAN_JUMPSUIT)
            self.equip_item(item_to_equip ,-1,True)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_INFECTED_SCIENTIST:
            self.name = "Gregos, 'The Researcher'"
            self.hp_max = 8
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 2
            self.sanity_max = 2

            self.engineering = 4
            self.security = 0
            self.science = 9
            self.scavenging = 1
            self.stealth = 4

            self.strength = 2
            self.intelligence = 8
            self.wisdom = 8
            self.dexterity = 2
            self.speed = 2

            self.starting_combat_rank = ENUM_RANK_PC_FAR
            self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD

            # Starting equipment
            self.add_ability(ENUM_ITEM_REVOLVER)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_SKITTERING_LARVA:
            self.name = "Skittering Larva"
            self.hp_max = random.randint(3,4)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20
            self.speed = 8

            self.combat_ai_preference = ENUM_AI_COMBAT_MELEE

            self.armor = 0
            self.evasion = 3
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0
            #debug:
            self.starting_combat_rank = ENUM_RANK_ENEMY_FAR
            #abilities
            self.add_ability(ENUM_ITEM_LARVA_INJECTION_BARB)
            self.add_ability(ENUM_ITEM_LARVA_WRITHING_TENDRIL)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_JITTERING_BUZZSAW:
            self.name = "Jittering Buzzsaw Droid"
            self.hp_max = random.randint(3,5)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20
            self.speed = 4

            self.combat_ai_preference = ENUM_AI_COMBAT_MELEE

            self.armor = 0
            self.evasion = 1
            self.res_fire = 50
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = -100
            #debug:
            self.starting_combat_rank = ENUM_RANK_PC_FAR
            #abilities
            self.add_ability(ENUM_ITEM_CRUDE_BUZZSAW)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_FUMIGATING_FLAMER:
            self.name = "Fumigating Flamer Droid"
            self.hp_max = random.randint(6,8)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20
            self.speed = 1

            self.combat_ai_preference = ENUM_AI_COMBAT_MELEE

            self.armor = 0
            self.evasion = 0
            self.res_fire = 50
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = -100
            #debug:
            self.starting_combat_rank = ENUM_RANK_PC_FAR
            #abilities
            self.add_ability(ENUM_ITEM_FLAME_THROWER)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_SPINNING_SCATTERSHOT:
            self.name = "Spinning Scattershot Droid"
            self.hp_max = random.randint(5,7)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20
            self.speed = 4

            self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD

            self.armor = 0
            self.evasion = 1
            self.res_fire = 50
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = -100
            #debug:
            self.starting_combat_rank = ENUM_RANK_PC_FAR
            #abilities
            self.add_ability(ENUM_ITEM_SHOTGUN)

        elif char_type_enum == ENUM_CHARACTER_NEUTRAL_WHIPSTICH_SENTINEL:
            self.name = "Whipstich Sentinel Droid"
            self.hp_max = random.randint(7,9)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20
            self.speed = 4

            self.combat_ai_preference = ENUM_AI_COMBAT_OVERWATCH

            self.armor = 0
            self.evasion = 1
            self.res_fire = 50
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = -100
            #debug:
            self.starting_combat_rank = ENUM_RANK_PC_FAR
            #abilities
            self.add_ability(ENUM_ITEM_LASER_PISTOL)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_LUMBERING_MAULER:
            self.name = "Lumbering Mauler"
            self.hp_max = random.randint(14,18)
            self.hp_cur = self.hp_max
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

            self.suppress_immune_boolean = True
            self.stun_immune_boolean = True
            self.can_spawn_minions = True
            self.spawn_minion_count = random.randint(1,3)

            self.combat_ai_preference = ENUM_AI_COMBAT_MELEE

            self.speed = -1
            #debug:
            self.starting_combat_rank = ENUM_RANK_ENEMY_MIDDLE
            # abilities
            self.add_ability(ENUM_ITEM_MONSTROUS_CLAW)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_SPINED_SPITTER:
            self.name = "Spined Spitter"
            self.hp_max = random.randint(9,11)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20

            self.armor = 0
            self.evasion = 1
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0

            self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD

            self.speed = 3

            # abilities
            self.add_ability(ENUM_ITEM_SPINE_PROJECTILE)
            self.add_ability(ENUM_ITEM_DESPERATE_CLAW)
            #self.add_ability(ENUM_ITEM_SPINE_PROJECTILE_VENOMOUS)
            #self.add_ability(ENUM_ITEM_SPINE_PROJECTILE_INFECTED)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SOLDIER:
            self.name = "Transmogrified Soldier"
            self.hp_max = random.randint(9,12)
            self.hp_cur = self.hp_max
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

            self.combat_ai_preference = ENUM_AI_COMBAT_OVERWATCH

            self.speed = 2

            # abilities
            self.add_ability(ENUM_ITEM_MONSTROUS_CLAW)

            if wep_loadout_int <= 0:
                self.add_ability(ENUM_ITEM_LASER_RIFLE)
                self.add_ability(ENUM_ITEM_SECURITY_VEST)
            elif wep_loadout_int == 1:
                ran_abil_enum = random.choice([ENUM_ITEM_ASSAULT_RIFLE,ENUM_ITEM_SUB_MACHINE_GUN])
                self.add_ability(ran_abil_enum)
                self.add_ability(ENUM_ITEM_FLAK_ARMOR)
            elif wep_loadout_int == 2:
                ran_val = random.choice([1,2])
                if ran_val == 1:
                    ran_abil_enum = random.choice([ENUM_ITEM_SHOTGUN,ENUM_ITEM_FLAME_THROWER])
                    self.add_ability(ran_abil_enum)
                else:
                    self.add_ability(ENUM_ITEM_MACHINE_PISTOL)
                    self.add_ability(ENUM_ITEM_RIOT_SHIELD)
                self.add_ability(ENUM_ITEM_SUIT_MARINE)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_SODDEN_SHAMBLER:
            self.name = "Sodden Shambler"
            self.hp_max = random.randint(6,8)
            self.hp_cur = self.hp_max
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

            self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD

            self.speed = 0

            self.add_ability(ENUM_ITEM_ACID_SPIT)
            self.add_ability(ENUM_ITEM_ACID_CLOUD)
            self.add_ability(ENUM_ITEM_DESPERATE_CLAW)

        elif char_type_enum == ENUM_CHARACTER_ENEMY_WEBBED_LURKER:
            self.name = "Chittering Lurker"
            self.hp_max = random.randint(7,9)
            self.hp_cur = self.hp_max
            self.ability_points_cur = 3
            self.ability_points_max = 3
            self.sanity_cur = 20
            self.sanity_max = 20

            self.armor = 0
            self.evasion = 2
            self.res_fire = 0
            self.res_vacuum = 100
            self.res_gas = 100
            self.res_electric = 0

            self.ai_is_suppressor_boolean = True
            self.combat_ai_preference = ENUM_AI_COMBAT_RANGED_COWARD

            self.speed = 10 #debug value for now; it's too damn high.

            # abilities
            self.add_ability(ENUM_ITEM_FILAMENT_SPRAY)
            self.add_ability(ENUM_ITEM_STICKY_SLIME)
            self.add_ability(ENUM_ITEM_DESPERATE_CLAW)

        #endregion for define char stats

        #Call our method add_or_remove_char_from_room_list to add this char to the appropriate room list:
        if self.add_to_room_list_boolean:
            self.add_or_remove_char_from_room_list(self.cur_room_id,True)

        #Build our self.status_res_list:
        self.status_res_list = []
        for i in range(0, ENUM_STATUS_EFFECT_TOTAL_EFFECTS):
            if i == ENUM_STATUS_EFFECT_FIRE:
                self.status_res_list.append(self.res_fire)
            elif i == ENUM_STATUS_EFFECT_INFECT:
                self.status_res_list.append(self.res_infect)
            elif i == ENUM_STATUS_EFFECT_COMPROMISE:
                self.status_res_list.append(self.res_compromised)
            elif i == ENUM_STATUS_EFFECT_POISON:
                self.status_res_list.append(self.res_poison)
            elif i == ENUM_STATUS_EFFECT_BLEED:
                self.status_res_list.append(self.res_bleed)
            elif i == ENUM_STATUS_EFFECT_STUN:
                self.status_res_list.append(self.res_stun)
            elif i == ENUM_STATUS_EFFECT_SUPPRESSED:
                self.status_res_list.append(self.res_suppress)

        #Set our self.starting_combat_rank:
        if self.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
            self.starting_combat_rank = ENUM_RANK_ENEMY_FAR
        else:
            self.starting_combat_rank = ENUM_RANK_PC_FAR

    # endregion

    def update_cur_room_id(self):
        self.cur_room_id = self.cur_grid[self.cur_grid_y][self.cur_grid_x]

    def print_char_inv(self):

        print(f"{self.name} is wearing and carrying the following items:")

        for i in range(0,len(self.inv_list)):

            #Set default as nothing
            intro_str = ""

            if i == ENUM_EQUIP_SLOT_BODY:
                intro_str = f"Wearing on body: "
            elif i == ENUM_EQUIP_SLOT_ACCESSORY:
                intro_str = f"Wearing as accessory: "
            elif i == ENUM_EQUIP_SLOT_RH:
                intro_str = f"Wielding in right hand: "
            elif i == ENUM_EQUIP_SLOT_LH:
                intro_str = f"Wielding in left hand: "

            if i == ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                print("They are carrying on their person:")

            if isinstance(self.inv_list[i], Item):
                intro_str += f"{i}.) {self.inv_list[i].item_name}. "
                if self.inv_list[i].slot_designation_str == "Accessory":
                    equip_slot_str = f"({self.inv_list[i].slot_designation_str})"
                    intro_str += f"{equip_slot_str}"
            else:
                intro_str += f"{i}.) Nothing."

            print(intro_str)

        print("")
        print \
            ("Simply enter the associated number to use, equip, unequip, or swap an item; or enter 'BACK' to leave the inventory screen.")
        print("You can also enter 'L{ITEM NUMBER} to get a description of the corresponding item;")
        print("Or 'G{ITEM NUMBER} to give the corresponding item to another player;")
        print \
            ("Or 'D{ITEM NUMBER} to drop the item back into your current room (you could retrieve it again with 'SCAVENGE').")
        print("Enter your selection now >")

    #Note: most abilities are just items at this point
    def add_ability(self,item_enum):

        suppress_boolean = False
        #These units use pc weapons but shouldn't be able to suppress all of the time, disable their supresss
        if self.char_team_enum == ENUM_CHAR_TEAM_ENEMY or self.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:
            suppress_boolean = True
            if (self.char_type_enum >= ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SOLDIER
            and self.char_type_enum >= ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SOLDIER):
                suppress_boolean = False

        if isinstance(self.ability_list, list):
            self.ability_list.append(Item(item_enum,suppress_boolean))
        else:
            self.ability_list = []
            self.ability_list.append(Item(item_enum,suppress_boolean))

        #If this is not a pc char (whose abilities must be activated) then automatically apply any associated stat changes:
        if self.char_team_enum != ENUM_CHAR_TEAM_PC:
            item_id = self.ability_list[len(self.ability_list)-1]
            self.change_char_stats(item_id,True,True)

    #equip_item: item_index: indicates which BACKPACK SLOT this item should be removed from (-1 works fine when equipping starting kit); item_inst_id: indicates the item being equipped.
    def equip_item(self ,item_inst_id, item_index ,starting_equip_boolean = False):
        if isinstance(item_inst_id.equip_slot_list,list):
            #Iterate through equip_slot_list, matching with corresponding empty positions in the self.inv_list;
            #The first empty applicable slot we find, we'll add our item to position.
            item_equipped = False
            for i in range(0,len(item_inst_id.equip_slot_list)):
                if isinstance(item_inst_id.equip_slot_list[i], list):
                    for nested_i in range(0,len(item_inst_id.equip_slot_list[i])):
                        item_equip_slot_enum = item_inst_id.equip_slot_list[i][nested_i]
                        if self.inv_list[item_equip_slot_enum] == -1: #We don't include this break here so that a copy of the item will be placed in both empty hand slots
                            self.inv_list[item_equip_slot_enum] = item_inst_id
                            item_equipped = True

                if item_equipped:
                    break

                item_equip_slot_enum = item_inst_id.equip_slot_list[i]
                if self.inv_list[item_equip_slot_enum] == -1:
                    self.inv_list[item_equip_slot_enum] = item_inst_id
                    item_equipped = True
                    break

            # Only remove from backpack if item_index points to a backpack slot; this is necessary because when we're adding an item
            # for the first time as part of a character's starting kit, it doesn't yet exist as one of the 'backpack slots'
            if item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS and item_index < len(self.inv_list):
                # Remove corresponding position in list, this should be one of the 'backpack' indices:
                del self.inv_list[item_index]
        else:
            print \
                (f"equip_item method for {self.name} with item: {item_inst_id.item_name}, equip_slot_enum == -1, which means we're trying to equip an item that is not equippable, something went wrong.")
        if item_equipped:
            if not starting_equip_boolean:
                print(f"{self.name} has equipped the {item_inst_id.item_name}")
            if item_inst_id.changes_stats_boolean:
                self.change_char_stats(item_inst_id, True ,starting_equip_boolean)
        else:
            print(f"equip_item method for {self.name} with item: {item_inst_id.item_name}, we entered this method and yet could not equip the item, something went very wrong.")

    def unequip_item(self ,item_inst_id, item_index, starting_equip_boolean = False):
        # Remove from corresponding self.inv_list position:
        self.inv_list[item_index] = -1
        # Check to see if this item has a nested list, which indicates that it is a two-handed item;
        # If it is, then be sure to remove from both hand slots:
        if isinstance(item_inst_id.equip_slot_list[0],list):
            self.inv_list[ENUM_EQUIP_SLOT_RH] = -1
            self.inv_list[ENUM_EQUIP_SLOT_LH] = -1
        # add to end of list:
        self.inv_list.append(item_inst_id)
        print(f"{self.name} has unequipped the {item_inst_id.item_name}")
        if item_inst_id.changes_stats_boolean:
            self.change_char_stats(item_inst_id, False, starting_equip_boolean)

    def defunct_swap_equip_item(self ,first_item_id ,first_item_index ,second_item_id ,second_item_index
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

    def check_valid_item_equip(self,item_id_to_equip):
        #It's a list:
        if isinstance(item_id_to_equip.equip_slot_list,list):
            #Before iterating through the list, set this == False
            invalid_equip_found = False
            #Iterate through our outer list - applicable for all items
            for i in range(0,len(item_id_to_equip.equip_slot_list)):
                #Check to see if there is a nested_list here; if there is, it indicates a two-handed item:
                if isinstance(item_id_to_equip.equip_slot_list[i], list):
                    #In this case we're checking a two-handed item, so if ANY of the equip_slot positions in the char inv_list are filled, return false.
                    for nested_i in range(0,len(item_id_to_equip.equip_slot_list[i])):
                        item_equip_slot = item_id_to_equip.equip_slot_list[i][nested_i]
                        if self.inv_list[item_equip_slot] != -1:
                            print("This item requires two hands to wield; make sure that both of your hands are free before equipping.")
                            invalid_equip_found = True
                            return False
                        #If we iterate through this list and the last corresponding item_equip_slot on the char_inv_list
                        #is still == -1, then this is a valid equip, we can return true now:
                        elif self.inv_list[item_equip_slot] == -1 and nested_i == len(item_id_to_equip.equip_slot_list[i])-1:
                            #print("Debug only: check_valid_item_equip returning TRUE for a two-handed item.")
                            return True

                if invalid_equip_found:
                    break

                #In this case we're checking for a ONE handed item, so if ANY of the corresponding equip slots in the
                # char inv_list are empty, return TRUE
                item_equip_slot = item_id_to_equip.equip_slot_list[i]
                if self.inv_list[item_equip_slot] == -1:
                    #print("Debug only: check_valid_item_equip returning TRUE for one-handed item, body item, or accessory item.")
                    return True
        else: #Else: It must therefore == -1
            print(f"The {item_id_to_equip.item_name} is not an item that can be equipped.")
            return False

        #print(f"check_valid_item_equip method for char_inst {self.name}, for item name: {item_id_to_equip.item_name}, none of our conditions executed, something likely went wrong, returning False.")
        print(f"Can't equip the {item_id_to_equip.item_name}--make sure that the corresponding equipment slot is free.")
        return False

    def add_or_remove_char_from_room_list(self,room_id,add_boolean):

        if isinstance(room_id, Room):
            #Find array to use - checks to make sure the appropriate list exists first- and if it doesn't, then it creates, then adds:
            if self.char_team_enum == ENUM_CHAR_TEAM_PC:
                if not isinstance(room_id.pcs_in_room_list, list):
                    room_id.pcs_in_room_list = []
                ar_to_use = room_id.pcs_in_room_list
            elif self.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                if not isinstance(room_id.enemies_in_room_list, list):
                    room_id.enemies_in_room_list = []
                ar_to_use = room_id.enemies_in_room_list
            elif self.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:
                if not isinstance(room_id.neutrals_in_room_list, list):
                    room_id.neutrals_in_room_list = []
                ar_to_use = room_id.neutrals_in_room_list

            #Append to end of list:
            if add_boolean:
                ar_to_use.append(self)

            #Del element position from list:
            else:
                if self in ar_to_use:
                    ar_to_use.remove(self)
        else:
            print(f"A non-Room object was fed to the method add_chars_to_room_list for Char with name: {self.name}")
