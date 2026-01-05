

TOTAL_LINE_W = 130

NIFFY_W = 26*2
NIFFY_H = 26*2

GAME_STATE_CHOOSE_CHARS = 0
GAME_STATE_MAIN = 1
GAME_STATE_ACCESS_INV = 2
GAME_STATE_PRINT_BIO = 3
GAME_STATE_PASSING_ITEM = 4
GAME_STATE_COMBAT_ASSIGN_COMMAND = 5
GAME_STATE_COMBAT_TARGET_RANK = 6
GAME_STATE_COMBAT_EXECUTE_ACTION = 7
GAME_STATE_INITIALIZING_NEW_TURN = 8
GAME_STATE_COMBAT_CHOOSE_ATTACK = 9
GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST = 10
GAME_STATE_USE_TARGET_ITEM = 11
GAME_STATE_ACCESS_ABIL_MAIN_GAME_STATE = 12
GAME_STATE_PREP_COMBAT = 13
GAME_STATE_CHOOSE_DOOR_DIRECTION = 14

ENUM_LOCATION_NIFFY = 0
ENUM_LOCATION_PLANET = 1
ENUM_LOCATION_ASTARES = 2
ENUM_LOCATION_SPACE = 3
ENUM_LOCATION_BATTLESHIP = 4
ENUM_LOCATION_NIFFY_SHUTTLE = 5
ENUM_LOCATION_ESCAPE_POD = 6
ENUM_LOCATION_RAPTOR = 7
ENUM_LOCATION_MOON_PALE = 8
ENUM_LOCATION_PIRATE_SHIP = 9
ENUM_LOCATION_DERELICT = 10
ENUM_LOCATION_GARBAGE_FREIGHTER = 11
ENUM_LOCATION_PLANET_SHUTTLE = 12
ENUM_LOCATION_MOON_DARK = 13
ENUM_LOCATION_MOON_RED = 14

ENUM_ROOM_NIFFY_CORRIDOR_BASIC_EAST_WEST = 0
ENUM_ROOM_NIFFY_STASIS_CHAMBER = 1 #This is where our players start the game. Also can insert badly injured or infected players in here and they will remain safe and ignored by enemies. Requires someone else to open again however.
ENUM_ROOM_NIFFY_COMMISSARY = 2 #Can find food for free here, or pay for it
ENUM_ROOM_NIFFY_BARRACKS = 3
ENUM_ROOM_NIFFY_ARMORY = 4 #Can find weapons for free here
ENUM_ROOM_NIFFY_SEC_ROOM = 5 #Can lock or open doors from here
ENUM_ROOM_NIFFY_BRIDGE = 6 #Can use sensors from here to locate enemies throughout the map, and can also direct the ship toward another location in the game, such as the planet, one of its moons, the battleship, etc.
ENUM_ROOM_NIFFY_ENVIRONMENTAL_CONTROL = 7 #Can vent or pressurize rooms from here, thereby suffocating enemies, fires, and toxic gas
ENUM_ROOM_NIFFY_AIRLOCK = 8 #Allows access to outside of ship
ENUM_ROOM_NIFFY_MEDBAY = 9 #Can exchange technology for healing items
ENUM_ROOM_NIFFY_ENGINE_ROOM = 10 #Powers or unpowers rooms in the game, must be operated to be used.
ENUM_ROOM_NIFFY_SHUTTLE_BAY = 11 #Can provide win scenario if a certain amount of scrap and/or technology is invested
ENUM_ROOM_NIFFY_ENGINEERING_BAY = 12 #Can fabricate new items and equipment here
ENUM_ROOM_NIFFY_CREW_QUARTERS = 13 #Can sleep here at the cost of food to regain some hp and sanity; can only be every 10-20 turns
ENUM_ROOM_NIFFY_SUPPLY_CLOSET = 14 #Can find free useful items
ENUM_ROOM_NIFFY_HYDROPONICS_LAB = 15 #Can slowly grow food here
ENUM_ROOM_NIFFY_OFFICERS_LOUNGE = 16
ENUM_ROOM_NIFFY_COMMUNICATION_STATION = 17 #Can broadcast for help from here (invites Pirates faster), can also create sounds in powered rooms where there are no characters in order to lure enemies there
ENUM_ROOM_NIFFY_ARBORETUM = 18 #High concentration of enemies here
ENUM_ROOM_NIFFY_STORAGE_ROOM = 19 #Can find scrap and tech here
ENUM_ROOM_NIFFY_LABORATORY = 20 #Can perform experiments on enemies here (dead or alive) to learn about their vulnerabilities.
ENUM_ROOM_NIFFY_REC_ROOM = 21
ENUM_ROOM_NIFFY_GROWTH_VATS = 22
ENUM_ROOM_NIFFY_ROBOTICS_BAY = 23
ENUM_ROOM_NIFFY_STORAGE_LOCKER = 24 #At the cost of credits, can store items here to retrieve between runs
ENUM_ROOM_NIFFY_RECYCLER = 25 #Can exchange resources here: scrap, technology and items for credits
ENUM_ROOM_NIFFY_ASTROMETRICS = 26
ENUM_ROOM_NIFFY_ANIMAL_LAB = 27
ENUM_ROOM_NIFFY_READY_ROOM = 28 #Can view upcoming crisis events from here
ENUM_ROOM_NIFFY_COMPUTER_CORE = 29 #This room has a terminal from which you can remotely OPERATE other rooms, if you pass a science skill test. Characters only have to pass this skill check once until they move again.
ENUM_ROOM_NIFFY_INTERSECTION = 30 #Like the corridor but contains more doors.
ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST = 31
ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST = 32
ENUM_ROOM_NIFFY_CORRIDOR_BASIC_NORTH_SOUTH = 33
ENUM_ROOM_VACUUM = -1 #This is what each location grid is initialized to start

