# Import user made modules
from constants import *
from models.character import Character
from models.item import Item
from models.room import Room
from util.utils import *
from models.abil import Abil

#Import built-in python modules:
import random
import textwrap
import keyboard
import string
from collections import Counter
import pygame
import sys

if __name__ == '__main__':

    #region pygame setup:

    GAME_WIDTH = 320
    GAME_HEIGHT = 180

    #Initialize all of pygame's modules:
    pygame.init()

    #Create surface for smaller, pixel art size:
    game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    # Create fullscreen window at user's native resolution
    debug_full_screen = True
    if debug_full_screen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1920, 1080))

    # Get the actual screen size
    screen_width, screen_height = screen.get_size()

    #Set 'clock': this will limit FPS
    clock = pygame.time.Clock()

    #region Define global vars:

    game_end = False
    print_room_recap = True
    choose_weapon_boolean = False
    choose_ability_boolean = False
    attempting_suppress_boolean = False #only used for choose weapon logic
    attempting_overwatch_boolean = False #only used for choose weapon logic
    overwatch_loop_mode_enabled = False
    combat_begun = False #Reset to false in game_state GAME_STATE_INITIALIZING_NEW_TURN, only switched to true when iterating through pc_list and certain combat-related conditions met.
    using_ability_boolean = False
    prep_combat_boolean = False
    pc_fleeing_combat_boolean = False

    fleeing_pc_id = -1
    opportunity_attacker_id = -1
    cur_char = -1
    cur_char_index = 0
    cur_grid_to_use = -1
    cur_room_inst_id = -1
    new_turn_cur_char_index = 0 #Used for iterating through pc_char_list at the start of turn, determining whether or not we need to start a fight with enemies
    cur_combat_room_id = -1

    overwatch_target_id = -1
    overwatch_attacker_id = -1
    cur_overwatch_attacker_index = -1

    passing_item_id = -1 #Used with GAME_STATE_PASSING_ITEM and GAME_STATE_USE_TARGET_ITEM; also used to hold the item_id of what item is being 'u'sed
    passing_item_index = -1 #Used with GAME_STATE_PASSING_ITEM

    cur_game_state = GAME_STATE_CHOOSE_CHARS
    prev_game_state = GAME_STATE_INITIALIZING_NEW_TURN

    #Global resources:
    basic_tech_total = 0
    advanced_tech_total = 0
    credits_total = 0
    food_total = 0
    fuel_total = 0 #Called 'neutronium' fuel, used for niffy engine
    ammo_total = 0

    combat_initiative_list = -1
    cur_combat_char = -1
    cur_combat_round = 0
    combat_rank_list = -1
    overwatch_attacker_list = -1

    pc_char_list = [] #Used for the player's final chosen party
    enemy_char_list = []
    neutral_char_list = []
    total_chars_stats_list = [] #Used simply to display char stats
    total_chars_bio_list = [] #Used to display a char's biography

    #endregion

    # region Manually build our location grid for the niffy location AND add debug enemies:

    # location grid for niffy:
    location_grid_niffy = [[0 for _ in range(NIFFY_W)] for _ in range(NIFFY_H)]
    #Initialize each grid coordinate to ENUM_ROOM_VACUUM
    for yy in range(0,len(location_grid_niffy)):
        for xx in range(0,len(location_grid_niffy[yy])):
            location_grid_niffy[yy][xx] = ENUM_ROOM_VACUUM

    origin_grid_y = len(location_grid_niffy) // 2
    origin_grid_x = len(location_grid_niffy[0]) // 2

    location_grid_niffy[origin_grid_y][origin_grid_x] = Room(ENUM_LOCATION_NIFFY, ENUM_ROOM_NIFFY_STASIS_CHAMBER,origin_grid_x,origin_grid_y,location_grid_niffy)
    location_grid_niffy[origin_grid_y][origin_grid_x].already_explored_boolean = True
    location_grid_niffy[origin_grid_y][origin_grid_x-1] = Room(ENUM_LOCATION_NIFFY,ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST,origin_grid_x-1,origin_grid_y,location_grid_niffy)
    location_grid_niffy[origin_grid_y][origin_grid_x+1] = Room(ENUM_LOCATION_NIFFY,ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST,origin_grid_x+1,origin_grid_y,location_grid_niffy)

    #Iterate through again, Build 'vacuum' room to any coordinate with the corresponding enum:
    for yy in range(0,len(location_grid_niffy)):
        for xx in range(0,len(location_grid_niffy[yy])):
            if location_grid_niffy[yy][xx] == ENUM_ROOM_VACUUM:
                location_grid_niffy[yy][xx] = Room(ENUM_LOCATION_NIFFY, ENUM_ROOM_VACUUM, yy, xx, location_grid_niffy)

    #region Debug placeholder: Add some random enemies and neutral chars to the starting room:
        # char_type_enum, spawn_grid_x, spawn_grid_y, spawn_grid, char_team_enum
    debug_chars = True
    if debug_chars:

        ammo_total += 55

        #Neutral scientist
        for i in range(0,0):
            neutral_char_list.append(Character(ENUM_CHARACTER_NEUTRAL_INFECTED_SCIENTIST,origin_grid_x,origin_grid_y,location_grid_niffy,
                                               ENUM_CHAR_TEAM_NEUTRAL,True))

        #Chittering lurker:
        for i in range(0, random.randint(0, 0)): #1,4
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_WEBBED_LURKER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY,True))

        #Spined Spitter
        for i in range(0, random.randint(0, 0)): #1,3
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_SPINED_SPITTER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY,True))

        #Sodden Shambler
        for i in range(0, random.randint(0, 0)): #1,3
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_SODDEN_SHAMBLER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY,True))

        #Lumbering mauler
        for i in range(0, random.randint(0, 0)): #1,3
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_LUMBERING_MAULER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY,True))

        #Skittering Larva
        for i in range(0, random.randint(1, 1)): #1,3
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_SKITTERING_LARVA, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY,True))

        # Flamer droid:
        for i in range(0, random.randint(0, 0)):
            enemy_char_list.append(
                Character(ENUM_CHARACTER_NEUTRAL_FUMIGATING_FLAMER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_NEUTRAL, True))

        # Scattershot droid:
        for i in range(0, random.randint(0, 0)):
            enemy_char_list.append(
                Character(ENUM_CHARACTER_NEUTRAL_SPINNING_SCATTERSHOT, origin_grid_x, origin_grid_y,
                          location_grid_niffy,
                          ENUM_CHAR_TEAM_NEUTRAL, True))

        # Whipstich sentinel droid:
        for i in range(0, random.randint(0, 0)):
            enemy_char_list.append(
                Character(ENUM_CHARACTER_NEUTRAL_WHIPSTICH_SENTINEL, origin_grid_x, origin_grid_y,
                          location_grid_niffy,
                          ENUM_CHAR_TEAM_NEUTRAL, True))

        # Jittering buzzsaw droid:
        for i in range(0, random.randint(0, 0)):
            enemy_char_list.append(
                Character(ENUM_CHARACTER_NEUTRAL_JITTERING_BUZZSAW, origin_grid_x, origin_grid_y,
                          location_grid_niffy,
                          ENUM_CHAR_TEAM_NEUTRAL, True))

        # Light sentry drone:
        for i in range(0, random.randint(0, 0)):
            enemy_char_list.append(
                Character(ENUM_CHARACTER_NEUTRAL_LIGHT_SENTRY_DRONE, origin_grid_x, origin_grid_y,
                          location_grid_niffy,
                          ENUM_CHAR_TEAM_NEUTRAL, True))

        # Transmogrified Soldier - overwatch type:
        wep_loadout_num = 0
        for i in range(0,0): #0,9
            if i != 0 and i % 3 == 0:
                wep_loadout_num += 1
            enemy_char_list.append(
                Character(ENUM_CHARACTER_ENEMY_TRANSMOGRIFIED_SOLDIER, origin_grid_x, origin_grid_y, location_grid_niffy,
                          ENUM_CHAR_TEAM_ENEMY, True,wep_loadout_num))

    #endregion

    # endregion

    #region Create a temporary copy of each character, use their stats to fill a print list for convenience:

    for i in range(0,ENUM_CHARACTER_SOLDIER+1): #ENUM_CHARACTER_SOLDIER is our last pc character
        temp_pc_char = Character(i,0,0,location_grid_niffy,ENUM_CHAR_TEAM_PC,False)
        primary_role_str = "Undefined"
        char_class_snippet = "Undefined"
        #Now define total_chars_bio_list:
        if i == ENUM_CHARACTER_OGRE:
            total_chars_bio_list.append("Cragos, 'The Ogre':\n\nCragos was intended to be just another of the millions of faceless clones born into servitude by the Kethas Corporation, but a power surge in his gestation vat caused an excessive amount of growth hormone to be released into his developmental stew. As a result, he emerged from his birthing chamber weeks before his brothers and sisters, a hulking giant of a man with the mind of a child, and a misshapen face that only a mother could love... If only he had one.\n\nThe scientists at Keth Corp. were bemused by this unanticipated variant, and rigorously tested his physical and mental capabilities to determine the viability of his strain. They called it 'testing,' but Cragos would come to know the euphimism for what it truly was: torture.\n\nHe was only six weeks old by the time they had subjected him to a battery of tests that included blunt force trauma, precision tissue damage, and unimaginable G-forces, all to determine the tolerances of his physical structure, and also the rate of his healing factor, which surpassed even that of his kin. He was at least spared the psychological conditioning, not by any act of mercy, but merely because he was overlooked and forgotten after the researchers grew bored of his screams, labeling his mutation as 'UNSATISFACTORY.' He was deemed too large and clumsy to be useful on the battlefield, and too hideous to serve as steward in the gilded homes of the elite back in the Core.\n\nHe would have been reprocessed and recycled, in fact, liquified and fed back to his fellow clones as essential nutrients, had the interstellar freighter that was his home not been attacked by raiders from the Fringe. It was of course Keth Corp. policy to never reveal the secrets of their proprietary technology, and so they reduced the massive hulk of their starship to ruins in the depths of space, rather than submit to the pirates' boarding party. The brigands did not leave empty handed, nonetheless.\n\nThey found Cragos still clinging to life in a small pressurized compartment in a field of floating debris, like a cockroach that refused to die, or a caterpillar cocooned in stasis, patiently awaiting chrysalis. Unlike the scientists at Keth Corp., they found good use for his muscle among their ranks, all right.\n\nBanditry was their trade, and his healing factor an invaluable asset. The absence of psychological conditioning had made it possible for Cragos to adjust to their nomadic lifestyle, to view himself as an invidual at last, as a person who could inspire respect--if never love.\n\nThey named him 'Cragos,' after the son of the stone god who ruled the mountains of their homeworld. And as the years passed he became well known as the most vicious and relentless of their clan. Eventually he outlived them all, and when the very last of their clan had been struck down by enforcers from the Core, Cragos struck out into the void to earn his own coin, plying his trade as a mercenary for hire, a dealer of death and punishment alike. Yet he never forgot the faces of his tormentors who had given him life, and always he hoarded the horror of his past as fuel for future conquests.\n\nIt was a kidnapping job gone sideways that found him in a stasis chamber aboard the Keth Corp. research vessel 'Niffy.' And there he remains: a caged animal once more, eyes closed, yet not sleeping--always dreaming of vengeance against the inexhaustible and inexorable corporation that made him... Always dreaming... And always promising pain.\n\nGameplay features: Cragos is a resilient tank who deals double damage with melee weapons and extra damage with his fists. He is very fond of wrestling opponents and dismembering them with his bare hands, often putting himself into compromised positions in order to do so. His RAGE meter builds while fighting and when it reaches 10, he becomes uncontrollable for 6-10 turns, smashing room features, items, or attacking friendly characters. He has poor accuracy when using ranged weapons, and therefore should rely upon weapons that offer multiple hits, such as the shotgun or flame thrower. He is also too large to be able to use the 'HIDE' command. Abilities: Healing Factor: automatically heals 1 hp and 1 infection point every 3-4 turns (passive); Thick Hide: +2 armor value (passive)")
            primary_role_str = "SECURITY"
            char_class_snippet = "This stubbled brute almost looks like the standard variant of the Keth Corporation clone, only... bigger. Much bigger. Uglier, too."
        elif i == ENUM_CHARACTER_SOLDIER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: As a security character, Cooper excels when buffing allies and pinning enemies down with suppressive fire. His starting kit is effective enough to give him an edge in combat for much of the early game. Abilities: Suppressing fire: 1 AP: For the next turn, any enemy that Cooper targets has a 100% chance of becoming suppressed; Focus Fire: 2 AP: For the next 2-3 turns, all friendly characters in the current battle receive +2 to their accuracy stat; Take Command: 5 AP: All friendly characters in the same room as Cooper reduce their sanity meter by 1.")
            primary_role_str = "SECURITY"
            char_class_snippet = "If the data on his identity tag is any indication, then this poor fellow's contract was nearly up. Judging by his flabby gullet, it looks like he hasn't seen the inside of a gym in years. At least he entered the stasis pod while wearing some decent equipment."
        elif i == ENUM_CHARACTER_PLAYBOY:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "Immediately identifiable is the handsome scion of the rival conglomerate Boros Incorporated, better known for his sexual conquests than his contributions to the family's sterling legacy. What is he doing here?"
        elif i == ENUM_CHARACTER_CRIMINAL:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "The barcode branded across this man's forehead displays his status as nothing more than chattle. It's not difficult to end up on the wrong side of the law as a citizen of any one of the thousands of worlds owned by Keth Corp. What is this man's crime?"
        elif i == ENUM_CHARACTER_GAMER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: Though frail and unable to use weapons, Kira abilities, when combined with her high stealth stat and starting items, can make her an effective scout. She is also the only character small enough to use the ventillation system to travel. The player will receive 10 extra victory points when completing any victory scenario with Kira. Abilties: Hide: 1 AP: Enemies have a 80% chance of ignoring Kira while this ability is active; Scurry: 2 AP: Move to an adjacent, accessible room through an open door without using move points or consuming food. This ability can only be used when Kira is moving alone.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "This unfortunate little girl must have been in the wrong place at the wrong time. Where are her parents?"
        elif i == ENUM_CHARACTER_ENGINEER:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGameplay features: ")
            primary_role_str = "ENGINEER"
            char_class_snippet = "His blue overcoat is emblazoned with the Keth Corporation's sigil of a star cresting the shoulder of a shadowed planet. The patch suggests that this is a company man, while the tool belt around his waist indicates that he works for the engineering department, most likely."
        elif i == ENUM_CHARACTER_CEO:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "Oh how the mighty have fallen! This face has been seen by almost everyone with a video feed this side of the galaxy. It's Celeste Mattix, Chief Executive Officer of the interstellar research and development corporation Zephyr Industries. One can only wonder how she lost her first-class seat."
        elif i == ENUM_CHARACTER_SERVICE_DROID:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "ENGINEER"
            char_class_snippet = "This standard service droid has been deactivated for reasons unknown. It is roughly the same size and shape as a man, with a burnished steel frame, articulated joints, and an expressionless face that sports two large mustaches engraved over a mouth slit. It sleeps in the corner of the stasis chamber with the camera lenses of its eyes wide open, seeing nothing. There is some blackened scoring around the junction box on its metal chest; the old scars of laser blasts, no doubt. Is it still operational?"
        elif i == ENUM_CHARACTER_MERCENARY_MECH:
            total_chars_bio_list.append("This character's backstory is not yet defined.\n\nGame play features: Torvald is a versatile fighter who relies heavily upon Ability Points to utilize his built-in weapons. Being cybernetic, he accumulates infection points half as quickly as organic characters, and requires twice as many before transforming. Abilities: 2 AP: Palm Laser (can WELD room features, does light damage to enemies); 4 AP: Hand Flamer (can BURN room features, and does medium damage to groups of enemies); 6 AP: Wrist Rocket (deals medium to high damage to groups of enemies); 1 AP + 1 basic_tech: Improvisational Repair: Heal 2 hp.")
            primary_role_str = "SECURITY"
            char_class_snippet = "Half of this man's face has been replaced by steel plating and electronics. A trans-humanist from the Fringe, then; such modifications are generally outlawed within the Core, especially in worlds owned by the Keth Corporation. Even in sleep he wears a malevolent grin."
        elif i == ENUM_CHARACTER_MECH_MAGICIAN:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "ENGINEER"
            char_class_snippet = "Another trans-humanist, this one more machine than woman. Her skin is deathly pale. Huge metal slits have been carved into the sides of her skull, presumably to vent the massive amount of heat generated by her cybernetically enhanced brain. A clear violation of the Keth Corporation's law against cybernetic enhancement, if ever there was one."
        elif i == ENUM_CHARACTER_BIOLOGIST:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "SCIENTIST"
            char_class_snippet = "This woman is wearing a white lab coat emblazoned with the Keth Corporation's sigil. It is disconcerting to know that she chose refuge here, in a stasis chamber, rather than face head-on whatever terrible crisis has clearly paralyzed this vessel. Surely she must know more about what happened here."
        elif i == ENUM_CHARACTER_JANITOR:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "CIVILIAN"
            char_class_snippet = "An older man in the gray overalls of a technician. A company man, by his sigil. He has a nasty looking head wound. Perhaps he saw something before his sense of self-preservation brought him here?"
        elif i == ENUM_CHARACTER_SCIENTIST:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
            primary_role_str = "SCIENTIST"
            char_class_snippet = "Another bespeckled gray beard in a white lab coat, they seem to populate most star ships--especially those that operate well outside of the known regions of space. This one has an imperious look and a slight sneer, even in stasis."
        else:
            total_chars_bio_list.append("This character's backstory is not yet defined.")
        #Add stats string to total_char_stats_list
        total_chars_stats_list.append(
            f"{i}.) {temp_pc_char.name}: Primary role: {primary_role_str}. {char_class_snippet} Security: {temp_pc_char.security}; Engineering: {temp_pc_char.engineering}; Science: {temp_pc_char.science}; Stealth: {temp_pc_char.stealth}")
        #De-reference (destroy) this instance:
        temp_pc_char = -1
    #endregion

    #region Define help text:

    help_instructions_str_list = [
        "The following is a list of available commands to be used in the primary game state:\n",
        "'SCAVENGE': This command can only be used once per room, and will automatically collect any global resources and items that can be found within the room.\n",
        "'E' or 'EAST'; 'W' or 'WEST'; 'N' or 'NORTH'; 'S' or 'SOUTH': Costs 1 action point and 1 food per character. Directional commands to move between rooms. The corresponding direction must be accessible.\n"
        "'UNLOCK {DIRECTION}': Consumes one of your key cards to unlock the door in the corresponding direction.\n",
        "'JAM {DIRECTION}': Costs 1 action point per character. Uses random scrap items found in the room and your character(s) strength to attempt to jam a door in the corresponding direction. A strength-based skill test will ensue to determine if the action was successful.\n",
        "'HIDE': Costs 1 action point to hide the character in the current room, using whatever cover they can find. A stealth-based skill check ensues to determine if this action was successful. Note that the effectiveness of this action is dependent upon the level of cover in the current room, with 'low amounts of cover' providing a 30% chance to remain concealed in the room; 'medium amounts of cover' providing a 60% chance to remain concealed in the room; and 'large amounts of cover' providing a 90% chance to remain concealed in the room.",
        "'AMBUSH': Costs 1 action point to initiate combat against an enemy or enemies in the current room while a character is HIDDEN, giving you a full extra turn against the enemy. Initiating an ambush will also allow to add other currently hidden characters to the combat. If you choose not to add them, they will remain hidden and not participate in the battle.",
        "'INV' or 'INVENTORY': Access the inventory options for the current character",
        "'L' or 'LOOK': Describe the current character's room again and reassess their current status.",
        "'STAT' or 'STATS': Examine each of the current character's statistics.",
        "'P' or 'PARTY': Show a list of all player-controlled characters, along with their corresponding number, which can be used to change the current character.",
        "{0-9}: Change control to the corresponding character.",
        "You will also notice that many rooms contain keywords in ALL CAPS that represent a feature of the room that the player can interact with. Simply entering the name of these ALL CAPITALIZED keywords will allow you to fully interact with that feature."
    ]

    #endregion

    #region Print intro:
    print("")
    intro_str_list = [
        "Welcome to 'Sector 17', an interactive, science-fiction and horror story generator. Hopefully you enjoy a good read!",
        "In order to survive this scenario, you'll need to use your wits, utilize your party members' strengths, and mitigate their weaknesses.",
        "The ultimate goal is to either escape from section 17 with every party member, or utterly destroy the alien threat that has infested this sector of space.",
        "There are multiple endings and you'll be awarded points at the end of each run depending upon how much you accomplish.",
        "A word of advice: while it is technically possible to beat the game with any party combination, a party that includes a diverse set of skills will serve you best. That being said, there is no 'perfect party,' and it is useful to play with every character to learn their strengths and weaknesses--so don't bother deliberating over your first party composition too much.",
        "Good luck!",
    ]

    for i in intro_str_list:
        intro_line = textwrap.fill(i, TOTAL_LINE_W)
        print(intro_line)
        print("")

    any_key = input("Press enter to travel to Sector 17.")
    print("")

    statis_chamber_str_list = [
        "Klaxons blare deep within the metal womb of the spindle-ship 'K.C. Niffy,' adrift somewhere within the endless sea of stars...",
        "... Yet outside the vessel, in the vacuum of the void, there is only silence.",
        "We move closer toward the starship, a jagged splinter tumbling through the abyss...",
        "... Moving closer and closer still...",
        "... Moving through layers of steel hull, insulation, electronics, metal grating...",
        "... Emerging from a ceiling fan into an oval-shaped room, dimly lit with banks of red emergency lighting, recessed within the floor. Here the sound of the klaxons is deafening. The walls of the room have nearly been torn asunder and are shaking from the impact of some distant explosion. Wrent paneling and torn steel reveal the steaming and sparking guts of the ship's infrastructure.",
        "Near the center of the room, raised upon a wide dais, row upon row of stasis pods are gleaming in the gloom like white pearls with red bellies, beckoning us closer.",
        "Above the stasis pods, through glass casings filmed with frost, one can see that most of the sleepers wear placid expressions, totally at ease within their pale cribs, indifferent to the apparent chaos raging all around them.",
        "Three of the occupants, however, are stirring. They seem convinced that these glass cages with their white velvet cushions will not become their coffins. Sweat beads upon their brows. Their features twist and contort, fighting against the ephemeral pull of some discontented dream.",
        "In the shadow of the eerie purgatory light, it is difficult to make out their faces.",
        "Who among them will wake, shaken by the last gasp of a failing power system?...",
        "... And who among them will slip deeper still from slumber, into death?"
    ]

    for i in statis_chamber_str_list:
        intro_line = textwrap.fill(i, TOTAL_LINE_W)
        print(intro_line)
        print("")

    any_key = input("Press enter to peruse the stasis chamber.")
    print("")

    #endregion

    while game_end == False:

        #Listen for pygame events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_end = True
                    pygame.quit()
                    sys.exit()

        # Draw everything to your smaller, pixel-art game_surface:
        game_surface.fill((0, 0, 0))  # Clear screen to black

        #region ALL DRAWING CODE:

        # - Draw backgrounds
        # - Draw sprites
        # - Draw UI

        #endregion

        # Scale surface up to fullscreen - must be called AFTER all of our draw code:
        scaled_surface = pygame.transform.scale(game_surface, (screen_width, screen_height))
        screen.blit(scaled_surface, (0, 0))

        #region Choose chars game state:

        if cur_game_state == GAME_STATE_CHOOSE_CHARS:

            print("Enter a character's number to add them to your party, or type '*' followed by a character's number to learn more about them.")
            print("You can revoke your most recent selection at any time by entering 'BACK'.")
            print("You can also enter '?' at any point during the game to learn more about stats, commands, and the game in general.")
            print("Note: All commands in this game are case insensitive.")
            print("")
            for i in total_chars_stats_list:
                char_stats_str = textwrap.fill(i,TOTAL_LINE_W)
                print(char_stats_str)
                print("")

            user_input = input("Who will awaken? >").upper()
            print("")

            if user_input == "BACK":
                if len(pc_char_list) > 0:
                    #Remove from list:
                    removed_char_inst = pc_char_list.pop()
                    #Remove from corresponding team list in room obj:
                    removed_char_inst.add_or_remove_char_from_room_list(location_grid_niffy[removed_char_inst.cur_grid_y][removed_char_inst.cur_grid_x],False)
                    print(f"{removed_char_inst.name} has been removed from the party.")
                    print("")
                    del removed_char_inst
            else:
                print_bio = False
                char_select_str = ""

                if user_input.startswith("*"):
                    print_bio = True
                    char_select_str = user_input[1:]  # Everything after the "*"
                else:
                    char_select_str = user_input

                valid_char = False

                try:
                    int_char = int(char_select_str)
                    if int_char >= 0 and int_char < ENUM_CHARACTER_SOLDIER+1:
                        if print_bio == False:
                            duplicate_found = False
                            for i in range(0,len(pc_char_list)):
                                char_inst = pc_char_list[i]
                                if char_inst.char_type_enum == int_char:
                                    valid_char = False
                                    duplicate_found = True
                                    print("You've already added that character to your party, try again.\n")
                                    break
                            if duplicate_found == False:
                                valid_char = True
                        else:
                            valid_char = True
                    else:
                        print("That is not a valid character number.")
                except ValueError:
                    print("You must enter a valid integer.")

                if valid_char == True:
                    if print_bio:
                        cur_game_state = GAME_STATE_PRINT_BIO
                    else:
                        #Add to chosen_pc_chars_list, then check start condition
                        pc_char_list.append(Character(int_char,origin_grid_x,origin_grid_y,location_grid_niffy,ENUM_CHAR_TEAM_PC, True)) #instantiate char
                        print(f"You have added {pc_char_list[len(pc_char_list)-1].name} to the party.")
                        print("")
                        if len(pc_char_list) == 3:
                            print("... Three silhouettes shamble from the stasis pods in the light of the bloody gloaming, the room quaking all around them...")
                            print("")
                            print("Through bleary eyes, you find yourself in the middle of a chaotic scene:")
                            print("")
                            #Define cur_char:
                            cur_char = pc_char_list[0]
                            #DEBUG ONLY: Add more chars and enemies:
                            debug_features = False
                            if debug_features:
                                #West hall:
                                pc_char_list.append(Character(ENUM_CHARACTER_OGRE,origin_grid_x-1,origin_grid_y,location_grid_niffy,ENUM_CHAR_TEAM_PC,True))
                                enemy_char_list.append(
                                    Character(ENUM_CHARACTER_ENEMY_SKITTERING_LARVA, origin_grid_x - 1, origin_grid_y, location_grid_niffy,
                                              ENUM_CHAR_TEAM_ENEMY, True))
                                enemy_char_list.append(
                                    Character(ENUM_CHARACTER_ENEMY_SPINED_SPITTER, origin_grid_x + 1, origin_grid_y,
                                              location_grid_niffy,
                                              ENUM_CHAR_TEAM_ENEMY, True))
                                #East hall:
                                pc_char_list.append(
                                    Character(ENUM_CHARACTER_CRIMINAL, origin_grid_x + 1, origin_grid_y, location_grid_niffy,
                                              ENUM_CHAR_TEAM_PC, True))
                                enemy_char_list.append(
                                    Character(ENUM_CHARACTER_ENEMY_SKITTERING_LARVA, origin_grid_x + 1, origin_grid_y,
                                              location_grid_niffy,
                                              ENUM_CHAR_TEAM_ENEMY, True))
                                enemy_char_list.append(
                                    Character(ENUM_CHARACTER_ENEMY_SPINED_SPITTER, origin_grid_x + 1, origin_grid_y,
                                              location_grid_niffy,
                                              ENUM_CHAR_TEAM_ENEMY, True))

                            #change game state to initialize new turn, if applicable:
                            enter_combat_boolean = check_combat_start(pc_char_list)

                            if enter_combat_boolean:
                                cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                            else:
                                cur_game_state = GAME_STATE_MAIN

        #endregion for game_state == choose_chars

        #region game_state == print_char_bio:

        elif cur_game_state == GAME_STATE_PRINT_BIO:
            #Manually separate string by '\n' escape key into list elements:
            lines_list = total_chars_bio_list[int_char].split('\n\n')
            #Then wrap each each string element within the lines_list if it exceeds the TOTAL_LINE_W by using textwrap.fill which adds \n where appropriate
            wrapped_lines = [textwrap.fill(line, TOTAL_LINE_W) for line in lines_list]
            #Then join the string elements again into a single string, wherever '\n' is found:
            bio_str = '\n\n'.join(wrapped_lines)

            #Finally, print:
            print(bio_str)
            print("")
            any_key = input("Press enter to return to the character selection screen.")

            #Return to character selection:
            cur_game_state = GAME_STATE_CHOOSE_CHARS

        #endregion

        #region game_state == INITIALIZING NEW TURN

        elif cur_game_state == GAME_STATE_INITIALIZING_NEW_TURN:

            #Just a failsafe for memory garbage collection:
            opportunity_attacker_id = -1
            overwatch_target_id = -1
            overwatch_attacker_id = -1

            #Iterate through every pc char, if they have already participated in a battle and there's enemies in their
            #room, then start a battle:
            combat_begun = False
            for i in range(0,len(pc_char_list)):
                #Define pc_char vars:
                new_turn_cur_char_index = i #Where else is this used? Remove?
                pc_inst = pc_char_list[i]
                occupying_grid_id = pc_inst.cur_grid
                cur_combat_room_id = occupying_grid_id[pc_inst.cur_grid_y][pc_inst.cur_grid_x]

                if (isinstance(cur_combat_room_id.enemies_in_room_list,list)
                and len(cur_combat_room_id.enemies_in_room_list) > 0):
                    if pc_inst.participated_in_new_turn_battle == False:
                        #Print discovery string:
                        combat_discovery_str = wrap_str(f"There are enemies in the {cur_combat_room_id.room_name} that have discovered {pc_inst.name}! You have no choice now--you have to fight to save yourself!",TOTAL_LINE_W,False)
                        print(combat_discovery_str+"\n")

                        #Setup combat_initiative_list:
                        combat_initiative_list = -1
                        combat_initiative_list = []

                        # This ALSO sets Character.participated_in_new_turn_battle == TRUE!
                        combat_initiative_list = fill_combat_initiative_list(cur_combat_room_id)

                        #Organize by speed + random_int(0,6)
                        combat_initiative_list = organize_initiative_list(combat_initiative_list)

                        #Create our combat_rank_list:
                        if isinstance(combat_rank_list,list) == False:
                            combat_rank_list = []
                        else:
                            combat_rank_list.clear()

                        #organize it by starting positions:
                        combat_rank_list = organize_combat_rank_list(combat_initiative_list)

                        #Go through combat_initiative_list, assign the Character.cur_combat_rank var as starting_combat_rank
                        for i in range(0,len(combat_initiative_list)):
                            if combat_initiative_list[i].char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                combat_initiative_list[i].cur_combat_rank = 0
                            else:
                                combat_initiative_list[i].cur_combat_rank = ENUM_RANK_PC_FAR

                        #Assign our global cur_combat_char as the first pc char we find, as we'll be moving into prep_combat game_state
                        for i in range(0,len(combat_initiative_list)):
                            if combat_initiative_list[i].char_team_enum == ENUM_CHAR_TEAM_PC:
                                cur_combat_char = combat_initiative_list[i]
                                break

                        #Send us to prep combat to give the player a chance to use abilities, change gear, use items, or flee:
                        cur_game_state = GAME_STATE_PREP_COMBAT
                        cur_combat_round = 0
                        combat_begun = True
                        prep_combat_boolean = True

                        break

            #If we completely get through this for loop without a battle being initiated, always set cur_char to first
            #pc_inst in pc_char_list, then change game state:
            if combat_begun == False:
                #Assign cur char as the first alive and conscious we find in our pc_list:
                cur_char = return_first_alive_pc(pc_char_list)

                prev_game_state = GAME_STATE_MAIN #We'll use this prev_game_state to return to either here or the main game state after combat is concluded
                cur_game_state = GAME_STATE_MAIN

        #endregion

        #region GAME_STATE_PREP_COMBAT
        elif cur_game_state == GAME_STATE_PREP_COMBAT:
            #Reset:
            choose_ability_boolean = False
            pc_fleeing_combat_boolean = False
            pc_collapsed_from_dot = False
            using_ability_boolean = False
            choose_weapon_boolean = False

            #Print battlefield
            prep_phase_summary = wrap_str(
                f"Preparation phase of combat has begun. Here you can use abilities that don't target the enemy; change out your gear; or decide to flee. ",
                TOTAL_LINE_W, False)
            print(prep_phase_summary)
            print("")
            battlefield_summary_str = wrap_str("If you imagine a center-line separating your half of the room from the enemy's half at the start of the battle, this is what you see:",TOTAL_LINE_W,False)
            print(battlefield_summary_str)
            print_combat_ranks(combat_rank_list)
            print("")
            #print char status combat summation:
            print(return_combat_char_summary_string(cur_combat_char,ammo_total))

            #Build playable char list - these are the only chars we can access in prep combat phase:
            playable_char_combat_list = []
            for i in range(0,len(combat_initiative_list)):
                if combat_initiative_list[i].char_team_enum == ENUM_CHAR_TEAM_PC:
                    playable_char_combat_list.append(combat_initiative_list[i])

            print("")
            #Print char summary:
            char_options_str = wrap_str(
                f"Prepare for combat. You have the following commands available to you: 'S'TART COMBAT, 'ABIL'ITY, 'I'NV, '<' or '>' to iterate through the playable characters, or 'R'UN",TOTAL_LINE_W, False)
            print(char_options_str)
            input_str = input("Enter a combat command now.> ").upper().strip()
            print("")

            #Goto CHOOSE_DOOR_DIR game state:
            if input_str == "R" or input_str == "RUN":
                if cur_combat_char.already_fled_this_turn_boolean == False:
                    pc_fleeing_combat_boolean = True
                    prev_game_state = GAME_STATE_PREP_COMBAT
                    cur_game_state = GAME_STATE_CHOOSE_DOOR_DIRECTION
                else:
                    retreat_str = wrap_str(f"{cur_combat_char.name} is already exhausted from running. They can't retreat again!",TOTAL_LINE_W,False)
                    print(retreat_str)
                    print("")

            #Iterate through chars:
            elif input_str == "<" or input_str == ">":
                if input_str == "<":
                    move_dir = -1
                elif input_str == ">":
                    move_dir = 1

                cur_char_index = playable_char_combat_list.index(cur_combat_char)

                cur_char_index += move_dir

                if cur_char_index < 0:
                    cur_char_index = len(playable_char_combat_list)-1
                elif cur_char_index >= len(playable_char_combat_list):
                    cur_char_index = 0

                cur_combat_char = playable_char_combat_list[cur_char_index]

            #region Goto CHOOSE_ATTACK screen:
            elif input_str == "ABIL" or input_str == "ABILITY":
                valid_combat_abil = False
                if isinstance(cur_combat_char.ability_list,list) and len(cur_combat_char.ability_list) > 0:
                    for i in range(0,len(cur_combat_char.ability_list)):
                        if cur_combat_char.ability_list[i].is_combat_abil_only_boolean == True:
                            valid_combat_abil = True
                            break
                if valid_combat_abil:
                    choose_ability_boolean = True
                    #print(f"DEBUG: ABIL option chosen, moving to GAME_STATE_COMBAT_CHOOSE_ATTACK now, choose_weapon_boolean == {choose_weapon_boolean}, choose_ability_boolean {choose_ability_boolean}.")
                    cur_game_state = GAME_STATE_COMBAT_CHOOSE_ATTACK
                else:
                    print(f"{cur_combat_char.name} has no valid combat abilities to use.\n")
            #endregion

            #Goto access inv screen:
            elif input_str == "I" or input_str == "INV" or input_str == "INVENTORY":
                cur_game_state = GAME_STATE_ACCESS_INV

            elif input_str == "S" or input_str == "START":
                #Reset vars:
                combat_begun = True
                prep_combat_boolean = False
                #Advance round:
                cur_combat_round += 1
                #Reorganize our initiative_list, as new, neutral characters could have been spawned:
                combat_initiative_list = organize_initiative_list(combat_initiative_list)
                #Assign cur_combat_char:
                cur_combat_char = combat_initiative_list[0]
                #Move to either execute action or assign command:
                if (combat_initiative_list[0].char_team_enum == ENUM_CHAR_TEAM_ENEMY or
                combat_initiative_list[0].char_team_enum == ENUM_CHAR_TEAM_NEUTRAL):
                    cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION
                else:
                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND

            else:
                print("That is an invalid command.")

        #endregion

        #region game state choose door direction
        elif cur_game_state == GAME_STATE_CHOOSE_DOOR_DIRECTION:
            if pc_fleeing_combat_boolean:
                print("Where will you flee to?\n")
                room_id = cur_combat_room_id
            else:
                print("Which door will you interact with?\n")
                room_id = cur_room_inst_id

            room_id.print_room_directions()

            if pc_fleeing_combat_boolean:
                instruction_str = wrap_str("Enter the first letter or the full word of the direction you want to flee to, or 'B'ACK to return to the previous screen. Note: you can only flee once per turn. If you flee into a room that also has enemies, you will be forced to fight them.",TOTAL_LINE_W,False)
                print(instruction_str)
                input_str = input("Enter your choice now. >").upper().strip()
                print("")
                if (input_str == "W" or input_str == "WEST" or input_str == "E" or input_str == "N" or input_str == "NORTH"
                or input_str == "S" or input_str == "SOUTH"):
                    move_dir_x = 0
                    move_dir_y = 0
                    if input_str == "W" or input_str == "WEST":
                        move_dir_x = -1
                        input_str = "WEST"
                    elif input_str == "E" or input_str == "EAST":
                        move_dir_x = 1
                        input_str = "EAST"
                    elif input_str == "S" or input_str == "SOUTH":
                        move_dir_y = 1
                        input_str = "SOUTH"
                    elif input_str == "N" or input_str == "NORTH":
                        move_dir_y = -1
                        input_str = "NORTH"

                    #Make sure that's a valid direction to travel to:
                    if input_str in room_id.directional_dict:
                        if return_valid_door_dir(room_id,input_str) == True:
                            #Define fleeing vars
                            fleeing_pc_id = cur_combat_char
                            fleeing_pc_id.fleeing_dir_x = move_dir_x
                            fleeing_pc_id.fleeing_dir_y = move_dir_y
                            fleeing_pc_id.flee_directional_str = input_str


                            #Check for enemies in current rank position:
                            ran_enemy_list = []
                            rank_pos = cur_combat_char.cur_combat_rank
                            for nested_i in range(0,len(combat_rank_list[rank_pos])):
                                char_id = combat_rank_list[rank_pos][nested_i]
                                if char_id.char_team_enum == ENUM_CHAR_TEAM_ENEMY and char_id.stun_count <= 0:
                                    ran_enemy_list.append(char_id)

                            #Choose random enemy
                            if len(ran_enemy_list) > 0:
                                ran_ind = random.randint(0,len(ran_enemy_list)-1)
                                opportunity_attacker_id = ran_enemy_list[ran_ind]
                                opportunity_attacker_id.is_opportunity_attacker_boolean = True #Is reset to false in advance_cur_char and at the end of execute action

                                #print(f"DEBUG: CHARACTER INITIATED FLEEING: fleeing_pc_id: {fleeing_pc_id.name}, opportunity_attacker_id = {opportunity_attacker_id.name}")

                                #Choose weapon with max damage:
                                random.shuffle(opportunity_attacker_id.ability_list)
                                opportunity_attacker_id.ability_list.sort(key=attrgetter('dmg_max'), reverse=True)
                                opportunity_attacker_id.chosen_weapon = opportunity_attacker_id.ability_list[0]

                                #Print status:
                                flee_str = wrap_str(f"{fleeing_pc_id.name} is attempting to flee {input_str}, but they are engaged in melee with an enemy! {opportunity_attacker_id.name} has an opportunity to attack...",TOTAL_LINE_W,False)
                                print(flee_str)
                                print("")

                                #Move to combat (we'll skip enemy AI):
                                cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION

                            #Move them right now, check for combat end, advance cur combat char:
                            else:
                                #Delete from both initiative list and combat_rank_list:
                                pc_fleeing_combat_boolean = False #Reset
                                prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)
                                execute_char_combat_flee(combat_initiative_list,combat_rank_list,cur_combat_room_id,fleeing_pc_id,False)

                                combat_concluded, enemies_won_boolean = check_combat_end_condition(cur_combat_room_id)

                                if combat_concluded:
                                    overwatch_loop_mode_enabled = False  # Always reset
                                    if not enemies_won_boolean:
                                        prematurely_end_overwatch_mode = True
                                        combat_begun = False  # reset
                                        # Reset, clear our combat lists:
                                        combat_initiative_list = -1
                                        combat_rank_list = -1
                                        overwatch_attacker_list = -1
                                        cur_combat_char = -1

                                        # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                        cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                        continue_key = input(
                                            "The battle is over! Every enemy has fled or been slain. Press enter to continue.")
                                        print("")
                                    elif enemies_won_boolean:
                                        remove_team_chars_from_room(cur_combat_room_id, ENUM_CHAR_TEAM_NEUTRAL)
                                        print(
                                            "The battle is over! The enemies in this room cavort and slaver in the wake of their victory...\n")
                                        if len(pc_char_list) <= 0:
                                            print(
                                                "Every playable character is dead--you have lost! Hopefully you have learned from your experiences...")
                                            game_end = True
                                        else:
                                            prematurely_end_overwatch_mode = True
                                            # Reset, clear our combat lists:
                                            combat_initiative_list = -1
                                            combat_rank_list = -1
                                            overwatch_attacker_list = -1
                                            attacking_char = -1
                                            defending_char = -1
                                            cur_combat_char = -1
                                            filtered_enemy_list = -1
                                            # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                            cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                            continue_key = input(
                                                "Press enter to continue.")
                                            print("")
                                #either advance cur_Char (if our previous game_state == ASSIGN_COMMAND; or simply return to
                                #the prev game state:
                                elif not combat_concluded:
                                    #This char has used their combat turn.
                                    if prev_game_state == GAME_STATE_COMBAT_ASSIGN_COMMAND:
                                        cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                            cur_combat_char,
                                            combat_initiative_list,
                                            cur_combat_room_id,
                                            cur_combat_round,
                                            prev_cur_combat_char_index,
                                            f"moving away from GAME_STATE_CHOOSE_DOOR_DIRECTION game state, cur_combat_char: {cur_combat_char.name} was able to flee immediately without provoking an opportunity attack, advancing cur_char: combat has NOT concluded and this character has fled. Their prev_cur_combat_char_index var == {prev_cur_combat_char_index}.")

                                        #Await player input:
                                        continue_key = input(
                                            "Press enter to continue to the next combatant in the initiative queue.")
                                        print("")
                                    #Simply change cur_char and return to our previous screen
                                    else:
                                        cur_combat_char = return_first_team_member_in_list(combat_initiative_list,ENUM_CHAR_TEAM_PC)
                                        if cur_combat_char != -1:
                                            cur_game_state = prev_game_state
                                        else:
                                            print("DEBUG: After char fled and was removed from combat lists, combat_concluded == False but we couldn't find another char with the TEAM_PC in our initiative_list... Something went wrong.")

                        else:
                            print("You must choose a valid direction that is accessible. Try again.")
                    else:
                        print("You must choose a valid direction that is accessible. Try again.")
                elif input_str == "B" or input_str == "BACK":
                    cur_game_state = prev_game_state
                    pc_fleeing_combat_boolean = False
                else:
                    print("You must choose a valid direction that is accessible. Try again.")
        #endregion

        #region GAME_STATE_COMBAT_ASSIGN_COMMAND GAME STATE
        elif cur_game_state == GAME_STATE_COMBAT_ASSIGN_COMMAND:

            if cur_combat_char.unconscious_boolean:
                plural_str = ""
                if cur_combat_char.unconscious_count != 1:
                    plural_str = "s"
                status_str = wrap_str(f"**... {cur_combat_char.name} is unconscious with {cur_combat_char.hp_cur} hit points. They have {cur_combat_char.unconscious_count-1} turn{plural_str} left to be healed, otherwise they will die...** \n",TOTAL_LINE_W,False) #We subtract 1 here b.c they lose -1 and die on the same turn they reach 0, so it's more accurate to that the full turns they have remaining == unconscious_count-1
                print(status_str)
                print("")
            #Mutually exclusive; I don't want to know if a character is stunned if they're also unconscious:
            elif cur_combat_char.stun_count > 0:
                #Only print this if they are not about to recover this same turn:
                if cur_combat_char.stun_count-1 > 0:
                    plural_str = ""
                    if cur_combat_char.stun_count > 1:
                        plural_str = "s"
                    print(f"**...{cur_combat_char.name} is stunned for {cur_combat_char.stun_count-1} more turn{plural_str}!...**\n")

            #Reset
            pc_collapsed_from_dot = False
            using_ability_boolean = False
            combat_concluded_boolean = False
            pc_fleeing_combat_boolean = False

            # Store in case the cur_char dies as a result of DOT damage:
            prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)

            #region Resolve DOT effects:
            #This ALSO catches the use-case where the pc is simply unconscious, but doesn't die from it and the game doesn't end.
            if cur_combat_char.resolve_dot_effects_boolean:
                #Reset
                cur_combat_char.resolve_dot_effects_boolean = False
                #Resolve dot:
                pc_collapsed_from_dot = resolve_dot_effects(cur_combat_char)

                if pc_collapsed_from_dot:

                    #Store prev_index before we potentially kill off our pc:
                    prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)
                    #Delete pc if they are truly dead (not just unconscious):
                    if cur_combat_char.hp_cur <= 0 and cur_combat_char.completely_dead_boolean:
                        # Destroy the cur_combat_char pc by removing them from all applicable lists:
                        #print(f"Debug: before entering destroy_combatant_inst: the cur_combat_char's index in combat_initiative_list is : {combat_initiative_list.index(cur_combat_char)}.")

                        #Drop their gear; while it may seem extraneous to check their team, the game is always growing so its not bad practice:
                        if cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_PC:
                            drop_all_pc_inventory(cur_combat_char,cur_combat_room_id)

                        combat_rank_list, combat_initiative_list, pc_char_list, enemy_char_list, neutral_char_list = destroy_combatant_inst(
                            combat_rank_list,
                            combat_initiative_list,
                            cur_combat_char,
                            pc_char_list, enemy_char_list, neutral_char_list)

                        combat_concluded_boolean, enemies_won_boolean = check_combat_end_condition(cur_combat_room_id)

                        if combat_concluded_boolean:
                            overwatch_loop_mode_enabled = False  # Always reset
                            if not enemies_won_boolean:
                                prematurely_end_overwatch_mode = True
                                combat_begun = False  # reset
                                #Reset, clear our combat lists:
                                combat_initiative_list = -1
                                combat_rank_list = -1
                                overwatch_attacker_list = -1
                                cur_combat_char = -1

                                #Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                continue_key = input("The battle is over! Every enemy has fled or been slain. Press enter to continue.")
                                print("")
                            elif enemies_won_boolean:
                                remove_team_chars_from_room(cur_combat_room_id, ENUM_CHAR_TEAM_NEUTRAL)
                                print(
                                    "The battle is over! The enemies in this room slaver and cavort in the wake of their victory...\n")
                                if len(pc_char_list) <= 0:
                                    print("Every playable character is dead--you have lost! Hopefully you have learned from your experiences...")
                                    game_end = True
                                else:
                                    prematurely_end_overwatch_mode = True
                                    # Reset, clear our combat lists:
                                    combat_initiative_list = -1
                                    combat_rank_list = -1
                                    overwatch_attacker_list = -1
                                    attacking_char = -1
                                    defending_char = -1
                                    cur_combat_char = -1
                                    filtered_enemy_list = -1
                                    # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                    cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                    continue_key = input(
                                        "Press enter to continue.")
                                    print("")
            #endregion

            #Don't care whether DOT effects resolved or not, don't care if the char passed out from DOT effects.
            # All that matters here is if the combat is still running, and this char is either dead, unconscious, or stunned,
            # then we need to advance the cur_char and game_state--it's that fucking simple.And if they died and
            # combat didn't conclude, then they've been removed from memory--but either way we stored their
            # prev_cur_combat_char_index var before the DOT code block, before they were removed from memory:
            if (combat_concluded_boolean == False and
            (cur_combat_char.unconscious_boolean or cur_combat_char.completely_dead_boolean or cur_combat_char.stun_count > 0)):

                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                    cur_combat_char,
                    combat_initiative_list,
                    cur_combat_room_id,
                    cur_combat_round,
                    prev_cur_combat_char_index,
                    f"moving away from ASSIGN_COMMANDS game state, advancing cur_char and game state away from char: {cur_combat_char.name}: combat has NOT concluded and this character is either unconscious or dead. In either case, the combat hasn't ended and we need to advance the cur_char and game_state; we stored their prev_cur_combat_char_index var before this char resolved any dot effects. They prev_cur_combat_char_index var == {prev_cur_combat_char_index}.")

                #Pause here so the player isn't potentially bombarded with a wall of text as we iterate through unconscious characters:
                continue_key = input("Press enter to continue to the next combatant in the initiative queue.")
                print("")

            if (cur_game_state == GAME_STATE_COMBAT_ASSIGN_COMMAND and cur_combat_char.completely_dead_boolean == False
            and cur_combat_char.unconscious_boolean == False and cur_combat_char.stun_count <= 0):
                #Reset vars for GAME_STATE_COMBAT_CHOOSE_ATTACK game state:
                choose_weapon_boolean = False
                choose_ability_boolean = False
                attempting_overwatch_boolean = False # only used for choose weapon logic
                attempting_suppress_boolean = False #Defunct

                #Check overwatch and suppress availability:
                overwatch_avail_boolean = return_overwatch_or_suppress_capable(cur_combat_char,True)

                battlefield_summary_str = wrap_str(f"Round {cur_combat_round} of the battle is underway. If you imagine a center-line separating your half of the room from the enemy's half at the start of the battle, this is what you see:",TOTAL_LINE_W,False)
                print(battlefield_summary_str)
                print_combat_ranks(combat_rank_list)
                print("")

                print(return_combat_char_summary_string(cur_combat_char,ammo_total))

                overwatch_str = ""
                suppress_str = ""
                if overwatch_avail_boolean:
                    overwatch_str = ", 'O'VERWATCH"

                char_options_str = wrap_str(f"You have the following commands available to you: 'F'IGHT, 'A'DVANCE, 'W'ITHDRAW, 'I'NV, 'D'ODGE, 'R'UN, 'ABIL'ITY', 'V'IEW TURN ORDER{overwatch_str}{suppress_str}",TOTAL_LINE_W,False)
                print(char_options_str)
                input_str = input("Enter a combat command now.> ").upper().strip()
                print("")

                #region Choose ability:
                if input_str == "ABIL" or input_str == "ABILITY":
                    valid_combat_abil = False
                    if isinstance(cur_combat_char.ability_list, list) and len(cur_combat_char.ability_list) > 0:
                        for i in range(0, len(cur_combat_char.ability_list)):
                            if cur_combat_char.ability_list[i].is_combat_abil_only_boolean == True:
                                valid_combat_abil = True
                                break
                    if valid_combat_abil:
                        cur_game_state = GAME_STATE_COMBAT_CHOOSE_ATTACK
                        choose_ability_boolean = True
                    else:
                        print(f"{cur_combat_char.name} has no valid combat abilities.\n")
                #endregion

                #region FIGHT logic
                elif input_str == "F" or input_str == "FIGHT":
                    cur_game_state = GAME_STATE_COMBAT_CHOOSE_ATTACK
                    choose_weapon_boolean = True
                #endregion

                #region Advance or Withdraw logic:
                elif input_str == "A" or input_str == "ADVANCE" or input_str == "W" or input_str == "WITHDRAW":
                    valid_advance = False
                    if input_str == "A" or input_str == "ADVANCE":
                        move_dir = -1
                    if input_str == "W" or input_str == "WITHDRAW":
                        move_dir = 1

                    if cur_combat_char.cur_combat_rank + move_dir >= 0 and cur_combat_char.cur_combat_rank + move_dir < len(combat_rank_list):
                        valid_advance = True

                    if valid_advance:
                        #Forbid movement if suppressed:
                        if cur_combat_char.suppressed_count <= 0:
                            #Add to next rank in combat_rank_list
                            combat_rank_list = advance_or_withdraw_char(move_dir,combat_rank_list,cur_combat_char)

                            #Await player input before launching into a potential overwatch_loop mode:
                            continue_key = input("Press enter to continue to the next character in the initiative queue.")
                            print("")

                            # Check to see if moving from this rank would allow an enemy a free hit from:
                            # overwatch and melee attacks of opportunity
                                # Call build_overwatch_list:
                            overwatch_attacker_list = build_overwatch_list(cur_combat_char, combat_initiative_list)

                            if len(overwatch_attacker_list) > 0:
                                # Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                if len(overwatch_attacker_list) > 0:
                                    cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                    cur_overwatch_attacker_index = 0
                                    overwatch_loop_mode_enabled = True
                                    overwatch_target_id = cur_combat_char
                                    print(f"**{cur_combat_char.name} has been targeted for overwatch fire!**\n")
                                    #print(
                                        #f"DEBUG:Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")
                            else:
                                # Advance cur_combat_char (and possibly cur_combat_round):
                                prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)

                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(cur_combat_char,
                                                                                                                                    combat_initiative_list,
                                                                                                                                    cur_combat_room_id,
                                                                                                                                    cur_combat_round,
                                                                                                                                    prev_cur_combat_char_index,
                                                                                                                                    f"Moving away from ASSIGN_COMMANDS game state: pc_char: {cur_combat_char.name} just finished moving, moving away from this instance now; we called build_overwatch_list but overwatch_attacker_list return with a len(overwatch_attacker_list) <= 0, so we're not entering overwatch_loop and instead just advancing normally.")
                                #EOF
                        else:
                            print("You have been suppressed by enemy fire and cannot move!\n")
                    else:
                        print("You cannot move any further in that direction.")
                #endregion

                #region Dodge logic
                elif input_str == "D" or input_str == "DODGE":
                    #Apply dodge bonus boolean
                    cur_combat_char.dodge_bonus_boolean = True
                    print(f"{cur_combat_char.name} is acting defensively, and will receive +1 to their evasion stat until the start of their next turn.\n")

                    prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)

                    # Advance cur_combat_char (and possibly cur_combat_round):
                    cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                        cur_combat_char,
                        combat_initiative_list,
                        cur_combat_room_id,
                        cur_combat_round,
                        prev_cur_combat_char_index,
                        f"Moving away from ASSIGN_COMMANDS game_state: pc char: {cur_combat_char.name} just finished entering their 'dodge' action.")

                    # Await player input before continuing:
                    continue_str = input("Press enter to continue to the next combatant in the initiative queue.")
                    print("")
                #endregion

                #region Access inventory logic
                elif input_str == "I" or input_str == "INV":
                    cur_game_state = GAME_STATE_ACCESS_INV
                #endregion

                #region Overwatch logic:
                elif (input_str == "O" or input_str == "OVERWATCH") and overwatch_avail_boolean:
                    attempting_overwatch_boolean = True
                    cur_game_state = GAME_STATE_COMBAT_CHOOSE_ATTACK
                    choose_weapon_boolean = True
                #endregion

                #region VIEW TURN ORDER logic
                elif input_str == "V" or input_str == "VIEW TURN ORDER":

                    print_combat_initiative_list(combat_initiative_list,cur_combat_char)
                    print("")
                    continue_key = input("Press enter to continue.")
                    print("")
                #endregion

                #region 'RUN' logic:
                elif input_str == "R" or input_str == "RUN":
                    if cur_combat_char.already_fled_this_turn_boolean == False:
                        if cur_combat_char.cur_combat_rank == ENUM_RANK_ENEMY_FAR or cur_combat_char.cur_combat_rank == ENUM_RANK_PC_FAR:
                            prev_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
                            pc_fleeing_combat_boolean = True
                            prev_game_state = cur_game_state
                            cur_game_state = GAME_STATE_CHOOSE_DOOR_DIRECTION
                        else:
                            print("In order to flee, you must be occupying either the distant enemy position, or the distant friendly position.")
                    else:
                        retreat_str = wrap_str(
                            f"{cur_combat_char.name} is already exhausted from running. They can't retreat again!",
                            TOTAL_LINE_W, False)
                        print(retreat_str)
                        print("")
                #endregion

                else:
                    print("That is an invalid combat option, try again.")

                #endregion

        #endregion

        #region Choose attack - loads either weapon list (left hand and right hand) or ability list (all combat-usable) abilities:

        elif cur_game_state == GAME_STATE_COMBAT_CHOOSE_ATTACK:

            ar_to_use = []
            desc_str = "undefined"

            if choose_weapon_boolean:

                desc_str = "Choose equipped weapon"
                for i in range(ENUM_EQUIP_SLOT_RH,ENUM_EQUIP_SLOT_LH+1):
                    item_id = cur_combat_char.inv_list[i]
                    if isinstance(item_id,Item):
                        ar_to_use.append(item_id)
                if len(ar_to_use) == 0:
                    #Means this char has no equipped items--they'll get the option to use their fists:
                    fists_item_enum = return_fists_enum(cur_combat_char)
                    ar_to_use.append(Item(fists_item_enum))

            elif choose_ability_boolean:

                desc_str = "Choose combat ability"

                if isinstance(cur_combat_char.ability_list, list):
                    for i in range(0, len(cur_combat_char.ability_list)):
                        abil_id = cur_combat_char.ability_list[i]
                        if isinstance(abil_id, Item):
                            ar_to_use.append(abil_id)
            else:
                print("GAME_STATE_COMBAT_CHOOSE_ATTACK: neither choose_weapon_boolean or choose_abil_boolean == true, something went wrong.")

            #Print the weapon or ability name, index, along with relevant info like max_range, min-max damage
            if choose_ability_boolean:
                for i in range(0,len(ar_to_use)):
                    full_item_str = wrap_str(f"{desc_str} {i}.) {ar_to_use[i].item_name}: {ar_to_use[i].ability_cost_str} {return_item_stats_str(ar_to_use[i])}",TOTAL_LINE_W,False)
                    print(full_item_str)
            elif choose_weapon_boolean:
                for i in range(0,len(ar_to_use)):
                    full_item_str = wrap_str(f"{desc_str} {i}.) {ar_to_use[i].item_name}: {return_item_stats_str(ar_to_use[i])}",TOTAL_LINE_W,False)
                    print(full_item_str)
            print("")
            if choose_weapon_boolean:
                input_str = input("Enter the corresponding number associated with the weapon, or enter 'B' or 'BACKUP' to enter a new combat command.> ").upper().strip()
            else:
                input_str = input(
                    "Enter the corresponding number associated with the ability, or enter 'B' or 'BACKUP' to enter a new combat command.> ").upper().strip()
            print("")
            if input_str == "B" or input_str == "BACKUP":
                if not prep_combat_boolean:
                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
                elif prep_combat_boolean == True:
                    cur_game_state = GAME_STATE_PREP_COMBAT
            else:
                try:
                    input_int = int(input_str)
                    if input_int >= 0 and input_int < len(ar_to_use):
                        if ar_to_use[input_int].is_shield_boolean == False:
                            #Do a quick check to see if we have sufficient ammo to use this weapon:
                            sufficient_ammo = True
                            ammo_required = 1
                            if attempting_suppress_boolean:
                                ammo_required = 2
                            if ammo_total < ammo_required:
                                sufficient_ammo = False
                            #Insufficient ammo case - allow player to use fists instead, without unequipping all of their items:
                            if sufficient_ammo == False and ar_to_use[input_int].requires_ammo_boolean == True:
                                #You don't have enough ammunition to use that weapon! You could try equipping a different weapon, or attack with your{char specific fists}. Enter 'F' for FISTS to attack with your fists. Any other command will return you to the combat options screen.”
                                print("You don't have enough ammunition to use that weapon! You could try equipping a different weapon, or attack with your bare fists.")
                                fists_acknowledgement_str = input("Enter 'F' for 'F'ISTS to attack with your bare fists. Any other command will return you to the combat options screen.").upper().strip()
                                if fists_acknowledgement_str == "F":
                                    fists_enum = return_fists_enum(cur_combat_char)
                                    cur_combat_char.chosen_weapon = Item(fists_enum)
                                    cur_game_state = GAME_STATE_COMBAT_TARGET_RANK
                                else:
                                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
                            #Sufficient ammo case:
                            else:
                                valid_attack = True

                                #Check ability point restriction:
                                if choose_ability_boolean and cur_combat_char.ability_points_cur < ar_to_use[input_int].ability_point_cost:
                                    valid_attack = False

                                if valid_attack:
                                    if not attempting_overwatch_boolean:
                                        # Reduce ap, if applicable:
                                        if choose_ability_boolean:

                                            #Things like Torvald's shield generator, cooper's buffs/debuffs, etc.,
                                            # these things do NOT require a target:
                                            if ar_to_use[input_int].non_attack_ability_boolean == True:

                                                execute_non_attack_ability(ar_to_use[input_int],cur_combat_char,combat_initiative_list,combat_rank_list)

                                                #Use abil points
                                                cur_combat_char.ability_points_cur -= ar_to_use[input_int].ability_point_cost

                                                #Return the to ASSIGN_COMMAND
                                                if prep_combat_boolean == True:
                                                    cur_game_state = GAME_STATE_PREP_COMBAT

                                                elif ar_to_use[input_int].abil_passes_turn_boolean == False:
                                                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND

                                                #Call advance_cur_combat_char
                                                elif ar_to_use[input_int].abil_passes_turn_boolean == True and ar_to_use[input_int].use_requires_target_boolean == False:
                                                    # Advance our cur_char:
                                                    prev_cur_combat_char_index = combat_initiative_list.index(
                                                        cur_combat_char)

                                                    cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                                        cur_combat_char,
                                                        combat_initiative_list,
                                                        cur_combat_room_id,
                                                        cur_combat_round,
                                                        prev_cur_combat_char_index,
                                                        f"moving away from game_state GAME_STATE_COMBAT_CHOOSE_ATTACK: pc char: {cur_combat_char.name} just used an ability with non_attack_ability_boolean == True, and abil_passes_turn_boolean == True. It was: {ar_to_use[input_int].item_name}.")

                                                    continue_str = input(
                                                        "Press enter to continue to the next combatant in the initiative queue.")
                                                    print("")

                                            elif ar_to_use[input_int].non_attack_ability_boolean == False:

                                                #We'll simply use this ability as a weapon item and move to GAME_STATE_COMBAT_TARGET_RANK:
                                                if ar_to_use[input_int].use_requires_target_boolean == False:
                                                    if prep_combat_boolean == False:
                                                        cur_combat_char.chosen_weapon = ar_to_use[input_int]
                                                        cur_game_state = GAME_STATE_COMBAT_TARGET_RANK
                                                    else:
                                                        print("Combat has not started, you cannot yet use that weapon or ability.\n")

                                                #We'll move to USE_ITEM game state and attempt to use the item there:
                                                elif ar_to_use[input_int].use_requires_target_boolean == True:
                                                    passing_item_id = ar_to_use[input_int]
                                                    cur_game_state = GAME_STATE_USE_TARGET_ITEM
                                                    using_ability_boolean = True

                                        #Move to execute combat if this was not an ability item:
                                        elif (choose_ability_boolean == False):
                                            cur_combat_char.chosen_weapon = ar_to_use[input_int]
                                            cur_game_state = GAME_STATE_COMBAT_TARGET_RANK

                                    if attempting_overwatch_boolean:
                                        if ar_to_use[input_int].can_overwatch_boolean:
                                            cur_combat_char.chosen_weapon = ar_to_use[input_int]
                                            cur_game_state = GAME_STATE_COMBAT_TARGET_RANK
                                        else:
                                            print("This weapon does not support overwatch mode.")

                                    if attempting_suppress_boolean:
                                        if ar_to_use[input_int].can_suppress_boolean:
                                            cur_combat_char.chosen_weapon = ar_to_use[input_int]
                                            cur_combat_char.chosen_weapon.suppressive_fire_mode_enabled = False #Reset; this will be enabled when a valid rank is chosen
                                            cur_game_state = GAME_STATE_COMBAT_TARGET_RANK
                                        else:
                                            print("This weapon does not support suppressive fire mode.")
                                #Print insufficient AP:
                                elif valid_attack == False:
                                    print(f"You don't have enough ability points to use that ability.")
                        else:
                            print("You can't attack with a shield, try again.")
                    else:
                        print("You must choose a valid weapon or ability to fight with, try again.")
                except ValueError:
                    print("That is an invalid command, try again.")
        #endregion

        # region GAME_STATE_COMBAT_TARGET_RANK

        elif cur_game_state == GAME_STATE_COMBAT_TARGET_RANK:
            target_str = "attack"
            if attempting_overwatch_boolean:
                target_str = "overwatch"
            if attempting_suppress_boolean:
                target_str = "suppress"
            print(f"Choose which position to target to {target_str}:")
            print_combat_ranks(combat_rank_list,True,cur_combat_char.chosen_weapon.max_range,cur_combat_char.cur_combat_rank)
            input_str = input("Enter the corresponding number to choose a position to attack, or 'B' or 'BACKUP' to enter a new combat command.> ").upper().strip()
            print("")
            if input_str == "B" or input_str == "BACKUP":
                cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
            else:
                try:
                    input_int = int(input_str)

                    #Make sure we're within bounds of list:
                    if input_int >= 0 and input_int < len(combat_rank_list):

                        # Determine if there's even an enemy in this rank:
                        filtered_enemy_list = []
                        for i in range(0, len(combat_rank_list[input_int])):
                            if combat_rank_list[input_int][i].char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                filtered_enemy_list.append(combat_rank_list[input_int][i])

                        #If there was at least applicable enemy in this rank, or we're attempting overwatch:
                        if len(filtered_enemy_list) > 0 or attempting_overwatch_boolean:

                            #Set .targeted_rank:
                            cur_combat_char.targeted_rank = input_int

                            #Calc dist to rank:
                            dist_between_ranks = return_distance_between_ranks(cur_combat_char.cur_combat_rank,
                                                                               cur_combat_char.targeted_rank)
                            #Proceed - or not:
                            if dist_between_ranks > cur_combat_char.chosen_weapon.max_range:
                                print("That position is beyond your equipped weapon's range.")
                            else:
                                #Set char instance suppress or overwatch boolean - they are reset to false in advance_cur_combat_char()
                                if attempting_overwatch_boolean:
                                    cur_combat_char.will_overwatch_boolean = True
                                    #Define the rank they are targeting for overwatch:
                                    cur_combat_char.overwatch_rank = cur_combat_char.targeted_rank
                                    #Print action message:
                                    overwatch_str = wrap_str(f"{cur_combat_char.name} has carefully aimed their {cur_combat_char.chosen_weapon.item_name} at rank position {cur_combat_char.overwatch_rank}, and is patiently waiting for any enemy to move into this rank...\n",TOTAL_LINE_W,False)
                                    print(overwatch_str)
                                    print("")

                                    #Advance our cur_char:
                                    prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)
                                    cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                        cur_combat_char,
                                        combat_initiative_list,
                                        cur_combat_room_id,
                                        cur_combat_round,
                                        prev_cur_combat_char_index,
                                        f"moving away from game_state TARGET_RANK: pc char: {cur_combat_char.name} just successfully targeted a rank with overwatch.")

                                    continue_str = input("Press enter to continue to the next combatant in the initiative queue.")
                                    print("")

                                elif attempting_suppress_boolean:
                                    cur_combat_char.will_suppress_boolean = True
                                    # Print action message:
                                    overwatch_str = wrap_str(
                                        f"**{cur_combat_char.name} has decided to use SUPPRESSIVE FIRE. They will consume twice the amount of ammunition and suffer a {ENUM_SUPPRESSIVE_FIRE_ACCURACY_DEBUFF} accuracy penalty, but damaged enemies have a chance to become suppressed that is equal to 100% - the defender's suppression resistence. Suppressed units can't withdraw or advance, and suffer -2 speed and -2 evasion for one turn.**\n",
                                        TOTAL_LINE_W, False)
                                    print(overwatch_str)
                                    print("")
                                    cur_combat_char.chosen_weapon.suppressive_fire_mode_enabled = True #This is reset to false just after a pc chooses a weapon with suppressive fire capability; enemies automatically have their items created with this boolean var on, and never set it to false.
                                    cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION

                                #Move to execute action:
                                else:
                                    #Reduce AP, if applicable:
                                    if choose_ability_boolean:
                                        cur_combat_char.ability_points_cur -= cur_combat_char.chosen_weapon.ability_point_cost
                                        if cur_combat_char.chosen_weapon.item_enum == ENUM_ITEM_TASER:
                                            print("'TASER! TASER! TASER!'\n")
                                    #Move to fight phase:
                                    cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION
                        else:
                            print("There are no valid enemy targets in this position to attack, try again.")
                    else:
                        print("That is an invalid position to target.")
                except ValueError:
                    print("That is an invalid command.")

        # endregion

        # region GAME_STATE_COMBAT_EXECUTE_ACTION
        elif cur_game_state == GAME_STATE_COMBAT_EXECUTE_ACTION:

            char_killed_from_dot = False

            #Don't resolve DOT if we're in overwatch loop mode or a pc is fleeing combat - in the latter case,
            # they would have already had their DOT effects resolved at the start of their turn, in ASSIGN_COMMAND
            if overwatch_loop_mode_enabled == False and pc_fleeing_combat_boolean == False:
                #Define attacking char
                attacking_char = cur_combat_char

                if cur_combat_char.unconscious_boolean:
                    print(
                        f"Debug: {cur_combat_char.name} is unconscious--this should never be the case. Unconscious pcs won't arrive here, and enemies and neutrals are killed instantly. \n")

                #region Resolve DOT - Chars only receive DOT damage if we're not in overwatch mode:
                if cur_combat_char.resolve_dot_effects_boolean:
                    # Reset
                    cur_combat_char.resolve_dot_effects_boolean = False
                    # Resolve dot:
                    char_killed_from_dot = resolve_dot_effects(cur_combat_char)

                    if char_killed_from_dot:
                        # Store prev_index before we potentially kill off our pc:
                        prev_cur_combat_char_index = combat_initiative_list.index(cur_combat_char)

                        # Delete pc if they are truly dead (not just unconscious):
                        remove_from_memory_boolean = False
                        if (cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_PC and cur_combat_char.hp_cur <= 0 and
                                cur_combat_char.completely_dead_boolean):
                            remove_from_memory_boolean = True
                        if (cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY or
                                cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL):
                            remove_from_memory_boolean = True

                        #Destroy char instance, advance to next char inst in combat_init_list:
                        if remove_from_memory_boolean:

                            #Drop all this char's gear:
                            if cur_combat_char.char_team_enum == ENUM_CHAR_TEAM_PC:
                                drop_all_pc_inventory(cur_combat_char,cur_combat_room_id)

                            #If it was a lumbering carrier that just died from DOT, have them spawn larva:
                            combat_initiative_list,combat_rank_list = spawn_combat_minion(cur_combat_char,combat_initiative_list,combat_rank_list,True)

                            # Destroy the defender by removing them from all applicable lists:
                            #print(
                                #f"Debug: before entering destroy_combatant_inst: the cur_combat_char's index in combat_initiative_list is : {combat_initiative_list.index(cur_combat_char)}.")

                            combat_rank_list, combat_initiative_list, pc_char_list, enemy_char_list, neutral_char_list = destroy_combatant_inst(
                                combat_rank_list,
                                combat_initiative_list,
                                cur_combat_char,
                                pc_char_list, enemy_char_list, neutral_char_list)

                            #Region check combat end state:
                            combat_concluded_boolean, enemies_won_boolean = check_combat_end_condition(cur_combat_room_id)

                            if combat_concluded_boolean:
                                overwatch_loop_mode_enabled = False  # Always reset
                                if enemies_won_boolean == False:
                                    prematurely_end_overwatch_mode = True
                                    # Reset, clear our combat lists:
                                    combat_initiative_list = -1
                                    combat_rank_list = -1
                                    overwatch_attacker_list = -1
                                    attacking_char = -1
                                    defending_char = -1
                                    cur_combat_char = -1
                                    filtered_enemy_list = -1
                                    # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                    cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                    continue_key = input(
                                        "The battle is over! Every enemy has fled or been slain. Press enter to continue.")
                                    print("")
                                elif enemies_won_boolean:
                                    remove_team_chars_from_room(cur_combat_room_id, ENUM_CHAR_TEAM_NEUTRAL)
                                    print(
                                        "The battle is over! The enemies in this room cavort and slaver in the wake of their victory...\n")
                                    if len(pc_char_list) <= 0:
                                        print(
                                            "Every playable character has died--you have lost! Hopefully you learned a thing or two from your experiences...")
                                        game_end = True
                                    else:
                                        #Go through our cur_combat_room_id and remove neutral Characters
                                        # (it's assumed they all die if there's no pcs there to control/protect them)
                                        remove_team_chars_from_room(cur_combat_room_id,ENUM_CHAR_TEAM_NEUTRAL)

                                        cur_combat_room_id = -1
                                        prematurely_end_overwatch_mode = True
                                        # Reset, clear our combat lists:
                                        combat_initiative_list = -1
                                        combat_rank_list = -1
                                        overwatch_attacker_list = -1
                                        attacking_char = -1
                                        defending_char = -1
                                        cur_combat_char = -1
                                        filtered_enemy_list = -1
                                        # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                        cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                        continue_key = input(
                                            "Press enter to continue.")
                                        print("")

                            #Simply advance char:
                            elif not combat_concluded_boolean:
                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    cur_combat_char,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,
                                    f"Moving from GAME_STATE_COMBAT_EXECUTE_ACTION, enemy or neutral AI with RANGED_AI preference: moving away from char: {cur_combat_char.name}")

                            #endregion
                #endregion

            elif overwatch_loop_mode_enabled and pc_fleeing_combat_boolean == False:
                attacking_char = overwatch_attacker_id
                defending_char = overwatch_target_id

            if pc_fleeing_combat_boolean:
                attacking_char = opportunity_attacker_id
                defending_char = fleeing_pc_id
                attacking_char.enemy_ai_fight_boolean = True
                print(f"DEBUG: CHARACTER ATTEMPTING TO FLEE BUT ENEMY GETS OPOPRTUNIY ATTACK: fleeing_pc_id: {defending_char.name}, attacking_char == {attacking_char.name}")

            # Check stunned print status, advance to next character
            # Enemies and neutrals will never be unconscious or have the 'dead completely' status because they're either
            # killed instantly in combat or removed from memory after resolve_dot_effects indicates that they died;
            # but enemies can be stunned. Also, if an enemy were to have died from DOT above, we would have caught it
            # already and moved on.
            if char_killed_from_dot == False and attacking_char.stun_count > 0:
                plural_str = ""
                if attacking_char.stun_count > 1:
                    plural_str = "s"
                print(f"**{attacking_char.name} is stunned for {attacking_char.stun_count} more turn{plural_str}!**\n")

                #Pause for player input before advancing to next char:
                continue_key = input("Press enter to continue to the next character in the initiative queue.")
                print("")

                #Advance game_state and cur_char:
                if pc_fleeing_combat_boolean == False:
                    prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)
                elif pc_fleeing_combat_boolean == True:
                    prev_cur_combat_char_index = combat_initiative_list.index(defending_char)

                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                    attacking_char,
                    combat_initiative_list,
                    cur_combat_room_id,
                    cur_combat_round,
                    prev_cur_combat_char_index,
                    f"Moving from GAME_STATE_COMBAT_EXECUTE_ACTION, moving away from char: {cur_combat_char.name}: This neutral or enemy character was STUNNED, so we're moving on.")

            #Only do any of this if the acting char didn't just die from dot and they're also not sunned:
            if char_killed_from_dot == False and attacking_char.stun_count <= 0:

                # We use prev_cur_combat_char_index in case the attacking_char dies during this combat,
                # in which case 'combat_initiative_list.index(cur_combat_char) would throw an error; it's used in destroy_combatant_inst()
                #debug_str = wrap_str(f"DEBUG: For line 1461: before assigning prev_cur_combat_char_index, overwatch_loop_mode_enabled = {overwatch_loop_mode_enabled}, pc_fleeing_combat_boolean = {pc_fleeing_combat_boolean}, attacking_char = {attacking_char.name}, their is_opportunity_attacker_boolean attribute = {attacking_char.is_opportunity_attacker_boolean}, and combat_initiative_list = {[Character.name for Character in combat_initiative_list]}",TOTAL_LINE_W,False)
                #print(debug_str)
                prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                #Print attacker:
                if not overwatch_loop_mode_enabled:
                    print(f"{attacking_char.name} is acting now...\n")
                elif overwatch_loop_mode_enabled:
                    print(f"**{defending_char.name} has moved into the overwatch zone of {attacking_char.name}!**\n")

                #Reset - This is only set to TRUE when an enemy can't find a target b.c all applicable targets are unconscious -
                #In such a case, we don't want to just immediately jump into FIGHT code if the next enemy in our list is an
                # enemy, so instead we forbid fight code with this boolean var, which will cause the next instance to at least
                # run through its AI again, which informs the player as to what the hell is going on (and makes debugging easier for me).
                enemy_passed_turn_boolean = False

                #region Enemy or Neutral AI code - we ignore AI in overwatch loop mode and pc_fleeing_combat - in which case the attacker's
                # vars have already been defined, and they only need to attack:
                #print(f"DEBUG: ABOUT TO EVALUATE WHETHER OR NOT ENEMY AI SHOULD EXECUTE: attacking_char: {attacking_char.name}, overwatch_loop_mode_enabled == {overwatch_loop_mode_enabled}, attacking_char.is_opportunity_attacker_boolean == {attacking_char.is_opportunity_attacker_boolean}")
                if overwatch_loop_mode_enabled == False and attacking_char.is_opportunity_attacker_boolean == False:

                    if (attacking_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY or attacking_char.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL):

                        #Some default values shared by all enemies/neutrals regardless of ai:
                            #Reset these vars:
                        attacking_char.enemy_ai_move_boolean = False
                        attacking_char.enemy_ai_fight_boolean = False

                        # Define attacker team - used to build nearest_target_list:
                        attacker_team = attacking_char.char_team_enum

                        # Reset to throw an error if its not defined - failsafe? Necessary?:
                        attacking_char.targeted_rank = -1

                        # Define 'chosen weapon' for this enemy or neutral
                        # Shuffle ability list to ensure that items with equal max range are chosen randomly
                        random.shuffle(attacking_char.ability_list)

                        #region overwatch stationary ai:
                        if attacking_char.combat_ai_preference == ENUM_AI_COMBAT_STATIONARY_OVERWATCH:

                            # Define max_range weapon - this will be our 'ideal_abil_range:
                            # Sort by max range - those with longest range will be on top of the list:
                            attacking_char.ability_list.sort(key=attrgetter('max_range'), reverse=True)

                            # Define chosen weapon as the weapon with the max range
                            attacking_char.chosen_weapon = attacking_char.ability_list[0]
                            ideal_abil_range = attacking_char.chosen_weapon.max_range

                            # Build our nearest target rank:
                            nearest_target_list = []
                            nearest_target_list = build_nearest_target_list(combat_initiative_list, attacking_char)

                            # It's possible this could be 0, if only unconscious pcs or neutrals remain:
                            if len(nearest_target_list) > 0:

                                # Randomize, sort positions in list:
                                random.shuffle(nearest_target_list)
                                nearest_target_list.sort(key=attrgetter('dist_to_enemy'))

                                # Define our nearest pc rank as our target rank:
                                attacking_char.targeted_rank = nearest_target_list[0].cur_combat_rank

                                # Calculate dist between cur_rank and the rank we've targeted:
                                dist_between_target = return_distance_between_ranks(attacking_char.targeted_rank,
                                                                                    attacking_char.cur_combat_rank)

                                # Set overwatch if we can't currently hit them with our max range:
                                if dist_between_target > ideal_abil_range:

                                    rank_pos = return_overwatch_rank(attacking_char, combat_rank_list, ideal_abil_range)

                                    # Define boolean var and the rank they are targeting for overwatch:
                                    attacking_char.overwatch_rank = rank_pos
                                    attacking_char.will_overwatch_boolean = True

                                    # Debug:
                                    #print(f"Debug: stationary OVERWATCH AI: for {attacking_char.name} the distance between them and their target == {dist_between_target}, which is > to their ideal_target_range of: {ideal_abil_range}--but they have the ai_has_ranged_advantage, so they have decided to set overwatch on their max range rank instead.")

                                    # Print action message:
                                    overwatch_str = wrap_str(
                                        f"{attacking_char.name} has carefully aimed their {attacking_char.chosen_weapon.item_name} at rank position {attacking_char.overwatch_rank}, and is patiently waiting for any new enemy to move into this rank...\n",
                                        TOTAL_LINE_W, False)
                                    print(overwatch_str)
                                    print("")

                                elif dist_between_target <= ideal_abil_range:

                                    # Targeted rank has already been set, just move to fight:
                                    attacking_char.enemy_ai_fight_boolean = True
                                    #print(f"Debug: stationary overwatch AI: for {attacking_char.name} the distance between them and their target == {dist_between_target}, which is less or <=>= to their ideal_target_range of: {ideal_abil_range}--AND the opposing team has the ranged advantage (there's no point withdrawing), so they have decided to attack.")

                            # Unable to build nearest target list: this means all applicable targets were unconscious:
                            elif len(nearest_target_list) <= 0:
                                print(
                                    f"{attacking_char.name} can't find any active enemies to target--they've all been downed already.\n")

                                # Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                # executing its AI:
                                enemy_passed_turn_boolean = True

                                input("Press enter to continue to the next character in the initiative queue.")
                                print("")

                                # Advance cur_char:
                                prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    cur_combat_char,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,
                                    f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")


                        #endregion

                        #region Overwatch ai:
                        elif attacking_char.combat_ai_preference == ENUM_AI_COMBAT_OVERWATCH:

                            #Define max_range weapon - this will be our 'ideal_abil_range:
                                # Sort by max range - those with longest range will be on top of the list:
                            attacking_char.ability_list.sort(key=attrgetter('max_range'), reverse=True)

                            # Define chosen weapon as the weapon with the max range
                            attacking_char.chosen_weapon = attacking_char.ability_list[0]
                            ideal_abil_range = attacking_char.chosen_weapon.max_range

                            #Define our 'alternate' weapon choice as a reward for players who back us against a wall:
                            alternate_weapon_id = attacking_char.ability_list[len(attacking_char.ability_list)-1]

                            # Build our nearest target rank:
                            nearest_target_list = []
                            nearest_target_list = build_nearest_target_list(combat_initiative_list, attacking_char)

                            # It's possible this could be 0, if only unconscious pcs or neutrals remain:
                            if len(nearest_target_list) > 0:
                                # Randomize, sort positions in list:
                                random.shuffle(nearest_target_list)
                                nearest_target_list.sort(key=attrgetter('dist_to_enemy'))

                                #Define max and min pc range - useful for ai decisions:
                                target_max_range, target_min_range = return_target_max_min_weapon_range(combat_rank_list,-1,attacking_char)

                                #Define 'ai_has_ranged_advantage' boolean var, useful for ai decisions:
                                ai_has_ranged_advantage = False
                                if ideal_abil_range >= target_max_range:
                                    ai_has_ranged_advantage = True

                                # Degbug:
                                #print(
                                    #f"DEBUG:Just called return_target_max_min_weapon_range; target_max_range = {target_max_range}, target_min_range == {target_min_range}; ai_has_ranged_advantage = {ai_has_ranged_advantage}.")

                                # Define our nearest pc rank as our target rank:
                                attacking_char.targeted_rank = nearest_target_list[0].cur_combat_rank

                                # Calculate dist between cur_rank and the rank we've targeted:
                                dist_between_target = return_distance_between_ranks(attacking_char.targeted_rank,
                                                                                    attacking_char.cur_combat_rank)

                                #Set overwatch if we need to advance but we could out-range them:
                                if dist_between_target > ideal_abil_range and ai_has_ranged_advantage:

                                    rank_pos = return_overwatch_rank(attacking_char,combat_rank_list,ideal_abil_range)

                                    # Define boolean var and the rank they are targeting for overwatch:
                                    attacking_char.overwatch_rank = rank_pos
                                    attacking_char.will_overwatch_boolean = True

                                    # Debug:
                                    #print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name}: the distance between them and their target == {dist_between_target}, which is > to their ideal_target_range of: {ideal_abil_range}--but they have the ai_has_ranged_advantage, so they have decided to set overwatch on their max range rank instead.")

                                    # Print action message:
                                    overwatch_str = wrap_str(
                                        f"{attacking_char.name} has carefully aimed their {attacking_char.chosen_weapon.item_name} at rank position {attacking_char.overwatch_rank}, and is patiently waiting for any new enemy to move into this rank...\n",
                                        TOTAL_LINE_W, False)
                                    print(overwatch_str)
                                    print("")

                                #Move closer - the nearest target is outside of our range, and we don't have the ranged advantage anyway:
                                elif dist_between_target > ideal_abil_range and ai_has_ranged_advantage == False:

                                    if attacking_char.suppressed_count <= 0:
                                        #Target is north of us - move north:
                                        if attacking_char.cur_combat_rank > attacking_char.targeted_rank:
                                            move_dir = -1
                                        #Target is south of us - move south
                                        elif attacking_char.cur_combat_rank < attacking_char.targeted_rank:
                                            move_dir = 1

                                        # Debug:
                                        #print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name} cur_combat_round > 0: the distance between them and their target == {dist_between_target}, which is > to their ideal_target_range of: {ideal_abil_range}--and we do NOT have the ranged advantage, so they have decided to move.")

                                        # Move:
                                        combat_rank_list = advance_or_withdraw_char(move_dir, combat_rank_list,
                                                                                    attacking_char)

                                        # After advancing, build our overwatch list:
                                        overwatch_attacker_list = build_overwatch_list(attacking_char,
                                                                                       combat_initiative_list)

                                        # Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                        if len(overwatch_attacker_list) > 0:
                                            cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                            cur_overwatch_attacker_index = 0
                                            overwatch_loop_mode_enabled = True
                                            overwatch_target_id = attacking_char
                                            print(
                                                f"**The {attacking_char.name} has been targeted for overwatch fire!**\n")
                                            #print(
                                                #f"DEBUG: Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")

                                    #Attacker is suppressed - just use overwatch, as it's better than just standing here and doing nothing.
                                    else:
                                        rank_pos = return_overwatch_rank(attacking_char, combat_rank_list,
                                                                         ideal_abil_range)

                                        # Define boolean var and the rank they are targeting for overwatch:
                                        attacking_char.overwatch_rank = rank_pos
                                        attacking_char.will_overwatch_boolean = True

                                        # Debug:
                                        #print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name}: the distance between them and their target == {dist_between_target}, which is > to their ideal_target_range of: {ideal_abil_range}; they do NOT have the ranged advantage and want to advance but are suppressed, so they have decided to set overwatch on their max range rank instead.")

                                        # Print action message:
                                        overwatch_str = wrap_str(
                                            f"{attacking_char.name} has carefully aimed their {attacking_char.chosen_weapon.item_name} at rank position {attacking_char.overwatch_rank}, and is patiently waiting for any new enemy to move into this rank...\n",
                                            TOTAL_LINE_W, False)
                                        print(overwatch_str)
                                        print("")

                                #elif dist_to_target <= their max_range and enemy_has_ranged_adavantage == False:
                                #We might as well fire on our target -- withdrawing wouldn't do us any good as the opposing team has the ranged advantage anyway:
                                elif dist_between_target <= ideal_abil_range and ai_has_ranged_advantage == False:
                                    # Targeted rank has already been set, just move to fight:
                                    attacking_char.enemy_ai_fight_boolean = True
                                    #print(
                                        #f"Debug: Enemy OVERWATCH AI: for {attacking_char.name} cur_combat_round > 0: the distance between them and their target == {dist_between_target}, which is less or <=>= to their ideal_target_range of: {ideal_abil_range}--AND the opposing team has the ranged advantage (there's no point withdrawing), so they have decided to attack.")

                                #Withdraw, if able, because we have the ranged advantage over the enemy, and could therefore use overwatch next turn.
                                elif dist_between_target <= ideal_abil_range and ai_has_ranged_advantage == True:

                                    if attacking_char.suppressed_count <= 0:

                                        #Regardles of whether we're north, south, or == to the target, 'withdraw':
                                        if attacking_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                            move_dir = -1
                                        else:
                                            move_dir = 1

                                        #Check to see if we can withdraw:
                                        if attacking_char.cur_combat_rank+move_dir >= 0 and attacking_char.cur_combat_rank+move_dir < len(combat_rank_list):
                                            #We can, so do so:
                                            # Debug:print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name} cur_combat_round > 0: the distance between them and their target == {dist_between_target}, which is <= to their ideal_target_range of: {ideal_abil_range}--and we DO have the ranged advantage AND are able to withdraw, so they have decided to withdraw now.")

                                            # Move:
                                            combat_rank_list = advance_or_withdraw_char(move_dir, combat_rank_list,
                                                                                        attacking_char)

                                            # After advancing, build our overwatch list:
                                            overwatch_attacker_list = build_overwatch_list(attacking_char,
                                                                                           combat_initiative_list)

                                            # Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                            if len(overwatch_attacker_list) > 0:
                                                cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                                cur_overwatch_attacker_index = 0
                                                overwatch_loop_mode_enabled = True
                                                overwatch_target_id = attacking_char
                                                print(
                                                    f"**The {attacking_char.name} has been targeted for overwatch fire!**\n")
                                                #print(
                                                    #f"DEBUG: Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")

                                        #We can't withdraw any further, just attack:
                                        else:
                                            # Targeted rank has already been set, just move to fight:
                                            attacking_char.enemy_ai_fight_boolean = True
                                            if dist_between_target == 0:
                                                attacking_char.chosen_weapon = alternate_weapon_id
                                            #print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name} cur_combat_round > 0: the distance between them and their target == {dist_between_target}, which is <= to their ideal_target_range of: {ideal_abil_range}--and we DO have the ranged advantage but are NOT able to withdraw (against wall), so they have decided to attack now -- possibly with their alternate weapon if dist_between_target == 0.")

                                    #We're suppressed and target is within range, just fire
                                    else:
                                        # Targeted rank has already been set, just move to fight:
                                        attacking_char.enemy_ai_fight_boolean = True
                                        if dist_between_target == 0:
                                            attacking_char.chosen_weapon = alternate_weapon_id
                                        #print(f"Debug: Enemy OVERWATCH AI: for {attacking_char.name} cur_combat_round > 0: the distance between them and their target == {dist_between_target}, which is <= to their ideal_target_range of: {ideal_abil_range}--and we DO have the ranged advantage but are NOT able to withdraw (against wall), so they have decided to attack now -- possibly with their alternate weapon if dist_between_target == 0.")

                            # Unable to build nearest target list: this means all applicable targets were unconscious:
                            elif len(nearest_target_list) <= 0:
                                print(
                                    f"{attacking_char.name} can't find any active enemies to target--they've all been downed already.\n")

                                # Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                # executing its AI:
                                enemy_passed_turn_boolean = True

                                input("Press enter to continue to the next character in the initiative queue.")
                                print("")

                                # Advance cur_char:
                                prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    cur_combat_char,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,
                                    f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")

                        #endregion

                        # region ENEMY OR NEUTRAL PREFERS MELEE COMBAT:
                        elif attacking_char.combat_ai_preference == ENUM_AI_COMBAT_MELEE:
                            # Sort by max range - those with shortest range will be on top of the list:
                            attacking_char.ability_list.sort(key=attrgetter('max_range'), reverse=False)

                            # Define chosen weapon as the weapon with the least range
                            attacking_char.chosen_weapon = attacking_char.ability_list[0]
                            ideal_abil_range = attacking_char.chosen_weapon.max_range #Should always be 0

                            #Debug:
                            #print(f"Before calling nearest_target_list, attacking_char: {attacking_char.name}, their cur_combat_rank: {attacking_char.cur_combat_rank}, their team_enum == {attacking_char.char_team_enum}")

                            #Find our nearest target rank:
                            nearest_target_list = []
                            nearest_target_list = build_nearest_target_list(combat_initiative_list,attacking_char)

                            # It's possible this could be 0, if only unconscious pcs or neutrals remain:
                            if len(nearest_target_list) > 0:
                                # Randomize, sort positions in list:
                                random.shuffle(nearest_target_list)
                                nearest_target_list.sort(key=attrgetter('dist_to_enemy'))

                                # Define our nearest pc rank as our target rank:
                                attacking_char.targeted_rank = nearest_target_list[0].cur_combat_rank

                                #Show debug:
                                #print(
                                    #f"Debug: Enemy AI: {attacking_char.name} determined that the rank {attacking_char.targeted_rank} was the rank in which the closest pc to them resides."
                                    #f"Their enemy_ai_fight_boolean should still == False, it == {attacking_char.enemy_ai_fight_boolean}")

                                # Calculate dist between cur_rank and the rank we've targeted:
                                dist_between_target = return_distance_between_ranks(attacking_char.targeted_rank, attacking_char.cur_combat_rank)
                                #Show debug:
                                #print(
                                    #f"Debug: Enemy AI: {attacking_char.name} the distance between them (their current rank = {attacking_char.cur_combat_rank}) and their chosen rank was: {dist_between_target}.")

                                #If we're not within range, move within range, it's that simple; these types of units move like crazed berserkers:
                                if dist_between_target > ideal_abil_range:

                                    if attacking_char.suppressed_count <= 0:
                                        # Target is NORTH of you - move north to move closer to it:
                                        if attacking_char.cur_combat_rank > attacking_char.targeted_rank:
                                            move_dir = -1

                                        # Target is SOUTH of you - move south to move closer to it:
                                        elif attacking_char.cur_combat_rank < attacking_char.targeted_rank:
                                            move_dir = 1

                                        #Move:
                                        combat_rank_list = advance_or_withdraw_char(move_dir, combat_rank_list,
                                                                                    attacking_char)

                                        # After advancing, build our overwatch list:
                                        overwatch_attacker_list = build_overwatch_list(attacking_char,
                                                                                       combat_initiative_list)

                                        # Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                        if len(overwatch_attacker_list) > 0:
                                            cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                            cur_overwatch_attacker_index = 0
                                            overwatch_loop_mode_enabled = True
                                            overwatch_target_id = attacking_char
                                            print(f"**The {attacking_char.name} has been targeted for overwatch fire!**\n")
                                            #print(
                                                #f"DEBUG: Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")

                                    #Melee unit has no alternative when suppressed--they have to pass their turn
                                    else:
                                        print(f"{attacking_char.name} struggles to advance, but can't find an opening. They've been suppressed by enemy fire!\n")

                                        # Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                        # executing its AI:
                                        enemy_passed_turn_boolean = True

                                        input("Press enter to continue to the next character in the initiative queue.")
                                        print("")

                                        # Advance cur_char:
                                        prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                        cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                            cur_combat_char,
                                            combat_initiative_list,
                                            cur_combat_room_id,
                                            cur_combat_round,
                                            prev_cur_combat_char_index,
                                            f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")

                                #Melee attack them:
                                elif dist_between_target == ideal_abil_range:
                                    #If this is a lumbering mauler, attempt to spawn skittering larva:
                                    if (attacking_char.char_type_enum == ENUM_CHARACTER_ENEMY_LUMBERING_MAULER and
                                    attacking_char.can_spawn_minions == True and attacking_char.spawn_minion_count > 0):
                                        #Spawn a certain number of skittering larva:
                                        combat_initiative_list, combat_rank_list = spawn_combat_minion(attacking_char,combat_initiative_list,combat_rank_list,False)

                                    # Targeted rank has already been set, just move to fight:
                                    attacking_char.enemy_ai_fight_boolean = True
                                    #print(
                                        #f"Debug: Enemy AI: {attacking_char.name} the distance between them and their target == {dist_between_target}, which is the same as their ideal_target_range of: {ideal_abil_range}--so they have decided to attack.")

                            #Unable to build nearest target list: this means all applicable targets were unconscious:
                            elif len(nearest_target_list) <= 0:
                                print(
                                    f"{attacking_char.name} can't find any active enemies to target--they've all been downed already.\n")

                                # Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                # executing its AI:
                                enemy_passed_turn_boolean = True

                                input("Press enter to continue to the next character in the initiative queue.")
                                print("")

                                # Advance cur_char:
                                prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    cur_combat_char,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,
                                    f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")

                        # endregion

                        #region AI: RANGED_COWARD
                        elif attacking_char.combat_ai_preference == ENUM_AI_COMBAT_RANGED_COWARD:

                            #If a suppressor type (chittering lurker), randomly choose one of this character's items that can suppress:
                            if attacking_char.ai_is_suppressor_boolean:
                                #Sort ability list by those items that can suppress or not:
                                attacking_char.ability_list.sort(key=attrgetter('can_suppress_boolean'), reverse=True)
                                #Define chosen weapon as the top-most item that can suppress:
                                attacking_char.chosen_weapon = attacking_char.ability_list[0]
                                ideal_abil_range = attacking_char.chosen_weapon.max_range
                                # Also Define the 'alternate' weapon for this char -- in this case it will their ability with the lowest range:
                                # Usually 'desperate claw'
                                attacking_char.ability_list.sort(key=attrgetter('max_range'), reverse=False)
                                attacking_char.ai_inferior_alternate_wep = attacking_char.ability_list[0]
                                alternate_abil_range = attacking_char.ai_inferior_alternate_wep.max_range
                            # If not a suppressor type (Spined Spitter, Sodden Shambler): Search for ability item with the maximum range
                            else:
                                #Sort by max range:
                                attacking_char.ability_list.sort(key=attrgetter('max_range'),reverse=True)
                                # Define chosen weapon as the weapon with the maximum range
                                attacking_char.chosen_weapon = attacking_char.ability_list[0]
                                ideal_abil_range = attacking_char.chosen_weapon.max_range
                                # Also Define the 'alternate' weapon for this char -- in this case it will their ability with the lowest range:
                                # Usually 'desperate claw'
                                attacking_char.ability_list.sort(key=attrgetter('max_range'), reverse=False)
                                attacking_char.ai_inferior_alternate_wep = attacking_char.ability_list[0]
                                alternate_abil_range = attacking_char.ai_inferior_alternate_wep.max_range

                            #Define nearest pc target, then determine if you need to move closer to get it within range;
                            # or farther away to maintain your ideal_abil_range:
                                #Find nearest pc: cur_combat_rank
                            nearest_target_list = build_nearest_target_list(combat_initiative_list, attacking_char)

                            #It's possible this could be 0, if only unconscious pcs or neutrals remain:
                            if len(nearest_target_list) > 0:
                                #Randomize, sort positions in list:
                                random.shuffle(nearest_target_list)
                                nearest_target_list.sort(key=attrgetter('dist_to_enemy'))

                                #"""Okay, we've defined the closest applicable pc rank to us; the rest of this AI generally tries to
                                # move away (north) from that closest rank to maintain its max_range between itself and that rank, or it will
                                # try to move closer if the target rank is outside of the max range. It also won't move into or out
                                # of any rank that has over-watch on it if it can use over-watch itself.
                                # That's it"""

                                #Define our nearest pc rank as our target rank:
                                attacking_char.targeted_rank = nearest_target_list[0].cur_combat_rank

                                #print(
                                    #f"Debug: Enemy AI: {attacking_char.name} determined that the rank {attacking_char.targeted_rank} was the rank in which the closest pc to them resides."
                                    #f"Their enemy_ai_fight_boolean should still == False, it == {attacking_char.enemy_ai_fight_boolean}")

                                #Calculate dist between cur_rank and the rank we've targeted:
                                dist_between_target = return_distance_between_ranks(attacking_char.targeted_rank,attacking_char.cur_combat_rank)
                                #print(
                                    #f"Debug: Enemy AI: {attacking_char.name} the distance between them (their current rank = {attacking_char.cur_combat_rank}) and their chosen rank was: {dist_between_target}.")

                                #This is our ideal range - so fight
                                if dist_between_target == ideal_abil_range:
                                    #Targeted rank has already been set, just move to fight:
                                    attacking_char.enemy_ai_fight_boolean = True
                                    #print(
                                        #f"Debug: Enemy AI: {attacking_char.name} the distance between them and their target == {dist_between_target}, which is the same as their ideal_target_range of: {ideal_abil_range}--so they have decided to attack.")

                                #Target is getting close - backup to maintain our ideal range:
                                elif dist_between_target < ideal_abil_range:

                                    if attacking_char.suppressed_count <= 0:
                                        #print(
                                            #f"Debug: Enemy AI: {attacking_char.name} the distance between them and their target did NOT equal their ideal_target_range of: {ideal_abil_range}--"
                                            #f"BUT they were < than their ideal_abil_range, so they have decided to try and move north, if able, to maintain their ideal abil range.")

                                        if attacking_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                            move_dir = -1
                                        else:
                                            move_dir = 1

                                        #Determine if it can actually move in that direction:
                                        if (attacking_char.cur_combat_rank + move_dir >= 0 and
                                        attacking_char.cur_combat_rank + move_dir < len(combat_rank_list) and attacking_char.suppressed_count <= 0) :

                                            combat_rank_list = advance_or_withdraw_char(move_dir, combat_rank_list,
                                                                                        attacking_char)

                                            #print(f"Debug: Enemy AI: {attacking_char.name} was able to advance or withdraw to adjust their rank in relation to their nearest pc target in order to utilize their max_range. enemy_ai_fight_boolean should still == False, it == {attacking_char.enemy_ai_fight_boolean}")

                                            # After advancing, build our overwatch list:
                                            overwatch_attacker_list = build_overwatch_list(attacking_char, combat_initiative_list)

                                            # Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                            if len(overwatch_attacker_list) > 0:
                                                cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                                cur_overwatch_attacker_index = 0
                                                overwatch_loop_mode_enabled = True
                                                overwatch_target_id = attacking_char
                                                print(f"**The {attacking_char.name} has been targeted for overwatch fire!**\n")
                                                #print(f"DEBUG:Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")
                                        #Either we can't move any further in that direction or we're suppressed--either way, just attack nearest
                                        #target because they are within our max_range:
                                        else:
                                            #If we can't move in any further in that direction, just choose the nearest pc rank for attack:
                                            suppressed_debug_str = "No"
                                            if attacking_char.suppressed_count > 0:
                                                suppressed_debug_str = "YES, THEY ARE SUPPRESSED!"
                                            #print(f"Debug: Enemy AI: {attacking_char.name}: Couldn't move any further north or south as they were already on the boundaries of combat_rank_list, or because they were suppressed. Are they suppressed? Answer: {suppressed_debug_str}. Their suppressed_count == {attacking_char.suppressed_count}")

                                            attacking_char.enemy_ai_fight_boolean = True

                                            #print(f"Debug: Enemy AI: {attacking_char.name}: Our distance between ourself and our target rank: {dist_between_target} was <= our ideal_abil_range: {ideal_abil_range}."
                                                  #f"So we're just going to attack them.")

                                            #This rewards the player by backing this enemy into a wall - at which point the enemy is forced to use a weaker
                                            # melee attack instead; this is VERY exploitable by the player and so should only be used by certain enemy types;
                                            # in this case: the suppressor types.
                                            if attacking_char.ai_is_suppressor_boolean:
                                                if attacking_char.targeted_rank == attacking_char.cur_combat_rank:
                                                    attacking_char.chosen_weapon = attacking_char.ai_inferior_alternate_wep
                                                    #print(f"Debug: Enemy AI: {attacking_char.name}: This ai unit with RANGED_PREFERENCE_COWARD and ai_is_suppressor_boolean ==True has been backed into a wall and targets are in its same rank (melee range); as a reward for the player, this target will now be forced to use their inferior weapon.")

                                    #Attacker wants to withdraw to maintain ideal range but can't due to suppression,
                                    #so just attack instead:
                                    else:
                                        # Targeted rank has already been set, just move to fight:
                                        attacking_char.enemy_ai_fight_boolean = True
                                        #print(
                                            #f"Debug: Enemy AI: {attacking_char.name} the distance between them and their target == {dist_between_target}, which is < than their ideal_target_range of: {ideal_abil_range}; they would withdraw but they are supprsesed so they have decided to attack.")

                                elif dist_between_target > ideal_abil_range:
                                    #We need to move closer:
                                    #print(
                                        #f"Debug: Enemy AI: {attacking_char.name}: Our distance between ourself and our target rank: {dist_between_target} was > our ideal_abil_range (our max_range): {ideal_abil_range}."
                                        #f"So we're going to move closer to them. Our suppressed_count == {attacking_char.suppressed_count}")

                                    # Target is NORTH of you - move north to move closer to it:
                                    if attacking_char.cur_combat_rank > attacking_char.targeted_rank:
                                        move_dir = -1

                                    # Target is SOUTH of you - move south to move closer to it:
                                    elif attacking_char.cur_combat_rank < attacking_char.targeted_rank:
                                        move_dir = 1

                                    #Target is of equal distance - this case should never trigger:
                                    elif attacking_char.cur_combat_rank == attacking_char.targeted_rank:
                                        #This technically should never be the case, because otherwise dist_between_target <= ideal_abil_range would have triggered
                                        #print(f"Debug: For enemy ai with name of: {attacking_char.name}: something really odd happened, dist_between_target was greater than ideal_abil_range, but enemy was also in the same rank as the targeted_rank. Investigate.")
                                        pass
                                    #Move, if this attacker is not suppressed:
                                    if attacking_char.suppressed_count <= 0:
                                        #Advance or withdraw to get closer to our target rank:
                                        combat_rank_list = advance_or_withdraw_char(move_dir, combat_rank_list,
                                                                                    attacking_char)

                                        # After advancing or withdrawing, build our overwatch list:
                                        overwatch_attacker_list = build_overwatch_list(attacking_char,combat_initiative_list)

                                        #Move to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST, if applicable:
                                        if len(overwatch_attacker_list) > 0:
                                            cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                                            cur_overwatch_attacker_index = 0
                                            overwatch_loop_mode_enabled = True
                                            overwatch_target_id = attacking_char
                                            print(f"*{attacking_char.name} has been targeted for overwatch fire!*\n")
                                            #print(
                                                #f"DEBUG: Their index position in the combat_initiative_list == {combat_initiative_list.index(attacking_char)}.")
                                    else:
                                        #Print suppressed string
                                        print(f"{attacking_char.name} wants to advance, but can't find an opening. They've been suppressed by enemy fire!\n")

                                        # Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                        # executing its AI:
                                        enemy_passed_turn_boolean = True

                                        continue_key = input("Press enter to continue to the next character in the initiative queue.")
                                        print("")

                                        # Advance cur_char:
                                        prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                        cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                            cur_combat_char,
                                            combat_initiative_list,
                                            cur_combat_room_id,
                                            cur_combat_round,
                                            prev_cur_combat_char_index,
                                            f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")

                            #This can occur if all remaining pcs or neutrals are unconscious:
                            elif len(nearest_target_list) <= 0:
                                print(f"{attacking_char.name} can't find any active enemies to target--they've all been downed already.\n")

                                #Set var so the next enemy instance doesn't just instantly move to FIGHT code without
                                #executing its AI:
                                enemy_passed_turn_boolean = True

                                #Advance cur_char:
                                prev_cur_combat_char_index = combat_initiative_list.index(attacking_char)

                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    cur_combat_char,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,
                                    f"DEBUG: Moving away from EXECUTE_ACTION game_state: cur_char {cur_combat_char.name} for enemy or neutral AI: RANGED_PREFERENCE: nearest_target_list) <= 0, which means all applicable targets are downed and unconscious.")
                        # endregion

                #endregion

                # Reset:
                defender_killed_boolean = False

                #Actual FIGHT code:
                #It's possible we've moved into GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST by now, so make sure we're still
                # in this game state:
                if cur_game_state == GAME_STATE_COMBAT_EXECUTE_ACTION and enemy_passed_turn_boolean == False:

                    if (attacking_char.enemy_ai_fight_boolean or attacking_char.char_team_enum == ENUM_CHAR_TEAM_PC or
                            overwatch_loop_mode_enabled):
                        #Create a new list to get only the enemies of the opposite team from this rank:
                        filtered_enemy_list = []

                        #Filter chars of the same team from the chosen rank:
                        if not overwatch_loop_mode_enabled:
                            #Add Characters from the attacker's opposing team to the filtered_enemy_list
                            for i in range(0,len(combat_rank_list[attacking_char.targeted_rank])):
                                if attacking_char.char_team_enum == ENUM_CHAR_TEAM_PC or attacking_char.char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:
                                    if combat_rank_list[attacking_char.targeted_rank][i].char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                        filtered_enemy_list.append(combat_rank_list[attacking_char.targeted_rank][i])
                                elif attacking_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                    if (combat_rank_list[attacking_char.targeted_rank][i].char_team_enum == ENUM_CHAR_TEAM_PC or
                                    combat_rank_list[attacking_char.targeted_rank][i].char_team_enum == ENUM_CHAR_TEAM_NEUTRAL):
                                        if combat_rank_list[attacking_char.targeted_rank][i].unconscious_boolean == False:
                                            filtered_enemy_list.append(combat_rank_list[attacking_char.targeted_rank][i])

                            #Define how we'll iterate through filtered list:
                                # We'll iterate through the filtered_list sequentially, choosing new targets each time:
                            target_all_enemies = False
                            cur_target_index_in_list = 0
                            if attacking_char.chosen_weapon.aoe_count == -1:
                                enemies_to_target = len(filtered_enemy_list)
                                target_all_enemies = True
                            # Define enemies_to_target to choose a random defender in already defined rank:
                            else:
                                enemies_to_target = min(random.randint(1, attacking_char.chosen_weapon.aoe_count),
                                                        len(filtered_enemy_list))

                        #Manually define vars we'll need to not break the iteration code:
                        elif overwatch_loop_mode_enabled:
                            filtered_enemy_list.append(overwatch_target_id)
                            enemies_to_target = 1

                        #Manually define vars we'll need to not break the iteration code:
                        if pc_fleeing_combat_boolean:
                            filtered_enemy_list = -1
                            filtered_enemy_list = []
                            filtered_enemy_list.append(fleeing_pc_id)
                            enemies_to_target = 1

                        #Move into iteration code:
                        if len(filtered_enemy_list) > 0:

                            #Iterate
                            for i in range(0,enemies_to_target):
                                # Deduct ammunition or deduct ability points:
                                sufficient_ammo_boolean = True
                                if attacking_char.char_team_enum == ENUM_CHAR_TEAM_PC and attacking_char.chosen_weapon.requires_ammo_boolean:
                                    if ammo_total <= 0:
                                        sufficient_ammo_boolean = False
                                    else:
                                        if attempting_suppress_boolean:
                                            attacking_char.chosen_weapon.status_effect_list[ENUM_STATUS_EFFECT_SUPPRESSED] = 100
                                            ammo_total -= 2
                                        else:
                                            ammo_total -= 1
                                        #Cap, if necessary:
                                        if ammo_total < 0:
                                            ammo_total = 0

                                if sufficient_ammo_boolean:
                                    if len(filtered_enemy_list) > 0:
                                        #Define our defending char as either a random target in that rank (if target_all_enemies == False);
                                        if not overwatch_loop_mode_enabled:
                                            if not target_all_enemies:
                                                defending_char = filtered_enemy_list[random.randint(0,len(filtered_enemy_list)-1)]
                                            #Define our defending char as the next target in the filtered list, then iterate index var:
                                            elif target_all_enemies:
                                                defending_char = filtered_enemy_list[cur_target_index_in_list]
                                                cur_target_index_in_list += 1

                                        #Begin to_hit calculation:
                                        attacker_accuracy = attacking_char.accuracy
                                        #Apply to_hit debuff if we're using suppressive fire mode:
                                        if attempting_suppress_boolean:
                                            attacker_accuracy -= ENUM_SUPPRESSIVE_FIRE_ACCURACY_DEBUFF
                                        #Apply to_hit bonus if under the effects of adrenal pen:
                                        if attacking_char.adrenal_pen_count > 0:
                                            attacker_accuracy += ENUM_ADRENAL_PEN_BONUS
                                        #Ogre melee character gets slight to_hit bonus with melee weapons
                                        if attacking_char.char_type_enum == ENUM_CHARACTER_OGRE and attacking_char.chosen_weapon.max_range == 0:
                                            attacker_accuracy += ENUM_OGRE_MELEE_ACC_BONUS
                                        #Define defender evasion and armor:
                                        defender_evasion = defending_char.evasion
                                        defender_armor = defending_char.armor
                                        #Apply 'dodging' bonus:
                                        if defending_char.dodge_bonus_boolean:
                                            defender_evasion += 1
                                        #Apply 'shield bonus':
                                        if defending_char.shield_bonus_count > 0:
                                            defender_evasion += ENUM_PERSONAL_SHIELD_BONUS
                                            defender_armor += ENUM_PERSONAL_SHIELD_BONUS
                                        #Apply 'hold the line' bonus:
                                        if defending_char.hold_the_line_count > 0:
                                            defender_evasion += ENUM_HOLD_THE_LINE_EVADE_BONUS
                                        #Apply 'suppressed' malus:
                                        if defending_char.suppressed_count > 0:
                                            defender_evasion -= ENUM_SUPPRESSED_EVASION_DEBUFF
                                        #Create alternate string and add to attackers_accuracy if defender's evasion is less than 0:
                                        alternate_to_hit_str = ""
                                        if defender_evasion < 0:
                                            attacker_hit_val = attacker_accuracy + abs(defender_evasion)
                                            alternate_to_hit_str = " Their accuracy was boosted by the defender's negative evasion value instead!"
                                        else:
                                            attacker_hit_val = attacker_accuracy - defender_evasion

                                        ran_combat_val = random.randint(ENUM_MIN_COMBAT_RAN_NUM,ENUM_MAX_COMBAT_RAN_NUM)

                                        #Show player the to_hit chance and random value:
                                        to_hit_str = wrap_str(
                                            f"{attacking_char.name} {attacking_char.chosen_weapon.item_verb} {attacking_char.chosen_weapon.item_name}. Chance to hit: {attacker_accuracy} (accuracy) reduced by {defender_evasion} (defender's evasion) = {attacker_hit_val}.{alternate_to_hit_str} Rolled: {ran_combat_val}.",
                                            TOTAL_LINE_W, False)
                                        print(to_hit_str)
                                        print("")

                                        #Hit-miss logic -- HIT
                                        if attacker_hit_val >= ran_combat_val:
                                            #Hit:
                                            dmg_roll = random.randint(attacking_char.chosen_weapon.dmg_min,attacking_char.chosen_weapon.dmg_max)
                                            #Add extra damage if Cragos is attacking in melee:
                                            if attacking_char.char_type_enum == ENUM_CHARACTER_OGRE and attacking_char.chosen_weapon.max_range == 0:
                                                dmg_roll += random.randint(1,ENUM_OGRE_MELEE_DMG_BONUS)
                                            #Cap total damage at no less than 0:
                                            total_dmg = max(0,dmg_roll-defender_armor)
                                            #Check death, reduce hp, check status effects, etc:
                                            if total_dmg > 0:
                                                defending_char.hp_cur -= total_dmg
                                                #Print damage results along with armor reduction
                                                print(f"The {defending_char.name} has been {attacking_char.chosen_weapon.item_dmg_str} for {dmg_roll} damage - {defending_char.armor} armor, for a total of {total_dmg} damage!\n")
                                                #Destroy defending instance
                                                if defending_char.hp_cur <= 0:
                                                    if defending_char.char_team_enum == ENUM_CHAR_TEAM_PC:
                                                        print(f"{defending_char.name} has collapsed!\n")
                                                        defending_char.unconscious_boolean = True
                                                        defending_char.unconscious_count = ENUM_BASE_UNCONSCIOUS_COUNT
                                                    else:
                                                        if (defending_char.char_type_enum >= ENUM_CHARACTER_NEUTRAL_JITTERING_BUZZSAW and
                                                        defending_char.char_type_enum <= ENUM_CHARACTER_NEUTRAL_LIGHT_SENTRY_DRONE):
                                                            print(f"{defending_char.name} has been destroyed!\n")
                                                        else:
                                                            print(f"{defending_char.name} has been killed!\n")
                                                            #Spawn skittering larva, if able:
                                                            if defending_char.char_type_enum == ENUM_CHARACTER_ENEMY_LUMBERING_MAULER and defending_char.spawn_minion_count > 0:
                                                                #Spawn minions:
                                                                combat_initiative_list, combat_rank_list = spawn_combat_minion(defending_char,combat_initiative_list,combat_rank_list,True)

                                                    defender_killed_boolean = True
                                                    if overwatch_loop_mode_enabled:
                                                        #Important! We need to change this prev_cur_combat_char_index to == the index of the defending_char
                                                        #b.c when we later try to advance the cur_combat_char, we want to be using this index, NOT the attacker's index (they could be anywhere in the list)
                                                        prev_cur_combat_char_index = combat_initiative_list.index(defending_char)

                                                    #Destroy the defender by removing them from all applicable lists:
                                                    valid_death = True
                                                    #Unconscious pcs don't immediately die or get removed from memory; nor should they be getting targeted by other enemies.
                                                    if defending_char.char_team_enum == ENUM_CHAR_TEAM_PC:
                                                        valid_death = False
                                                    if valid_death:

                                                        #print(f"Debug: before entering destroy_combatant_inst: the defending_char's index in combat_initiative_list is : {combat_initiative_list.index(defending_char)}.")

                                                        combat_rank_list, combat_initiative_list, pc_char_list,enemy_char_list,neutral_char_list = destroy_combatant_inst(combat_rank_list,
                                                                                                                                               combat_initiative_list,
                                                                                                                                               defending_char,
                                                                                                                                               pc_char_list,enemy_char_list,neutral_char_list)
                                                        #EOF
                                                #If they've been hit, taken damage > 0 AND haven't been killed - apply status effects:
                                                if not defender_killed_boolean:
                                                    apply_status_effects(defending_char,attacking_char.chosen_weapon)

                                            #Print damage absorption - still check for status effect, if item allows it:
                                            else:
                                                print(f"The {defending_char.name} has been {attacking_char.chosen_weapon.item_dmg_str} for {dmg_roll} damage - but their armor fully absorbed the damage!\n")

                                                #Apply status effect anyway, if the chosen_weapon always applies status effects:
                                                if attacking_char.chosen_weapon.always_checks_status_effect_boolean:
                                                    apply_status_effects(defending_char, attacking_char.chosen_weapon)
                                        #Print miss message:
                                        else:
                                            if attacking_char.char_team_enum == ENUM_CHAR_TEAM_ENEMY:
                                                print(
                                                    f"{attacking_char.name} misses {defending_char.name} with their attack!\n")
                                            else:
                                                print(
                                                    f"{attacking_char.name} misses the {defending_char.name} with their attack!\n")
                                    else:
                                        #print("debug only: filtered_list is empty, last enemy instance in this rank deleted.")
                                        break
                                else:
                                    print(f"The {attacking_char.chosen_weapon.item_name} jammed! {attacking_char.name} is out of ammo!\n")
                                    break
                        else:
                            #This shouldn't conceivably happen, as we check for it in enemy ai.
                            #print(f"Debug: Error: {attacking_char.name} couldn't find any targets; its filtered_enemy_list len == 0.")
                            pass

                    #endregion

                    #region Resolve this phase of combat: destroy weapon (if single use);
                    # advance cur_char;
                    # check to see if combat concluded:
                        #Destroy weapon (if single use):
                    if isinstance(attacking_char.chosen_weapon,Item):
                        if attacking_char.chosen_weapon.single_use_boolean:
                            if isinstance(attacking_char.inv_list,list):
                                if attacking_char.chosen_weapon in attacking_char.inv_list:
                                    item_index = attacking_char.inv_list.index(attacking_char.chosen_weapon)
                                    if item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                                        del attacking_char.inv_list[item_index]
                                    else:
                                        is_two_handed_wep = check_two_handed_item(attacking_char.chosen_weapon)
                                        if is_two_handed_wep == False:
                                            attacking_char.inv_list[item_index] = -1
                                        elif is_two_handed_wep == True:
                                            attacking_char.inv_list[ENUM_EQUIP_SLOT_RH] = -1
                                            attacking_char.inv_list[ENUM_EQUIP_SLOT_LH] = -1
                                        elif is_two_handed_wep == -1:
                                            print(f"DEBUG: EXECUTE_ACTION: destroying 'single use' weapon after it was used for item: {attacking_char.chosen_weapon.item_name}, check_two_handed_item() returned -1 which means the char had equipped a weapon without the equip_slot enums LH or RH, something went very wrong.")


                            #Set attribute == -1 (remove it from memory)
                            attacking_char.chosen_weapon = -1

                    #In any case, the attacking_char has had a chance to do something-now their is_opportunity_attacker_boolean
                    #must be reset:
                    attacking_char.is_opportunity_attacker_boolean = False

                    # Reset suppress:
                    if attempting_suppress_boolean and isinstance(attacking_char.chosen_weapon,Item):
                        attacking_char.chosen_weapon.status_effect_list[ENUM_STATUS_EFFECT_SUPPRESSED] = 0
                        print(f"For attacking char: {attacking_char.name}, their item: {attacking_char.chosen_weapon.item_name} had its status_effect_list[suppress_enum] reset to 0.")

                    #Advance cur_combat_char (and possibly cur_combat_round), but only if we're not in overwatch loop mode:
                    if not overwatch_loop_mode_enabled:

                        #Execute 'flee' for character:
                        if (pc_fleeing_combat_boolean and defending_char.unconscious_boolean == False and defending_char.hp_cur > 0
                        and defending_char.completely_dead_boolean == False):
                            #Reset:
                            pc_fleeing_combat_boolean = False
                            #Assign index before it's removed:
                            prev_cur_combat_char_index = combat_initiative_list.index(defending_char)
                            #Flee
                            execute_char_combat_flee(combat_initiative_list, combat_rank_list, cur_combat_room_id,
                                                     fleeing_pc_id, False)

                        #Advance cur char:
                        cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(cur_combat_char,
                                                                                                                            combat_initiative_list,
                                                                                                                            cur_combat_room_id,
                                                                                                                            cur_combat_round,
                                                                                                                            prev_cur_combat_char_index,
                                                                                                                            f"Moving away from EXECUTE_ACTION game state for cur_combat_char: {cur_combat_char.name}, combat FIGHT just finished executing and overwatch_loop mode == FALSE.")
                        #EOF

                    #pc has by now either fled or been killed; either way, reset this var:
                    pc_fleeing_combat_boolean = False

                    #Check to see if combat needs to end:
                    combat_concluded_boolean, enemies_won_boolean = check_combat_end_condition(cur_combat_room_id)

                    if combat_concluded_boolean:
                        overwatch_loop_mode_enabled = False #Always reset
                        if enemies_won_boolean == False:
                            prematurely_end_overwatch_mode = True
                            #Reset, clear our combat lists:
                            combat_initiative_list = -1
                            combat_rank_list = -1
                            overwatch_attacker_list = -1
                            attacking_char = -1
                            defending_char = -1
                            cur_combat_char = -1
                            filtered_enemy_list = -1
                            #Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                            cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                            continue_key = input("The battle is over! Every enemy has fled or been slain. Press enter to continue.")
                            print("")
                        elif enemies_won_boolean:
                            remove_team_chars_from_room(cur_combat_room_id, ENUM_CHAR_TEAM_NEUTRAL)
                            print(
                                "The battle is over! The enemies in this room cavort and slaver in the wake of their victory...\n")
                            if len(pc_char_list) <= 0:
                                print("Every playable character has died--you have lost! Hopefully you learned a thing or two from your experiences...")
                                game_end = True
                            else:
                                prematurely_end_overwatch_mode = True
                                # Reset, clear our combat lists:
                                combat_initiative_list = -1
                                combat_rank_list = -1
                                overwatch_attacker_list = -1
                                attacking_char = -1
                                defending_char = -1
                                cur_combat_char = -1
                                filtered_enemy_list = -1
                                # Go back to our game_state GAME_STATE_INITIALIZING_NEW_TURN to see if other chars in other rooms will be attacked.
                                cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN
                                continue_key = input(
                                    "Press enter to continue.")
                                print("")

                    elif not combat_concluded_boolean:
                        #Check to see if we can move to the next char in the overwatch_attackers_list;
                        #If we can't, then advance the game state;
                        #If we can, then move back to GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST
                        if overwatch_loop_mode_enabled and not defender_killed_boolean:
                            #Check to see if we can move to next char in the overwatch_attackers_list:
                            cur_overwatch_attacker_index += 1

                            #Overwatch has ended, move to next character in initiative_list; use overwatch_target_id
                            # as our index for advancing the cur_char:
                            if cur_overwatch_attacker_index >= len(overwatch_attacker_list):
                                #Advance cur_char and game_state:
                                cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                    overwatch_target_id,
                                    combat_initiative_list,
                                    cur_combat_room_id,
                                    cur_combat_round,
                                    prev_cur_combat_char_index,f"End of _EXECUTE_ACTION game state for cur_combat_char: {cur_combat_char.name}, combat has NOT concluded, ovewatch_loop_mode was enabled and defender was NOT killed. Overwatch loop mode is now ending because our cur_overwatch_attacker_index >= len(overwatch_attacker_list). Moving to next instance in initiative queue.")
                                # EOF

                                # Reset, super important!
                                overwatch_loop_mode_enabled = False
                                overwatch_target_id = -1
                                overwatch_attacker_id = -1
                                overwatch_attacker_list = -1

                                #Await player input:
                                continue_str = input(
                                    "Press enter to continue to the next combatant in the initiative queue.")
                                print("")

                            #Move back to game_state ITERATE OVERWATCH
                            else:
                                cur_game_state = GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST

                        #Simply advance the cur_combat_char and end overwatch mode.
                        elif overwatch_loop_mode_enabled and defender_killed_boolean:
                            # Overwatch has ended, move to next character in initiative_list;
                            # since overwatch_target_id was killed, we'll use their prev_cur_combat_char_index in
                            # advance_combat_cur_char to advance to the next applicable char in the combat_init_list
                            # (it will be the Char in the index position of prev_cur_combat_char_index-1, or 0).

                            #Note: prev_cur_combat_char_index was also adjusted to reflect the defending_char (the overwatch target it)
                            # above, when they were killed.
                            cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                overwatch_target_id,
                                combat_initiative_list,
                                cur_combat_room_id,
                                cur_combat_round,
                                prev_cur_combat_char_index,f"end of _EXECUTE_ACTION game state for {cur_combat_char.name}, combat has NOT concluded, overwatch loop mode was enabled AND defender (the moving inst) has been killed, so now we're ending overwatch loop mode and moving to our next instance in our init_queue.")
                            # EOF

                            # Reset, super important!
                            overwatch_loop_mode_enabled = False
                            overwatch_target_id = -1
                            overwatch_attacker_id = -1
                            overwatch_attacker_list = -1

                            #Await player input:
                            continue_str = input("Press enter to continue to the next combatant in the initiative queue.")
                            print("")

                        #Pause for player input; overwatch_loop is not in effect and game_state has already advanced with advanced_combat_char()
                        else:
                            continue_str = input("Press enter to continue to the next combatant in the initiative queue.")
                            print("")

        # endregion

        #region game_state == GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST:

        elif cur_game_state == GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST:
            #Define overwatch_attacker_id
            overwatch_attacker_id = overwatch_attacker_list[cur_overwatch_attacker_index]

            #print(f"Debug: cur_game_state == GAME_STATE_COMBAT_ITERATE_OVERWATCH_LIST: overwatch_attacker_id.name == {overwatch_attacker_id.name}, overwatch_target_id.name == {overwatch_target_id.name}. \n Moving into EXECUTE_COMBAT now.")

            cur_game_state = GAME_STATE_COMBAT_EXECUTE_ACTION

        #endregion

        #region game_state == main

        elif cur_game_state == GAME_STATE_MAIN:

            #define location_grid_to_use and cur_room_inst_id:
            cur_grid_to_use = cur_char.cur_grid
            cur_room_inst_id = cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x]

            #Show room description - no need for another line break after this method, the for-loop witin it provides the necessary spaces:
            if print_room_recap:
                #Print room description, which includes keywords:
                cur_room_inst_id.print_room_desc()

                #Print any items on the floor in this room (but only if scavenged_once_boolean == True)
                if cur_room_inst_id.scavenged_once_boolean:
                    cur_room_inst_id.print_scavenge_list_item()

                #Print available directions:
                cur_room_inst_id.print_room_directions()
                print("")

                #Print any enemies in this room:
                cur_room_inst_id.print_char_list(ENUM_CHAR_TEAM_ENEMY)
                #Print any neutral chars in this room:
                cur_room_inst_id.print_char_list(ENUM_CHAR_TEAM_NEUTRAL)
                #Print all friendly characters in this room:
                cur_room_inst_id.print_char_list(ENUM_CHAR_TEAM_PC)

                #Print player what global resources the party is currently carrying: basic tech, advanced tech, food, fuel
                resource_str = wrap_str(f"The party is carrying between them the following shared resources: Food: {food_total}, Basic Tech.: {basic_tech_total}, Advanced Tech: {advanced_tech_total}, Ammunition: {ammo_total}, Engine Fuel: {fuel_total}.",TOTAL_LINE_W,False)
                print(resource_str)
                print("")

                #Tell player which character they are currently inhabiting, along with their primary stats (hp, stamina, sanity):
                status_effect_str = return_status_effects_str(cur_char)
                char_status_str = wrap_str(f"You are {cur_char.name}. You have {cur_char.hp_cur}/{cur_char.hp_max} hit points, {cur_char.ability_points_cur}/{cur_char.ability_points_max} ability points, {cur_char.sanity_cur}/{cur_char.sanity_max} sanity points, {cur_char.armor} armor, and {cur_char.evasion} evasion. {status_effect_str}",TOTAL_LINE_W,False)
                print(char_status_str)
                print_room_recap = False #Set to false so we don't see all of this again whenever the player performs a trivial action; is reset to True whenever the player moves to a different room, or uses the 'L'ook command:
                print("")

            input_str = input("What will you do? (You can enter '?' or 'HELP' at any time for a full list of commands.) >").upper().strip()
            print("")

            #Parse string for logic:
            #region Using integers or < or > to change character control:
            valid_int = False
            try:
                int_char = int(input_str)
                valid_int = True
            except:
                pass
            if valid_int:
                if int_char >= 0 and int_char < len(pc_char_list):
                    cur_char = pc_char_list[int_char]
                    cur_char_index = int_char
                    print_room_recap = True
                    print(f"You change control to {cur_char.name}\n")
                else:
                    print("That is an invalid friendly character, use 'P' or 'PARTY' to find the number associated with each playable party member.")
                    print("You can also '<' or '>' to iterate through each party member.\n")
            elif input_str == "<" or input_str == ">":
                iterate_dir = 1
                if input_str == "<":
                    iterate_dir = -1
                #Adjust and cap cur_char_index:
                cur_char_index += iterate_dir
                if cur_char_index < 0:
                    cur_char_index = len(pc_char_list)-1
                elif cur_char_index >= len(pc_char_list):
                    cur_char_index = 0
                #Change cur_char, reprint room:
                cur_char = pc_char_list[cur_char_index]
                print_room_recap = True
                print(f"You change control to {cur_char.name}\n")
            #endregion

            #region Display help instructions
            elif input_str == "?" or input_str == "HELP":
                wrapped_instructions_list = wrap_str(help_instructions_str_list,TOTAL_LINE_W,True)
                for i in wrapped_instructions_list:
                    print(i)
                print("")
            #endregion

            #region Check cardinal directions:
            elif (input_str == "W" or input_str == "WEST" or input_str == "N" or input_str == "NORTH" or
            input_str == "E" or input_str == "EAST" or input_str == "S" or input_str == "SOUTH"):
                parsed_str = input_str
                if input_str == "W":
                    parsed_str = "WEST"
                elif input_str == "E":
                    parsed_str = "EAST"
                elif input_str == "S":
                    parsed_str = "SOUTH"
                elif input_str == "N":
                    parsed_str = "NORTH"
                if parsed_str in cur_room_inst_id.directional_dict:
                    if (cur_room_inst_id.directional_dict[parsed_str] == ENUM_DOOR_UNLOCKED or
                    cur_room_inst_id.directional_dict[parsed_str] == ENUM_DOOR_DESTROYED):
                        if cur_char.cur_action_points > 0:
                            move_dir_x = 0
                            move_dir_y = 0
                            if parsed_str == "WEST":
                                move_dir_x = -1
                            elif parsed_str == "EAST":
                                move_dir_x = 1
                            elif parsed_str == "SOUTH":
                                move_dir_y = 1
                            elif parsed_str == "NORTH":
                                move_dir_y = -1
                            #Change char grid vars:
                            cur_char.cur_grid_x += move_dir_x
                            cur_char.cur_grid_y += move_dir_y

                            #Remove from prev room list:
                            cur_char.add_or_remove_char_from_room_list(cur_char.cur_room_id, False)
                            #Update cur_char room_id:
                            cur_char.update_cur_room_id()
                            # Add to new room list:
                            cur_char.add_or_remove_char_from_room_list(cur_char.cur_room_id, True)

                            print_room_recap = True
                            cur_char.cur_action_points -= 1
                            print(f"{cur_char.name} moves {parsed_str}. They now have {cur_char.cur_action_points} action points.")
                        else:
                            print("You need at least one action point to move to a different room.")
                    elif cur_room_inst_id.directional_dict[parsed_str] == ENUM_DOOR_LOCKED:
                        print(f"The {parsed_str}ERN door is locked.")
                    elif cur_room_inst_id.directional_dict[parsed_str] == ENUM_DOOR_JAMMED:
                        print(f"The {parsed_str}ERN door has been thoroughly jammed.")
                else:
                    print("There is a wall in that direction.")

            #endregion

            #region End Turn Logic:

            elif input_str == "END" or input_str == "END TURN":
                #Check for available action points and give a warning if characters still have unused action points:
                #Necessary?

                #Replenish all characters action points, reset 'new turn' type vars:
                for i in range(0,len(pc_char_list)):
                    pc_char_list[i].cur_action_points = pc_char_list[i].max_action_points
                    pc_char_list[i].participated_in_new_turn_battle = False
                    pc_char_list[i].already_fled_this_turn_boolean = False
                    pc_char_list[i].ability_points_cur += 1
                    #Cap:
                    if  pc_char_list[i].ability_points_cur > pc_char_list[i].ability_points_max:
                        pc_char_list[i].ability_points_cur = pc_char_list[i].ability_points_max
                print("You've ended your turn, some time has passed.")

                #Execute crisis events, if applicable:

                #Grow hazards:

                #Implement enemy movement ai--moving around the map, including smashing locked or jammed doors,
                #and/or indicating to the player that they are in the process of smashing a door:

                #Check to see if we need to start combat:
                enter_combat_boolean = check_combat_start(pc_char_list)
                if enter_combat_boolean:
                    cur_game_state = GAME_STATE_INITIALIZING_NEW_TURN

            #endregion

            #Print party list:
            elif input_str == "P" or input_str == "PARTY":
                for i in range(0,len(pc_char_list)):
                    print(f"{i}.) {pc_char_list[i].name}")
                print("")

            #Debug placeholder: exit game:
            elif input_str == "EXIT":
                print("You have decided to quit the game.")
                game_end = True

            #region Ambush logic:
            elif input_str == "AMBUSH":
                print("Ambush is not yet implemented.")
            #endregion

            #region Hide logic:
            elif input_str == "HIDE":
                print("Hide is not yet implemented.")
            #endregion

            #Reprint room and everything else:
            elif input_str == "L" or input_str == "LOOK":
                print_room_recap = True
                print("You take another look around and assess your situation:")
                print("")
            #Print char stats:
            elif input_str == "STAT" or input_str == "STATS":
                cur_char.print_char_stats()

            #region Scavenge logic:

            elif input_str == "SCAVENGE":
                #region Scavenge logic:
                room_scavenge_list = cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].scavenge_resource_list
                if isinstance(room_scavenge_list, list) and len(room_scavenge_list) > 0:
                    has_resources_boolean = False
                    for i in range(0,len(room_scavenge_list)):
                        if room_scavenge_list[i] != -1:
                            has_resources_boolean = True
                            break

                    if has_resources_boolean:
                        found_food, found_ammo, found_basic_tech, found_advanced_tech, found_fuel_total, found_credits_total = cur_grid_to_use[cur_char.cur_grid_y][cur_char.cur_grid_x].collect_scavenge_from_room(cur_char)
                        food_total += found_food
                        ammo_total += found_ammo
                        basic_tech_total += found_basic_tech
                        advanced_tech_total += found_advanced_tech
                        fuel_total += found_fuel_total
                        credits_total += found_credits_total
                    else:
                        print("This room has already been picked clean.\n")
                else:
                    print("There is nothing of value to be found in this room.")

            #endregion

            #Change game state to access inv:
            elif input_str == "INV" or input_str == "INVENTORY" or input_str == "I":
                cur_game_state = GAME_STATE_ACCESS_INV

            else:
                print("Invalid command, try again.")

        #endregion

        #region access_inv game state

        elif cur_game_state == GAME_STATE_ACCESS_INV:

            if combat_begun == False:
                inv_char = cur_char
            elif combat_begun:
                inv_char = cur_combat_char

            inv_char.print_char_inv()

            inv_input_str = input().upper().strip()

            show_item_desc_boolean = False
            drop_item_boolean = False
            give_item_boolean = False
            valid_selection = False
            item_index = -1

            if inv_input_str == "B" or inv_input_str == "BACK":
                if prep_combat_boolean:
                    cur_game_state = GAME_STATE_PREP_COMBAT
                elif not combat_begun:
                    cur_game_state = GAME_STATE_MAIN
                    print_room_recap = True
                elif combat_begun:
                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND

            elif inv_input_str.startswith("L"):
                show_item_desc_boolean = True
                try:
                    item_index = int(inv_input_str[1:])  # Everything after the "L"
                    valid_selection = True
                except ValueError:
                    pass
            elif inv_input_str.startswith("D"):
                drop_item_boolean = True
                try:
                    item_index = int(inv_input_str[1:])  # Everything after the "D"
                    valid_selection = True
                except ValueError:
                    pass
            elif inv_input_str.startswith("G"):

                if combat_begun == False:
                    chars_in_room_list = cur_room_inst_id.pcs_in_room_list
                else:
                    chars_in_room_list = cur_combat_room_id.pcs_in_room_list

                if isinstance(chars_in_room_list, list) and len(chars_in_room_list) > 1:
                    give_item_boolean = True
                    try:
                        item_index = int(inv_input_str[1:])  # Everything after the "G"
                        valid_selection = True
                    except ValueError:
                        pass
                else:
                    print(f"There is no one else in the same room as {inv_char.name} to give the item to.")
            else:
                try:
                    item_index = int(inv_input_str)
                    valid_selection = True
                except ValueError:
                    pass

            if valid_selection:
                if item_index >= 0 and item_index < len(inv_char.inv_list):
                    #Store item instance id:
                    selected_item = inv_char.inv_list[item_index]
                    if isinstance(selected_item, Item):
                        #'G' give an item to another player
                        if give_item_boolean:
                            if item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                                passing_item_id = selected_item
                                passing_item_index = item_index
                                cur_game_state = GAME_STATE_PASSING_ITEM
                            else:
                                print("You must unequip that item first.\n")

                        #'L'ook at item:
                        elif show_item_desc_boolean:
                            selected_item.print_item_desc()

                        #'D'rop item:
                        elif drop_item_boolean:
                            inv_char.drop_item_into_room(selected_item,item_index, inv_char.cur_grid[inv_char.cur_grid_y][inv_char.cur_grid_x])

                        # Use item:
                        elif selected_item.usable_boolean == True:
                            if not combat_begun:
                                passing_item_id = selected_item
                                passing_item_index = item_index
                                cur_game_state = GAME_STATE_USE_TARGET_ITEM
                            elif combat_begun and selected_item.combat_usable_boolean == True:
                                passing_item_id = selected_item
                                passing_item_index = item_index
                                cur_game_state = GAME_STATE_USE_TARGET_ITEM
                            elif combat_begun and selected_item.combat_usable_boolean == False:
                                print("That item can't be used in combat.\n")
                        else:
                            if selected_item.equippable_boolean == True:
                                #Determine if we need to unequip, equip, swap, or use item:
                                if item_index <= ENUM_EQUIP_SLOT_LH:
                                    if not combat_begun or prep_combat_boolean:
                                        #Unequip item, if it's already equipped as one of the equipment slots:
                                        inv_char.unequip_item(selected_item,item_index)
                                    else:
                                        if item_index == ENUM_EQUIP_SLOT_LH or item_index == ENUM_EQUIP_SLOT_RH:
                                            # Unequip item, if it's already equipped as one of the equipment slots:
                                            inv_char.unequip_item(selected_item, item_index)
                                        else:
                                            print("You don't have time to unequip body or accessory slots during combat.")
                                #Equip an item from one of the backpack slots:
                                elif item_index > ENUM_EQUIP_SLOT_LH:
                                    if not combat_begun or prep_combat_boolean:
                                        if inv_char.check_valid_item_equip(selected_item):
                                            inv_char.equip_item(selected_item,item_index)
                                    else:
                                        if isinstance(selected_item.equip_slot_list,list):
                                            #Check to see if our equip_slot_list contains the lh or rh macro we're looking for
                                            lh_or_rh_slot_boolean = check_equip_slot_list_for_rh_or_lh(selected_item.equip_slot_list)

                                            if lh_or_rh_slot_boolean:
                                                if inv_char.check_valid_item_equip(selected_item):
                                                    inv_char.equip_item(selected_item, item_index)
                                            else:
                                                print("You don't have time to equip body or accessory slots during combat.")
                                        else:
                                            print(f"Debug: Equipping items from backpack slots during combat: some use-case slipped through the cracks, "
                                                  f"we were trying to equip the {selected_item.item_name} but it is not an equippable item.")
                            else:
                                print(f"The {selected_item.item_name} is not an equippable item.")
                    else:
                        print("You must select an item, try again.")
                else:
                    print("Invalid selection, try again.")
            else:
                if cur_game_state != GAME_STATE_MAIN and cur_game_state != GAME_STATE_COMBAT_ASSIGN_COMMAND:
                    print("Invalid selection, try again.")

        #endregion

        #region Passing item game state or use_target_item game state

        elif cur_game_state == GAME_STATE_PASSING_ITEM or cur_game_state == GAME_STATE_USE_TARGET_ITEM:
            if cur_game_state == GAME_STATE_PASSING_ITEM:
                print("Pass item to which character in the same room?\n")
            else:
                print("Which character in the same room or rank should you use the item or ability on?\n")
            list_to_target = -1
            chars_in_room_list = []
            if combat_begun:
                list_to_target = cur_combat_room_id.pcs_in_room_list
                inv_char = cur_combat_char
            else:
                list_to_target = cur_room_inst_id.pcs_in_room_list
                inv_char = cur_char

            if isinstance(list_to_target, list) and len(list_to_target) > 1:
                for i in range(len(list_to_target)):
                    #Forbid chars in a different rank if we're in combat;
                    # And forbid the self if we're passing an item:
                    if combat_begun and list_to_target[i].cur_combat_rank != inv_char.cur_combat_rank:
                        continue
                    if cur_game_state == GAME_STATE_PASSING_ITEM and list_to_target[i] == inv_char:
                        continue
                    else:
                        chars_in_room_list.append(list_to_target[i])

            #Actually print our chars_in_room_list:
            for i in range(0,len(chars_in_room_list)):
                print(f"{i}.) {chars_in_room_list[i].name}")

            print("")
            print("Enter the character's corresponding number now. You can enter 'B' or 'BACKUP' at any time to return to the invetory screen: >")
            print("")
            input_str = input().upper().strip()
            if input_str == "B" or input_str == "BACKUP":
                if using_ability_boolean == False:
                    # return to inventory game state:
                    passing_item_index = -1
                    passing_item_id = -1
                    cur_game_state = GAME_STATE_ACCESS_INV
                elif using_ability_boolean:
                    # return to inventory game state:
                    passing_item_index = -1
                    passing_item_id = -1
                    cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
            else:
                try:
                    int_input = int(input_str)

                    if int_input >= 0 and int_input < len(chars_in_room_list):

                        valid_target_boolean = True

                        if combat_begun == True:
                            if cur_combat_char.cur_combat_rank != chars_in_room_list[int_input].cur_combat_rank:
                                valid_target_boolean = False

                        if valid_target_boolean:
                            if cur_game_state == GAME_STATE_PASSING_ITEM:
                                #Add to recipient's backpack:
                                chars_in_room_list[int_input].add_item_to_backpack(passing_item_id)  #add_item_to_backpack(item_id_to_add ,starting_equip_boolean = False):
                                #Remove from this char's backpack:
                                del inv_char.inv_list[passing_item_index]
                                #return to inventory game state:
                                passing_item_index = -1
                                passing_item_id = -1
                                cur_game_state = GAME_STATE_ACCESS_INV
                            else:
                                #Consume your AP BEFORE using the ability - useful for abils like stim prick
                                if using_ability_boolean == True:
                                    # Consume AP:
                                    inv_char.ability_points_cur -= passing_item_id.ability_point_cost

                                #Use item:
                                passing_item_id.use_item(chars_in_room_list[int_input])

                                #Destroy item, return to inv screen:
                                if using_ability_boolean == False:
                                    #Destroy item, if applicable; remove from this char's backpack:
                                    if passing_item_id.single_use_boolean:
                                        if passing_item_index >= ENUM_EQUIP_SLOT_TOTAL_SLOTS:
                                            del inv_char.inv_list[passing_item_index]
                                        else:
                                            inv_char.inv_list[passing_item_index] = -1

                                    #Return to inventory game state:
                                    passing_item_index = -1
                                    passing_item_id = -1
                                    cur_game_state = GAME_STATE_ACCESS_INV
                                #Consume AP, move to next char or return to ASSIGN COMMAND:
                                elif using_ability_boolean == True:

                                    #If we're in game and abil_passes_turn == TRUE, advance char;
                                    # otherwise if it == False, return to ASSIGN COMMAND
                                    if combat_begun:
                                        if passing_item_id.abil_passes_turn_boolean == True:
                                            # Advance cur_char:
                                            prev_cur_combat_char_index = combat_initiative_list.index(inv_char)

                                            cur_combat_char, cur_combat_round, cur_game_state, combat_initiative_list = advance_combat_cur_char(
                                                inv_char,
                                                combat_initiative_list,
                                                cur_combat_room_id,
                                                cur_combat_round,
                                                prev_cur_combat_char_index,
                                                f"DEBUG: Moving away from USE ABILITY ON PC TARGET, game_state == {cur_game_state}, cur_char {cur_combat_char.name} .")

                                            continue_str = input(
                                                "Press enter to continue to the next combatant in the initiative queue.")
                                            print("")
                                        else:
                                            #Return to assign combat command:
                                            passing_item_index = -1
                                            passing_item_id = -1
                                            cur_game_state = GAME_STATE_COMBAT_ASSIGN_COMMAND
                                    #If we're not in combat, return to our main game state:
                                    else:
                                        # Return to inventory game state:
                                        passing_item_index = -1
                                        passing_item_id = -1
                                        cur_game_state = GAME_STATE_MAIN
                        else:
                            invalid_pass_str = wrap_str("You must be occupying the same rank position as that character in order target them with this ability or pass them an item in combat.",TOTAL_LINE_W,False)
                            print(invalid_pass_str)

                    else:
                        print("That is not a valid character from the list, try again.")
                except ValueError:
                    print("You must select a valid integer, try again.")

            #endregion
        #endregion

        #Second to last thing in main loop:
        pygame.display.flip()

        #Very last thing in main loop:
        clock.tick(60)  # Limit to 60 frames per second (FPS)

    #If we've exited our main game loop, use pygame.quit() to remove all of the pygame modules from memory:
    pygame.quit()