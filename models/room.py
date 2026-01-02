
from constants import *
from models.item import Item

from collections import Counter
import random
import textwrap

class Room:

    def __init__(self ,location_type_enum,room_type_enum ,grid_x ,grid_y,location_grid):

        # Instance vars for each room:
        self.tech_count = 0
        self.credits_count = 0
        self.food_count = 0
        self.cover_int = 0  # 0:none; 1: small amount of cover; 2: medium amount; 3: plenty of useful cover.
        self.powered_status_boolean = False
        self.unpowered_room_desc = "Not defined"
        self.powered_room_desc = "Not defined"
        self.scavenged_once_boolean = False
        self.already_explored_boolean = False

        # keyword_interaction_dict - used for room feature keywords associated with this room
        self.keyword_interaction_dict = {}

        # directional dictionary
        self.directional_dict = {}

        # Initialize to 0:
        self.scavenge_resource_list = []
        for i in range(0, ENUM_SCAVENGE_TOTAL_RESOURCES):
            self.scavenge_resource_list.append(0)

        #enemies_in_room_list and pcs_in_room_list:
        self.enemies_in_room_list = -1
        self.pcs_in_room_list = -1
        self.neutrals_in_room_list = -1

        self.grid_x = grid_x
        self.grid_y = grid_y
        self.room_type_enum = room_type_enum
        self.location_type_enum = location_type_enum
        self.room_name = "Not defined"
        self.location_grid = location_grid

        if self.location_type_enum == ENUM_LOCATION_NIFFY:

            if self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_BASIC_NORTH_SOUTH:
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0 ,3)
                self.unpowered_room_desc = [ "This basic corridor only serves as a connection between two areas on the ship. The floor is metal grating and the walls are dirty panels of burnished steel. A few piles of refuse lay scattered about, evidence of the vessel's disuse." ]
                self.directional_dict["NORTH"] = ENUM_DOOR_UNLOCKED
                self.directional_dict["SOUTH"] = ENUM_DOOR_UNLOCKED
                self.room_name = "NIFFY BASIC NS CORRIDOR"
            elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_BASIC_EAST_WEST:
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0 ,3)
                self.unpowered_room_desc = [ "This basic corridor only serves as a connection between two areas on the ship. The floor is metal grating and the walls are dirty panels of burnished steel. A few piles of refuse lay scattered about, evidence of the vessel's disuse." ]
                self.directional_dict["EAST"] = ENUM_DOOR_UNLOCKED
                self.directional_dict["WEST"] = ENUM_DOOR_UNLOCKED
                self.room_name = "NIFFY BASIC EW CORRIDOR"
            elif self.room_type_enum == ENUM_ROOM_NIFFY_STORAGE_ROOM:
                self.cover = 2
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = random.randint(0 ,3)
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED] = 1
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = random.randint(0 ,2)
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_CREDITS] = random.randint(0 ,2)
                self.unpowered_room_desc = [ "Racks of mostly empty shelving and opened boxes indicate that this room was once used for storage. Dust and debris are mostly all that remain. It looks as though the most important items have been pilfered already. The whirling red flare of the emergency lights overhead sends strange shadows pin-wheeling across the room." ]
                self.room_name = "NIFFY STORAGE ROOM"
            elif self.room_type_enum == ENUM_ROOM_NIFFY_HYDROPONICS_LAB:
                self.cover = 1
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = random.randint(0, 2)
                self.unpowered_room_desc = [ "Rows and rows of metal grow boxes line the room, their contents nothing more than withered weeds to clutching to dry, gray dirt. There's a nest of hydraulics and hoses in the walls, and huge sunlamps are recessed in the ceiling, now dark and inert. If you can restore power to this room, perhaps there's a way to get these hydroponics working again?" ]
                self.powered_room_desc = [ "The rows of hydroponics buzz happily with spray from the moisture pumps, while the leafy green vegetables within eagerly drink the light from the sunlamps overhead. These crops of potatoes, beans, and cabbages have clearly been genetically modified to grow quickly." ]
                self.room_name = "NIFFY HYDRO LAB"
            elif self.room_type_enum == ENUM_ROOM_NIFFY_STASIS_CHAMBER:
                self.cover = 1
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 3
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_FOOD] = 15
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_AMMO] = 17
                self.scavenge_resource_list.append(Item(ENUM_ITEM_SUIT_ENVIRONMENTAL))
                self.scavenge_resource_list.append(Item(ENUM_ITEM_MEDKIT))

                self.directional_dict["EAST"] = ENUM_DOOR_UNLOCKED
                self.directional_dict["WEST"] = ENUM_DOOR_UNLOCKED
                self.room_name = "NIFFY STASIS ROOM"

                self.unpowered_room_desc = [
                    "Klaxons blare, and an eerie red illumination seeps from the emergency lights in the floor. Row upon row of stasis pods have been arranged in this room, most of them shattered or inoperable. Those corpses who had sought refuge within them have met a truly ignoble end, asphyxiated in their sleep. There's only one STASIS POD that still looks operational and inviting, gleaming pearl-white in the blood-hued gloom.",
                    "The room itself has been badly damaged. Refuse and debris lay scattered about, along with piles of personal effects: whatever non-essential items the sleepers had stripped from their bodies before hastily clamboring within the statis pods to seal their doom.",
                    "Hull stresses and fractures have fissured the walls and ceiling, exposing pipes and electrical wires. One particularly damaged PIPE is rapidly venting a noxious green gas, caustic enough to make you sputter and gag. A nearby exposed service panel reveals two huge circular valves: a BRONZE VALVE and a STEEL VALVE.",
                    "The cover of the service panel looks as though it was torn off with some haste, almost as though someone was determined to access these valves but soon abandoned their task; you can only speculate as to why."
                ]
            elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_SR_WEST:
                self.cover = 1
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 1
                self.room_name = "NIFFY SR CORRIDOR W"

                self.directional_dict["EAST"] = ENUM_DOOR_UNLOCKED
                self.directional_dict["WEST"] = ENUM_DOOR_JAMMED

                self.unpowered_room_desc = [
                    "The air smells foul and stuffy in this narrow corridor, and is suffused with the same ominous dim red light. The floor is metal grating and the walls are made up of panels of burnished steel.",
                    "A shadowed and inert form is slumped against the western bulkhead door, as if in peaceful repose. Upon closer inspection, you can see that the man is one of the security forces on board, if his military fatigues and body armor are any indication. You can also see that he is very dead: his eyes stare lifelessly at the jagged hole in his abdomen beneath his flak vest, admiring the great heap of coiled intestines that lay piled between his legs.",
                    "If your eyes aren't mistaken in the gloomy light, there's a strangely colored, green goo clinging to the edges of the gaping wound, and more of it dribbling from his mouth. The CORPSE is also clutching a pistol in a death grip. Judging by the bloody hole in the side of his head, it looks as though his last act was to use the weapon on himself.",
                    "The self-inflicted head wound, combined with the abyss where the man's stomach used to be, has certainly given you pause. Nonetheless, the CORPSE is carrying some useful looking gear, and there could be more in the pockets of his tactical vest. Is it wise to take a closer look?"
                ]
            elif self.room_type_enum == ENUM_ROOM_NIFFY_CORRIDOR_SR_EAST:
                self.cover = 1
                self.scavenge_resource_list[ENUM_SCAVENGE_RESOURCE_TECH_BASIC] = 1
                self.room_name = "NIFFY SR CORRIDOR E"

                self.directional_dict["EAST"] = ENUM_DOOR_LOCKED
                self.directional_dict["WEST"] = ENUM_DOOR_UNLOCKED

                self.unpowered_room_desc = [
                    "There's an NPC in this room."
                ]

            else:
                print \
                    (f"Constructor event for Room class: room_type_enum: {room_type_enum} not captured by if case for location_type_enum {location_type_enum}")

    def print_room_directions(self):
        print("The following directions are available to you:")

        if len(self.directional_dict) > 0:
            for key, value in self.directional_dict:
                move_dir_x = 0
                move_dir_y = 0
                if key == "WEST":
                    move_dir_x = -1
                elif key == "NORTH":
                    move_dir_y = -1
                elif key == "EAST":
                    move_dir_x = 1
                elif key == "SOUTH":
                    move_dir_y = 1
                door_state_str = "undefined"
                if value == ENUM_DOOR_UNLOCKED:
                    door_state_str = "UNLOCKED DOOR"
                elif value == ENUM_DOOR_JAMMED:
                    door_state_str = "JAMMED DOOR"
                elif value == ENUM_DOOR_DESTROYED:
                    door_state_str = "DESTROYED DOOR"
                elif value == ENUM_DOOR_LOCKED:
                    door_state_str = "LOCKED DOOR"
                elif value == ENUM_DOOR_OPEN_SPACE:
                    door_state_str = "OPEN SPACE"

                room_name_str = ""
                if self.location_grid[self.grid_y+move_dir_y][self.grid_x+move_dir_x].already_explored_boolean:
                    room_name_str = ": "+self.location_grid[self.grid_y+move_dir_y][self.grid_x+move_dir_x].room_name
                    if isinstance(self.location_grid[self.grid_y+move_dir_y][self.grid_x+move_dir_x].enemies_in_room_list,list):
                        if len(self.location_grid[self.grid_y+move_dir_y][self.grid_x+move_dir_x].enemies_in_room_list) > 0:
                            room_name_str += ": (...Enemies lurk here...)"

                print(f"{key}: {door_state_str}{room_name_str}")


    def print_room_desc(self):
        if not self.powered_status_boolean:
            for i in self.unpowered_room_desc:
                room_str = textwrap.fill(i, TOTAL_LINE_W)
                print(room_str)
                print("")

        else:
            for i in self.powered_room_desc:
                room_str = textwrap.fill(i, TOTAL_LINE_W)
                print(room_str)
                print("")

    def collect_scavenge_from_room(self ,scavenging_char_id):
        #Define instance level vars, these will be returned to our main.py file:
        food_total, ammo_total, basic_tech_total, advanced_tech_total, fuel_total, credits_total = 0, 0, 0, 0, 0, 0
        # This will cause our main loop to show any items on the floor in this room:
        self.scavenged_once_boolean = True

        output_str = f"{scavenging_char_id.name} has found the following items in this room:\n"

        for i in range(0 ,len(self.scavenge_resource_list)):
            if i == ENUM_SCAVENGE_RESOURCE_FOOD:
                if self.scavenge_resource_list[i] > 0:
                    food_total += self.scavenge_resource_list[i]
                    output_str += f"+{self.scavenge_resource_list[i]} FOOD.\n"
            elif i == ENUM_SCAVENGE_RESOURCE_AMMO:
                if self.scavenge_resource_list[i] > 0:
                    ammo_total += self.scavenge_resource_list[i]
                    output_str += f"+{self.scavenge_resource_list[i]} AMMUNITION.\n"
            elif i == ENUM_SCAVENGE_RESOURCE_TECH_BASIC:
                if self.scavenge_resource_list[i] > 0:
                    basic_tech_total += self.scavenge_resource_list[i]
                    output_str += f"+{self.scavenge_resource_list[i]} BASIC TECHNOLOGY.\n"
            elif i == ENUM_SCAVENGE_RESOURCE_TECH_ADVANCED:
                if self.scavenge_resource_list[i] > 0:
                    advanced_tech_total += self.scavenge_resource_list[i]
                    output_str += f"+{self.scavenge_resource_list[i]} ADVANCED TECHNOLOGY.\n"
            elif i == ENUM_SCAVENGE_RESOURCE_FUEL_ENGINE:
                if self.scavenge_resource_list[i] > 0:
                    fuel_total += self.scavenge_resource_list[i]
                    plural_s = ""
                    if self.scavenge_resource_list[i] > 1:
                        plural_s = "S"
                    output_str += f"+{self.scavenge_resource_list[i]} NEUTRONIUM FUEL CELL{plural_s}.\n"
            elif i == ENUM_SCAVENGE_RESOURCE_CREDITS:
                if self.scavenge_resource_list[i] > 0:
                    credits_total += self.scavenge_resource_list[i]
                    plural_s = ""
                    if self.scavenge_resource_list[i] > 1:
                        plural_s = "S"
                    output_str += f"+{self.scavenge_resource_list[i]} CREDIT{plural_s}.\n"
            elif i >= ENUM_SCAVENGE_TOTAL_RESOURCES:
                # We are now adding items to the scavenging_char_id's inv_list:
                if isinstance(self.scavenge_resource_list[i], Item):
                    scavenging_char_id.add_item_to_backpack(self.scavenge_resource_list[i])
                    output_str += f"+{self.scavenge_resource_list[i].item_name}.\n"

        # Actually print the massive string we just created:
        print(output_str)

        # Delete the list but keep the variable
        self.scavenge_resource_list = -1
        self.scavenge_resource_list = []
        # Initialize:
        for i in range(0 ,ENUM_SCAVENGE_TOTAL_RESOURCES +1):
            self.scavenge_resource_list.append(-1)

        return food_total, ammo_total, basic_tech_total, advanced_tech_total, fuel_total, credits_total

    def print_scavenge_list_item(self):
        item_found = False
        items_found_str = "There are the following items in this room:\n"
        if len(self.scavenge_resource_list) >= ENUM_SCAVENGE_TOTAL_RESOURCES+1:
            for i in range(ENUM_SCAVENGE_TOTAL_RESOURCES,len(self.scavenge_resource_list)):
                if isinstance(self.scavenge_resource_list[i], Item):
                    item_found = True
                    items_found_str += self.scavenge_resource_list[i].item_name+"\n"

        if item_found:
            print(items_found_str)

    def print_char_list(self,char_team_enum):
        if char_team_enum == ENUM_CHAR_TEAM_PC:
            ar_to_use = self.pcs_in_room_list
        elif char_team_enum == ENUM_CHAR_TEAM_ENEMY:
            ar_to_use = self.enemies_in_room_list
        else:
            ar_to_use = self.neutrals_in_room_list

        if isinstance(ar_to_use, list) and len(ar_to_use) > 0:
            if ar_to_use == self.pcs_in_room_list:
                print("There are the following playable characters in this room:")
                for i in range(0,len(ar_to_use)):
                    print(f"{ar_to_use[i].name}")
                print("")
            else:
                team_str = "enemy"
                if char_team_enum == ENUM_CHAR_TEAM_NEUTRAL:
                    team_str = "friendly"
                # Count occurrences by name using Counter obj from imports
                name_counts = Counter(char.name for char in ar_to_use)
                # Print results
                print(f"There are the following {team_str} characters in this room:")
                for name, count in name_counts.items():
                    plural_str = ""
                    if count > 1:
                        plural_str = f"({count})"
                    print(f"{name} {plural_str}")
                print("")