ENUM_ITEM_FLASHLIGHT = 0 #No use for this I can currently see; could just contribute to certain scavenge type skill tests, if I even implement those.
ENUM_ITEM_SHOTGUN = 1
ENUM_ITEM_REVOLVER = 2
ENUM_ITEM_LASER_PISTOL = 3
ENUM_ITEM_SNIPER_RIFLE = 4
ENUM_ITEM_MOP = 5 #Can remove the 'slime' environmental hazards - sticky slime, toxic slime, etc.
ENUM_ITEM_FIRE_AXE = 6 #Contributes to skill tests when jamming doors
ENUM_ITEM_TORQUE_WRENCH = 7 #Contributes to certain engineering skill tests
ENUM_ITEM_SUB_MACHINE_GUN = 8
ENUM_ITEM_LASER_RIFLE = 9
ENUM_ITEM_FLAME_THROWER = 10
ENUM_ITEM_GRENADE = 11
ENUM_ITEM_ROCKET_LAUNCHER = 12
ENUM_ITEM_LEAD_PIPE = 13 #Just a very basic melee weapon
ENUM_ITEM_ASSAULT_RIFLE = 14
ENUM_ITEM_EMP_GRENADE = 15 #Functions like frag grenade but does no damage to bio units, only high damage and stunt to robot units
ENUM_ITEM_MOTION_DETECTOR = 16 #When 'u'sed, shows you exactly how many enemies are in the next room.
ENUM_ITEM_MEDKIT = 17 #Heals 5 HP, removes all status effects except for stunned and infected.
ENUM_ITEM_HEALING_NANITE_INJECTOR = 18 #Acts like a stronger version of Cragos' passive heal
ENUM_ITEM_TASER = 19
ENUM_ITEM_DNA_TESTER = 20 # Can be used on neutral units to see if they are aliens in disguise... Also reveals how many infection points they have, if any.
ENUM_ITEM_TRICORDER = 21 # ... ?
ENUM_ITEM_FIRE_EXTINGUISHER = 22 #Removes fire environmental hazard from current room.
ENUM_ITEM_SUIT_ENVIRONMENTAL = 23
ENUM_ITEM_SUIT_MARINE = 24
ENUM_ITEM_SUIT_VACUUM = 25
ENUM_ITEM_SHIELD_BELT = 26 #Adds evasion and/or armor
ENUM_ITEM_PRISONER_JUMPSUIT = 27
ENUM_ITEM_ENGINEER_GARB = 28
ENUM_ITEM_MEDICAL_SCRUBS = 29
ENUM_ITEM_SCIENTIST_LABCOAT = 30
ENUM_ITEM_OFFICER_JUMPSUIT = 31
ENUM_ITEM_CIVILIAN_JUMPSUIT = 32
ENUM_ITEM_FLAK_ARMOR = 33
ENUM_ITEM_ADRENAL_PEN = 34 #Increases accuracy and speed for a set amount of turns; single use.
ENUM_ITEM_TARGETING_HUD = 35
ENUM_ITEM_STUN_BATON = 36
ENUM_ITEM_POLICE_TRUNCHEON = 37
ENUM_ITEM_RIOT_SHIELD = 38
ENUM_ITEM_FLAK_SHIELD = 39
ENUM_ITEM_PHASE_SHIELD = 40
ENUM_ITEM_PLASMA_TORCH = 41 #Doubles as a decent melee weapon; adds to skill check when repairing doors.
ENUM_ITEM_FISTS_CHILD = 42
ENUM_ITEM_FISTS_ADULT = 43
ENUM_ITEM_FISTS_GIANT = 44
ENUM_ITEM_SPINE_PROJECTILE = 45
ENUM_ITEM_SPINE_PROJECTILE_VENOMOUS = 46
ENUM_ITEM_LARVA_INJECTION_BARB = 47 #Causes infection
ENUM_ITEM_LARVA_WRITHING_TENDRIL = 48
ENUM_ITEM_FIELD_MEDICINE = 49 #Doctor ability, consumes turn
ENUM_ITEM_ENERGIZING_STIM_PRICK = 50 #Avia ability, does not consume turn.
ENUM_ITEM_MONSTROUS_CLAW = 51
ENUM_ITEM_KIRAS_NOISY_GAME = 52 #Can be triggered and then dropped; it causes enemies in adjacent rooms to come flocking toward it, potentially breaking down doors to do so.
ENUM_ITEM_MACHINE_PISTOL = 53
ENUM_ITEM_ACID_SPIT = 54
ENUM_ITEM_ACID_CLOUD = 55
ENUM_ITEM_SPINE_PROJECTILE_INFECTED = 56
ENUM_ITEM_ACID_SACK = 57
ENUM_ITEM_DESPERATE_CLAW = 58
ENUM_ITEM_SECURITY_VEST = 59
ENUM_ITEM_TOXIC_GRENADE_LAUNCHER = 60
ENUM_ITEM_STICKY_SLIME = 61
ENUM_ITEM_FILAMENT_SPRAY = 62
ENUM_ITEM_CONCUSSION_GRENADE_LAUNCHER = 63
ENUM_ITEM_CRUDE_BUZZSAW = 64
ENUM_ITEM_HAND_FLAMER = 65 #Torvald ability
ENUM_ITEM_LIGHT_MG = 66
ENUM_ITEM_FRAG_GRENADE_LAUNCHER = 67
ENUM_ITEM_WRIST_ROCKETS = 68 #Torvald ability
ENUM_ITEM_SHOCKING_GRASP = 69 #Torvald ability
ENUM_ITEM_PERSONAL_SHIELD_GENERATOR = 70  #Torvald ability
ENUM_ITEM_HOLD_THE_LINE = 71
ENUM_ITEM_SPAWN_LIGHT_SENTRY_GUN = 72
ENUM_ITEM_SPAWN_BUZZSAW_DROID = 73
ENUM_ITEM_SPAWN_LIGHT_SENTINEL_DROID = 74
ENUM_ITEM_SPAWN_LIGHT_FLAMER_DROID = 75
ENUM_ITEM_SPAWN_LIGHT_SHOTGUN_DROID = 76
ENUM_ITEM_TOTAL_ITEMS = 77

ENUM_CHARACTER_MERCENARY_MECH = 0 #Sec - Comes equipped with built-in hand-flamer, laser, and wrist rockets which use ability points rather than ammunition.
ENUM_CHARACTER_GAMER = 1 #Survivor - Hacker, gamer, a girl; only character that is small enough to use vents. Is better at hiding than other characters.
ENUM_CHARACTER_ENGINEER = 2 #Engineer - Can interact with engineering bay in useful ways.
ENUM_CHARACTER_MECH_MAGICIAN = 3 #Engineer - A 'summoner': Can transform scrap into useful droids.
ENUM_CHARACTER_SCIENTIST = 4 #Scientist
ENUM_CHARACTER_CRIMINAL = 5 #Survivor; aka 'The Werewolf' - slowly transforms and will eventually turn on the player.
ENUM_CHARACTER_CEO = 6 #Civilian - Is secretly a traitor?
ENUM_CHARACTER_SERVICE_DROID = 7 #Scientist
ENUM_CHARACTER_OGRE = 8 #Sec - Tanky melee damage dealer, has
ENUM_CHARACTER_JANITOR = 9 #Survivor - Comes equipped with a mop (clears various harmful slimes and sludges) and a fire extinguisher, as well as a few key cards. Is otherwise useless.
ENUM_CHARACTER_PLAYBOY = 10 #Civilian - Is generally useless but a wealthy prince, gives extra completion points if you finish the game with him.
ENUM_CHARACTER_BIOLOGIST = 11 #Scientist - Can interact with the laboratory in useful ways
ENUM_CHARACTER_SOLDIER = 12 #Security - Standard and basic security choice, comes equipped with high quality items but is otherwise not exceptional.

ENUM_CHARACTER_ENEMY_SKITTERING_LARVA = 13
ENUM_CHARACTER_ENEMY_SPINED_SPITTER = 14
ENUM_CHARACTER_ENEMY_LUMBERING_MAULER = 15
ENUM_CHARACTER_ENEMY_FRENZIED_SLASHER = 16
ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SOLDIER = 17 #First trans used for switching suprress on-off in add_ability()
ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SCIENTIST = 18
ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_ENGINEER = 19
ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_OFFICER = 20 #last trans - used for switch suprress on-off in add_ability()

ENUM_CHARACTER_NEUTRAL_INFECTED_SCIENTIST = 21

ENUM_CHARACTER_ENEMY_SODDEN_SHAMBLER = 22
ENUM_CHARACTER_ENEMY_WEBBED_LURKER = 23

ENUM_CHARACTER_NEUTRAL_JITTERING_BUZZSAW = 24
ENUM_CHARACTER_NEUTRAL_WHIPSTICH_SENTINEL = 25
ENUM_CHARACTER_NEUTRAL_SPINNING_SCATTERSHOT = 26
ENUM_CHARACTER_NEUTRAL_FUMIGATING_FLAMER = 27
ENUM_CHARACTER_NEUTRAL_LIGHT_SENTRY_DRONE = 28

ENUM_CHARACTER_MAX_CHARS = 29

ENUM_SCAVENGE_RESOURCE_TECH_BASIC = 0
ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED = 1
ENUM_SCAVENGE_RESOURCE_FOOD = 2
ENUM_SCAVENGE_RESOURCE_CREDITS = 3
ENUM_SCAVENGE_RESOURCE_FUEL_ENGINE = 4
ENUM_SCAVENGE_RESOURCE_AMMO = 5
ENUM_SCAVENGE_TOTAL_RESOURCES = 6 #At and beyond this index is where items are stored in the scavenge_resource_list for room objects

ENUM_DOOR_UNLOCKED = 0
ENUM_DOOR_LOCKED = 1
ENUM_DOOR_JAMMED = 2
ENUM_DOOR_DESTROYED = 3
ENUM_DOOR_OPEN_SPACE = 4

ENUM_FEATURE_NIFFY_SR_PIPE_LEAKY = 0
ENUM_FEATURE_NIFFY_VALVE_BRONZE_BROKEN = 1
ENUM_FEATURE_NIFFY_VALVE_STEEL_BROKEN = 2
ENUM_FEATURE_ALIEN_EGG_SACK = 3

ENUM_HAZARD_GAS_TOXIC = 0
ENUM_HAZARD_GAS_VACUUM = 1
ENUM_HAZARD_FIRE = 2
ENUM_HAZARD_ELECTRIC_CURRENT = 3

ENUM_EQUIP_SLOT_BODY = 0
ENUM_EQUIP_SLOT_ACCESSORY = 1
ENUM_EQUIP_SLOT_RH = 2
ENUM_EQUIP_SLOT_LH = 3
ENUM_EQUIP_SLOT_TOTAL_SLOTS = 4 #Any element at or beyond this index in the character.inv_list should be considered to be an instance of an item.

ENUM_ITEM_STAT_BOOST_SECURITY = 0
ENUM_ITEM_STAT_BOOST_ENGINEERING = 1
ENUM_ITEM_STAT_BOOST_SCIENCE = 2
ENUM_ITEM_STAT_BOOST_STEALTH = 3
ENUM_ITEM_STAT_BOOST_STRENGTH = 4
ENUM_ITEM_STAT_BOOST_WISDOM = 5
ENUM_ITEM_STAT_BOOST_INTELLIGENCE = 6
ENUM_ITEM_STAT_BOOST_DEXTERITY = 7
ENUM_ITEM_STAT_BOOST_ACCURACY = 8
ENUM_ITEM_STAT_BOOST_HP = 9
ENUM_ITEM_STAT_BOOST_SANITY = 10
ENUM_ITEM_STAT_BOOST_ACTION_POINTS = 11
ENUM_ITEM_STAT_BOOST_ABILITY_POINTS = 12
ENUM_ITEM_STAT_BOOST_SCAVENGING = 13
ENUM_ITEM_STAT_BOOST_ARMOR = 14
ENUM_ITEM_STAT_BOOST_EVASION = 15
ENUM_ITEM_STAT_BOOST_FIRE_RES = 16
ENUM_ITEM_STAT_BOOST_GAS_RES = 17
ENUM_ITEM_STAT_BOOST_VACUUM_RES = 18
ENUM_ITEM_STAT_BOOST_ELECTRIC_RES = 19
ENUM_ITEM_STAT_BOOST_TOTAL_STATS = 20

ENUM_CHAR_TEAM_PC = 0
ENUM_CHAR_TEAM_ENEMY = 1
ENUM_CHAR_TEAM_NEUTRAL = 2

ENUM_COVER_NONE = 0 #-2 evasion for pcs in combat
ENUM_COVER_LOW = 1 #No impact on evasion
ENUM_COVER_MEDIUM = 2 #+1 evasion for pcs in combat
ENUM_COVER_HIGH = 3 #+2 evasion for pcs in combat
ENUM_COVER_FORTIFIED = 4 #+4 evasion for pcs in combat, only possible via some sort of engineer skill

ENUM_RANK_ENEMY_FAR = 0
ENUM_RANK_ENEMY_MIDDLE = 1
ENUM_RANK_ENEMY_NEAR = 2
ENUM_RANK_PC_NEAR = 3
ENUM_RANK_PC_MIDDLE = 4
ENUM_RANK_PC_FAR = 5
ENUM_RANK_TOTAL_RANKS = 6

ENUM_AI_COMBAT_MELEE = 0
ENUM_AI_COMBAT_RANGED_COWARD = 1
ENUM_AI_COMBAT_SUPPRESSOR = 2
ENUM_AI_COMBAT_OVERWATCH = 3
ENUM_AI_COMBAT_STATIONARY_OVERWATCH = 5
ENUM_AI_TOTAL_AI_PREFERENCES = 6

#In general, for any stat, 7 (which represents a 70% chance) should be average
#Misc., 'stat' type constants:
ENUM_AVERAGE_ACCURACY_SCORE = 7
ENUM_AVERAGE_EVASION_SCORE = 0
ENUM_MIN_COMBAT_RAN_NUM = 0 #Should also be used for skill checks
ENUM_MAX_COMBAT_RAN_NUM = 9
ENUM_MAX_RAN_INITIATIVE_VAL = 5
ENUM_STIM_PRICK_AP_BOOST = 2
ENUM_BASE_MAX_INFECTION = 6
ENUM_HOLD_THE_LINE_EVADE_BONUS = 1
ENUM_PERSONAL_SHIELD_BONUS = 1
ENUM_ADRENAL_PEN_BONUS = 2
ENUM_OGRE_MELEE_ACC_BONUS = 1
ENUM_OGRE_MELEE_ACC_BONUS = 1
ENUM_OGRE_MELEE_DMG_BONUS = 3

ENUM_STATUS_EFFECT_FIRE = 0
ENUM_STATUS_EFFECT_BLEED = 1
ENUM_STATUS_EFFECT_POISON = 2
ENUM_STATUS_EFFECT_STUN = 3
ENUM_STATUS_EFFECT_INFECT = 4
ENUM_STATUS_EFFECT_SUPPRESSED = 5
ENUM_STATUS_EFFECT_TOTAL_EFFECTS = 6

ENUM_DOT_FIRE = 5
ENUM_DOT_POISON = 4
ENUM_BASE_UNCONSCIOUS_COUNT = 4 #This is how many turns (-1) that the characters get while in combat to be revived before dying.
ENUM_SUPPRESSED_EVASION_DEBUFF = 2
ENUM_SUPPRESSIVE_FIRE_ACCURACY_DEBUFF = 1
ENUM_SUPPRESSED_SPEED_DEBUFF =2

