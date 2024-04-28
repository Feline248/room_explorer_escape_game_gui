#Name: Rachel Dahl
#Game class that controls gameplay and GUI

from room import Room
from items import Item, Grabbable, SoundItem, CodeItem
import hints
from pygame import mixer
from random import choice
from time import sleep
from constants import *
from miscellaneous_functions import *




class Game(pygame.Surface):
    #define size of window
    WIDTH = 1525
    HEIGHT = 650
    
    def __init__(self):

        self.inventory = []
        self.response = ""
        self.entry_hall, self.kitchen, self.living_room, self.library, self.bathroom, self.attic, self.basement, self.greenhouse, self.escape = self.create_rooms()
        self.bonuses_found = 0
        self.message_box = pygame.Rect(Room.IMAGE_SIZE[0], 0, Game.WIDTH - Room.IMAGE_SIZE[0], Room.IMAGE_SIZE[1],)
        self.input_box = pygame.Rect(0, Room.IMAGE_SIZE[1], Game.WIDTH, Game.HEIGHT - Room.IMAGE_SIZE[1])
        
        #initialize pygame
        pygame.init()
        mixer.init()

        #Set up window
        radio_icon = pygame.image.load(os.path.join(os.path.join("room_explorer_graphics", "other"), "radio_icon.png"))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.window.fill(PAPER)
        pygame.display.set_caption("Room Explorer")
        pygame.display.set_icon(radio_icon)

        #set up text in window
        self.font = pygame.font.Font(os.path.join(os.path.join("room_explorer_graphics", "other"), "TravelingTypewriter.ttf"), FONT_SIZE)


    #getters/setters
    @property                               #inventory
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, new_value):
        self._inventory = new_value

    @property                               #room the player is in
    def current_room(self):
        return self._current_room

    @current_room.setter
    def current_room(self, new_value):
        self._current_room = new_value

    #additional methods
    def drop_item(self, item):
        self.inventory.remove(item)

    def create_rooms(self):

        #create the rooms
        entry_hall = Room("entry hall")
        kitchen = Room("kitchen")
        living_room = Room("living room")
        library = Room("library")
        bathroom = Room("bathroom")
        attic = Room("attic")
        basement = Room("basement")
        greenhouse = Room("greenhouse")
        bomb_shelter = Room("bomb shelter")
        escape = Room("escape")

        #lock rooms
        library.locked = True
        basement.locked = True
        greenhouse.locked = True
        escape.locked = True
        bomb_shelter.locked = True

        #set room descriptions
        entry_hall.room_description = "There's not much in here other than a coat hangar, an\numbrella stand, and a few cabinets and shelves. The\nfront door has roses carved into the doorframe\nand pink stained glass diamond windows on either side."
        kitchen.room_description = "It is dusty and looks like it hasn't been used in years.\nThe walls are covered in fading vine-patterned paper.\nAll of the appliances are old-fashioned lemon\nyellow enamel, with dark metal showing through where\nit's been chipped. There's a window on one side of the\nroom with tattered yellow and white checkered curtains,\nbut it's so choked in vines that you can't see out of it. "
        living_room.room_description = "You can hear the sound of rushing water in the\ndistance. There's a moldy-looking couch on the far side\nof the room. The floor has thick grayish brown carpet\nthat might have once been another color. You try\nyour best not to think about all\nthe health hazards in here."
        library.room_description = "The room is filled with floor to ceiling bookshelves\ncontaining every possible kind of book. Ancient leather\nbound tomes on obscure subjects, cheap paperback\nnovels, college textbooks, old journals and spiral\nbound notebooks, travel logs, atlases, and out of print\nencyclopedias. "
        bathroom.room_description = "The bathroom is small, but overall pretty\nnormal-looking. It has light blue tiles going about halfway up the\nwalls, with plain white paint above them. The\nsink and counter are linoleum made to look like marble."
        attic.room_description = "The attic has exposed wooden rafters along the slanted\nceiling and peeling pink flower patterned wallpaper.\nThere's a black rug with pink roses on it in the\ncenter of the room. It looks like there used to be\nwindows along one wall, but they're allboarded up."
        basement.room_description = "The basement is long and narrow, with a concrete floor\nand walls. It's almost empty, except for a few wooden\ncrates and a door at the opposite end from the\nstairs. There's a strange contraption next to the\ndoor. Maybe it's some kind of lock?"
        greenhouse.room_description = "It's completely overgrown with all kinds of plants.\nYou can hear the rain tapping against the glass above\nyou. There must be a leak somewhere keeping the\nplants alive."
        bomb_shelter.room_description = ""

        #add exits
        entry_hall.add_exit("north", greenhouse)            #entry hall
        entry_hall.add_exit("east", kitchen)

        kitchen.add_exit("west", entry_hall)                #kitchen
        kitchen.add_exit("up", attic)
        kitchen.add_exit("south", living_room)

        attic.add_exit("down", kitchen)                     #attic

        living_room.add_exit("north", kitchen)              #living room
        living_room.add_exit("west", library)

        library.add_exit("east", living_room)               #library
        library.add_exit("south", bathroom)
        library.add_exit("down", basement)

        basement.add_exit("up", library)                    #basement
        basement.add_exit("forward", escape)

        greenhouse.add_exit("south", entry_hall)            #greenhouse

        bathroom.add_exit("north", library)                 #bathroom

        # bomb_shelter.add_exit("", )                 #bomb shelter


        #add regular items
        entry_hall.add_item("shelf", "It has a few picture frames on it, but all of them are \nempty.")                                                                   #entry hall
        entry_hall.add_item("door", "The door still won't open. Maybe the latch broke?")

        greenhouse.add_item("red_pot", "A red flower pot with a sprawling succulent.\nThe label says 'Christmas Cactus'.")                                                                   #greenhouse
        greenhouse.add_item("blue_pot", "A tall, narrow pot with what looks like bamboo\ngrowing in it. Some of it has escaped and is\ngrowing up through cracks in the floor.")
        greenhouse.add_item("brown_pot", "A small pot with a shimmery brown glaze and\nwilty red and orange flowers.")
        greenhouse.add_item("broken_pot", "A few fragments of a light green ceramic\nflowerpot. There's dirt and dead leaves scattered\nacross the ground near it.")
        greenhouse.add_item("trellis", "A rotting wooden trellis is leaning against\nthe wall, threatening to collapse under the weight\nof long-dead vines.")
               
        kitchen.add_item("cabinet", "There's a set of wooden cabinets above the stove.\nInside you see a few cracked dishes and a box of matches.")                      #kitchen
        kitchen.add_item("chair", "There is a broken chair in one corner.")
        kitchen.add_item("flowers", "A glass vase of dried out roses sits on top of a\nbattered table. The flowers are shades of pale brownish\npink and yellow.")

        attic.add_item("bed", "One side of the room is occupied by a large bed\nwith flower-patterned sheets and blue pillows.")                                                                        #attic
        attic.add_item("armchair", "There's a leather airmchair in one corner.\nIt's very comfy.")
        attic.add_item("bowls", "There are two shallow bowls on the floor. They\nlook like they might be food and water dishes for a pet.")

        living_room.add_item("piano", "There is a beautiful piano in one corner of the room.\nIt has a piece of hand-written sheet music sitting on\ntop of it.")                                               #living room

        library.add_item("typewriter", "There's some paper sticking out. It says: \n'vc ccc./  n                     \n                     jnmfcdok.l,;'\nI think whoever lived here must have had a cat.")          #library
        library.add_item("book", "An old cookbook is laying on the desk. There's a\nhighlighted passage:\n'There's lots of debate over the best way to organize\nthe ingredients in a recipe, but I always like to put \nmine in alphabetical order by the ingredient name.'")
        library.add_item("globe", "An old fashioned globe, complete with doodles of\nsea monsters lurking in the ocean.")
        library.add_item("fireplace", "A large brick fireplace. It's too bad there's\nno wood, it's kind of cold in here.")

        bathroom.add_item("painting", "An oil painting of a bouquet of roses hangs on the \nwall across from the door.")                                                                     #bathroom
        bathroom.add_item("tiles", "One of the tiles on the wall is a slightly more\ngreenish color than the others. When you touch it,\nit comes loose. It has the symbols\n._.    .    _..      ._ _.    ._..    ._    _.    _ \nwritten on the back.")
      
        basement.add_item("shelf", "One wall is covered with rows of wooden shelves,\nbut they're all empty.")                                                                     #basement
        basement.add_item("door", "The door is securely locked. I'll have to find\nsome other way to get it open.")
        basement.add_item("contraption", "It looks a little like an old fashioned scale\nwith a cup on one of the trays. There's a bunch of\nwires running from it to the door.")
        basement.add_item("pipes", "There are some rusted pipes running along the ceiling.")
        
        bomb_shelter.add_item("portrait", "A large, beautiful portrait. It contains a\npicture of a frog wearing a hat.")                                                                     #bomb_shelter
        bomb_shelter.add_item("cereal", "A box of Cheeri Tori cereal. It's probably gone bad by now...")


        #add grabbables
        entry_hall.add_grabbable("umbrella", "It's made of plain black fabric with lacy edges.")                                                        #entry hall

        kitchen.add_grabbable("matches", "There's a box of matches inside one of the cabinets.\nI wonder if any of these still work?")                   #kitchen
        kitchen.add_grabbable("recipe", "A recipe card for some kind of candy. It reads:\n4 cups sugar\n4.5 cups water\n2 tsp lemon juice\n1 tsp lemon zest\n1 tsp cornstarch\n1 tsp cream of tartar\n1 tsp vanilla extract\n Melt sugar with\nThe rest of the recipe is too stained to read.") 

        greenhouse.add_grabbable("watering_can", "A dented, dull gray metal watering can full of water.")                                               #greenhouse

        attic.add_grabbable("letter", "A crinkled piece of paper that says:\nMy love, it has been far too long since we've\nseen each other. Someday we will be able to stay together,\nbut for now these letters are the best we can do.\nEven at a distance, the flames of our love are\nenough to keep me warm.")                                                       #library

        basement.add_grabbable("unlabeled_record", "An old record with no label on it that looks like it \nmight fit in the record player in the living room.")                                                                   #basement

        living_room.add_grabbable("sheet_music", "A piece of handwritten sheet music labeled with the \nnumber '16'. It looks unfinished, but the first notes are: \nC D E D C.")


        #add sound items
                                                                                                                #kitchen
        kitchen.add_sound_item("radio", "You turn on the old fashioned radio sitting on the\ncounter. You hear an eerie, monotone recording of\nsomeone reciting a list of numbers:\n10 4 101    47 108 32 101 47 52 52 10    20 5 108 4 20 5 20    \n32 93 207 0    207 15 88 14 5 0 0 207 304 5\n62 101 32    207 32    56 4 3 32    93 5 52 88\n10 4 101    207 3    32 93 5    17 47 15 5", "radio_with_static.wav")
                                                                                                                #living_room
        living_room.add_sound_item("gramophone", "You turn on the record player and hear a beautiful\nrecording of someone playing the flute. The tune sounds\nvaguely familiar.", "scarborough.wav")
        living_room.add_sound_item("window", "You look out the window, but all you can see is a dense\nfog and a few withered flowers in a long-forgotten\nwindow box. The sound of water is much louder here.", "waterfall.mp3")
                                                                                                                #bomb shelter



        #add code items
        entry_hall.add_code_item("cabinet", "There's an old filing cabinet with a combination lock \non it. It has the number 10 scratched on the side.", "843484")                              #entry hall
       
        living_room.add_code_item("door", "The door to the west has a large rotating combination \nlock on it.", "490713")                              #living room

        library.add_code_item("box", "There is an ornately carved wooden box with 8 dials \non it.", "11214145")                              #library

        attic.add_code_item("wardrobe", "There's a large wooden wardrobe near the door.\nInside, it's empty except for a coat and a few spare \npillowcases. There's a carving on the inside wall of 4\nconcentric circles with letters on them. They look like\nthey might be some kind of dials?", "rose")                              #attic

        #randomly generate code
        oven_code = ""
        for i in range(4):
            oven_code += choice(OVEN_SYMBOLS)

        kitchen.add_code_item("oven", "An oven/stove combo the same bright yellow as the rest\nof the kitchen. At first glance it seems pretty \nnormal, but the dials have strange symbols on them\ninstead of numbers or normal oven settings.", oven_code)

        #set current room
        self.current_room = entry_hall

        return entry_hall, kitchen, living_room, library, bathroom, attic, basement, greenhouse, escape





    def handle_go(self, direction):
        self.response = "Pretty sure you can't walk through walls."
        if direction in self.current_room.exit_directions:
            index = self.current_room.exit_directions.index(direction)

            if self.current_room.exit_destinations[index].locked == False:
                self.current_room = self.current_room.exit_destinations[index]
                self.response = "You walk into a new room."
                self.response += str(self.current_room)

            else:
                self.response = "The door is locked. It won't budge."

    def handle_look(self, item_observed):
        self.response = "You can't look at something that isn't here."
        for i in range(len(self.current_room.items)):
            temp = self.current_room.items[i]
            if temp.name == item_observed:
                self.response = str(temp)
                
                #play sound when player looks at a sound item
                if type(temp) == SoundItem:
                    mixer.music.stop()
                    temp.play_sound()
                    self.restart_bg_music()


                #kill player if they climb out the window
                if temp.name == "window":
                    self.response += "Try to escape by climbing out the window? y/n"

                    contemplating = True

                    while contemplating:
                        for event in pygame.event.get():

                            if event == pygame.KEYDOWN:

                                if event.key == K_y:
                                    self.death()
                                    contemplating = False
                                    RUNNING = False
                                    self.response = "..."
                                    break

                                if event.key == K_n:
                                    self.response = ("You step away from the window")
                                    contemplating = False
                                    self.update_graphics("")
                                    mixer.music.stop()
                                    self.restart_bg_music()

                #let player search for bonus record in fireplace once greenhouse has been unlocked
                if temp.name == "fireplace" and self.greenhouse.locked == False:
                    print(self.response)
                    answer = input("Reach into the chimney to look for hidden items? y/n")
                    if answer in ["y", "yes", "sure", "absolutely"]:
                        print("Your hand brushes against something. You pull out a record with a faded blue label on it.")
                        blue_record = Grabbable("blue_record", "A scratched, soot smeared record you found in the fireplace.")
                        self.inventory.append(blue_record)

                break


    def handle_take(self, item_grabbed):
        self.response = "You can't pick that up."
        for i in range(len(self.current_room.items)):
            temp = self.current_room.items[i]
            if temp.name == item_grabbed and type(temp) == Grabbable:
                self.inventory.append(temp)
                self.current_room.items.pop(self.current_room.items.index(temp))
                self.response = f"You pick up the {item_grabbed}."
                break

    def handle_drop(self, item_dropped):
        self.response = "You can't drop an item that you're not holding."
        for i in range(len(self.inventory)):
            temp = self.inventory[i]
            if temp.name == item_dropped:
                self.current_room.items.append(temp)
                self.inventory.remove(temp)
                self.response = f"You drop the {item_dropped}"

    def handle_use(self, item):
        self.response = "I don't see a way I could use that here."
        
        #inventory items
        for i in range(len(self.inventory)):
            search = self.inventory[i]
            if search.name == item and search.single_use == False:

                #add key to player's invnentory when umbrella is opened
                if item == "umbrella":
                    self.response = "You open the umbrella. A tiny gold key with an intricately carved treble clef on it falls out."
                    tiny_key = Grabbable("tiny_key", "A tiny gold key with an intricately carved treble clef on it")
                    self.inventory.append(tiny_key)
                    search.single_use = True
                
                    break


                #reveal hidden message on letter with matches
                if item == "matches":
                    for i in range(len(self.inventory)):
                        temp = self.inventory[i]
                        if temp.name == "letter":
                            self.response = "You light a match under the letter and a hidden message\ntakes shape. It says 'escape below. 49 07 13.'"
                            temp.description += "\nThere's a message written between the lines in\ninvisible ink that says 'escape below. 49 07 13.'"
                            temp.single_use = True

                    break

                #unlock greenhouse
                if item == "flower_key":
                    if self.current_room.name == "entry hall":
                        self.response = "You unlock the door."
                        self.greenhouse.locked = False
                        search.single_use = True

                    elif self.current_room.name == "library":
                        self.response = "You try the key, but it doesn't fit in this door"

                    else:
                        self.response = "There's nothing here for me to unlock."

                    break


                #unlock basement
                if item == "rusty_key":
                    if self.current_room.name == "library":
                        self.response = "You unlock the door."
                        self.basement.locked = False
                        search.single_use = True

                    elif self.current_room.name == "entry_hall":
                        self.response = "You try the key, but it doesn't fit in this door"

                    else:
                        self.response = "There's nothing here for me to unlock."

                    break


                #fill scale with water and unlock escape
                if item == "watering_can" and self.current_room.name == "basement":
                    self.response = "You pour some of the water from the watering can into the cup on the scale and watch it balance out.\nThe door creaks open, finally giving you a chance to escape."
                    self.escape.locked = False
                    search.single_use = True

                    break

                #switch records in gramophone
                if item == "green_record" and self.current_room.name == "living room":
                    for i in range(len(self.current_room.items)):
                        temp = self.current_room.items[i]
                        if temp.name == "gramophone":

                            if temp.sound_file == "desperate_record_cut.mp3":
                                unlabeled_record = Grabbable("unlabeled_record", "An old record with no label on it that looks like it might fit in the record player in the living room.")
                                self.inventory.append(unlabeled_record)

                            if temp.sound_file == "bonus_record_full.wav":
                                blue_record = Grabbable("blue_record", "A scratched, soot smeared record you found in the fireplace.")
                                self.inventory.append(blue_record)
                            
                            temp.sound_file = "scarbourogh.wav"
                            temp.description = "You turn on the record player and hear a beautiful recording of someone playing the flute. The tune sounds vaguely familiar."
                            self.response = "You switch the records in the gramophone"
                            self.inventory.remove(search)
                            break

                    break

                #switch records in gramophone
                if item == "unlabeled_record" and self.current_room.name == "living room":
                    for i in range(len(self.current_room.items)):
                        temp = self.current_room.items[i]

                        if temp.name == "gramophone":

                            if temp.sound_file == "scarborough.wav":
                                green_record = Grabbable("green_record", "A record with a green and gold label that says 'Variations on Scarborough Fair'.")
                                self.inventory.append(green_record)

                            if temp.sound_file == "bonus_record_full.wav":
                                blue_record = Grabbable("blue_record", "A scratched, soot smeared record you found in the fireplace.")
                                self.inventory.append(blue_record)
                            
                            temp.sound_file = "desperate_record_cut.mp3"
                            temp.description = "The gramophone plays a recording of someone saying:\n'I don't have much time. I'm sorry it had to come to this, but you need to leave.\nThe code is your favorite flower, and remem-' *loud crash*\nThe recording stops abruptly."
                            self.response = "You switch the records in the gramophone"
                            self.inventory.remove(search)
                            break
                    
                    break

                #switch records in gramophone
                if item == "blue_record" and self.current_room.name == "living room":
                    for i in range(len(self.current_room.items)):
                        temp = self.current_room.items[i]
                        if temp.name == "gramophone":
                            if temp.sound_file == "desperate_record_cut.mp3":
                                unlabeled_record = Grabbable("unlabeled_record", "An old record with no label on it that looks like it might fit in the record player in the living room.")
                                self.inventory.append(unlabeled_record)

                            if temp.sound_file == "scarborough.wav":
                                green_record = Grabbable("green_record", "A record with a green and gold label that says 'Variations on Scarborough Fair'.")
                                self.inventory.append(green_record)
                            
                            temp.sound_file = "bonus_record_full.wav"
                            temp.description = "An excerpt of an orchestral piece. At the end, however, someone says:\n'Congratulations on finding this bonus! Now get back to the game.'"
                            self.response = "You switch the records in the gramophone"
                            self.inventory.remove(search)
                            self.bonuses_found += 1
                            break
                    
                    break



                #play music box
                if item == "tiny_key":
                    for i in range(len(self.current_room.items)):
                        temp = self.current_room.items[i]
                        if temp.name == "music box":
                            self.response = str(self.entry_hall.music_box)
                            self.response += "You put the key in the music box and wind it up."

                            mixer.music.load(os.path.join("room_explorer_audio", "flight_of_the_confused_pigeon.mp3"))
                            mixer.music.play()
                            for i in range(10):
                                pass
                            self.restart_bg_music()

                            self.bonuses_found += 1
                    break
                           

                else:
                    self.response = "I can't use an item I don't have."


        #Code Items
        if item in ["cabinet", "door", "box", "wardrobe"]:
            for i in range(len(self.current_room.items)):
                search = self.current_room.items[i]
                if search.name == item:
                    self.response = "Nothing happens. You must have entered the wrong code."

                    #unlock cabinet and add music box to room
                    if item == "cabinet" and self.current_room.name == "entry hall":

                        attempt = self.input_code()

                        if attempt == search.correct_code:
                            self.response = "The cabinet opens. Inside, you see a small music \nbox with a keyhole in it."
                            self.entry_hall.add_sound_item("music box", "A small wooden music box with a keyhole. \nAn engraving on the bottom says\n'Congratulations! You solved a set of extra-hard \npuzzles and found one of the bonuses!\nPlease enjoy this music as a reward.'", "flight_of_the_confused_pigeon.mp3")

                        break


                    #unlock box and add basement key to the player's inventory
                    if item == "box":
                        attempt = self.input_code()
                        if attempt == search.correct_code:
                            self.response = "The box pops open. Inside, you find a large, \nrusted key. You put the key in your pocket."
                            rusty_key = Grabbable("rusty_key", "A large, plain, rust-covered key.")
                            self.inventory.append(rusty_key)

                        break



                    #unlock secret compartment and add greenhouse key to the player's inventory
                    if item == "wardrobe":
                        attempt = self.input_code()
                        if attempt == search.correct_code:
                            self.response = "A secret compartment slides open! In it, you find a pretty \nsilver key with a flower engraved on the end. You put the \nkey in your pocket."
                            flower_key = Grabbable("flower_key", "A small silver key with a flower-shaped handle.")
                            self.inventory.append(flower_key)

                        break



                    #unlock library door
                    if item == "door" and self.current_room.name == "living room":
                        attempt = self.input_code()
                        if attempt == search.correct_code:
                            self.response = "You hear a click and the door unlocks."
                            self.library.locked = False

                        break


                
    def handle_inventory(self):
        """print player's inventory"""

        if len(self.inventory) != 0:
            self.response = f"\n You are carrying: "
            for i in range(len(self.inventory)):
                self.response += f"\n{self.inventory[i].name} --- {self.inventory[i].description}\n"

        else:
            self.response = "You have no items in your inventory"

    
    def handle_help(self):
        """print instructions"""

        controls = open(os.path.join("room_explorer_info", "controls.txt"))
        self.response = controls.read()
        controls.close()

    
    def handle_map(self):
        """display a map of the building"""

        house_map = open(os.path.join("room_explorer_info", "house_map.txt"))
        self.response = house_map.read()
        house_map.close()


    def handle_room_description(self):
        """re-print room description"""

        self.response = str(self.current_room)


    def handle_special(self, action:str):
        """Deals with special actions and Easter eggs"""

        if action in ["scream", "aaa", "temporarily go insane" ]:
            self.response = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!"
            self.response += "\nI feel much better now."
            mixer.music.stop()
            mixer.music.load(SCREAM)
            mixer.music.set_volume(0.7)
            mixer.music.play()
            sleep(3)
            self.restart_bg_music()
        
        if action == "escape":
            self.response = "Wow, that's a great idea. I wish I had thought of that earlier."

        if action in ["magic", "teleport", "time travel"]:
            self.response = "I mean I guess I could, but that feels like cheating"

        if action in ["cry", "boo hoo", "wahhh"]:
            self.response = "No, I can't give up hope yet."

        if action in ["burn house", "arson", "light everything on fire", "commit arson"]:
            self.response = "I don't have anything to start a fire with."
            for i in range(len(self.inventory)):
                temp = self.inventory[i]
                if temp.name == "matches":
                    self.response = "You set fire to the room. If you can't get out, you'll take the whole house with you."
                    RUNNING = False

        if action in ["celebrate", "woop woop", "cheer"]:
            self.response = "Yay! I accomplished something!"



    #gives player a hint based on the room they're in
    def hint(self):
        self.response = hints.default_hint

        #first hint for each room
        if self.current_room.hints_used == 0:
            if self.current_room.name == "greenhouse":
                self.response = hints.greenhouse_hint_0
            if self.current_room.name == "entry hall":
                self.response = hints.entry_hall_hint_0  
            if self.current_room.name == "kitchen":
                self.response = hints.kitchen_hint_0
            if self.current_room.name == "attic":
                self.response = hints.attic_hint_0  
            if self.current_room.name == "living_room":
                self.response = hints.living_room_hint_0
            if self.current_room.name == "basement":
                self.response = hints.basement_hint_0 
            if self.current_room.name == "library":
                self.response = hints.library_hint_0
            if self.current_room.name == "bathroom":
                self.response = hints.bathroom_hint_0  

        #2nd hint
        if self.current_room.hints_used == 1:
            if self.current_room.name == "greenhouse":
                self.response = hints.greenhouse_hint_1
            if self.current_room.name == "entry hall":
                self.response = hints.entry_hall_hint_1  
            if self.current_room.name == "kitchen":
                self.response = hints.kitchen_hint_1
            if self.current_room.name == "attic":
                self.response = hints.attic_hint_1  
            if self.current_room.name == "living_room":
                self.response = hints.living_room_hint_1
            if self.current_room.name == "library":
                self.response = hints.library_hint_1

        #3rd hint
        if self.current_room.hints_used == 2:
            if self.current_room.name == "entry hall":
                self.response = hints.entry_hall_hint_2  
            if self.current_room.name == "kitchen":
                self.response = hints.kitchen_hint_2
            if self.current_room.name == "attic":
                self.response = hints.attic_hint_2  

        self.current_room.hints_used += 1
        



    def play(self):

        #intro cutscene
        intro = "Due to your incredible planning skills, the 'fun hike' you had\nplanned turned out to be pretty"
        intro += "unpleasant. Not only are you completely\nlost, you also forgot to check the weather, and it started\n"
        intro += "pouring rain. Luckily, you found an old house to take shelter\nin. It looks like it's been abandoned"
        intro += "for decades, but at least it's dry.\nAs you close the door behind you, you hear a loud crack.\n"
        intro += "You try to open the door to see what it was, and realize too late\nthat the sound didn't come from"
        intro += "outside. It was the door itself.\nIt's firmly stuck, and now you'll need to find another way out."
        intro += "\n\n\t\t\t\t\t\tPress enter to begin."

        self.draw_text(intro, pygame.Rect(Game.WIDTH / 4, Game.HEIGHT / 4, Game.WIDTH / 2, Game.HEIGHT / 2))
        pygame.display.update()
        
        print(intro)
        mixer.music.load(STORM)
        mixer.music.set_volume(0.7)
        mixer.music.play()


        paused = True
        while paused:
            for event in pygame.event.get():
                #end game when x button or escape key is pressed
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    paused = False
                    break
                
                elif (event.type == QUIT):
                    paused = False
                    break

                elif event.type == KEYDOWN and event.key == K_RETURN:
                    paused = False
                    break


        mixer.music.stop()

        print(self.current_room)
        self.response = str(self.current_room)
        pygame.draw.rect(self.window, PAPER, pygame.Rect(Game.WIDTH / 4, Game.HEIGHT / 4, Game.WIDTH / 2, Game.HEIGHT / 2))
        self.update_graphics(" ")


        #set up background music
        self.restart_bg_music()


        RUNNING = True
        action = ""

        while (RUNNING):

            #did we win?
            if self.current_room == self.escape:
                self.win()
                RUNNING = False
                break
                

            #end game when x button or escape key is pressed
            for event in pygame.event.get():
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    RUNNING = False
                    break
                
                elif (event.type == QUIT):
                    RUNNING = False
                    break

                #get user input

                if event.type == pygame.KEYDOWN: 
                
                    # Check for backspace 
                    if event.key == K_BACKSPACE:  
                        action = action[:-1] 

                    elif event.key == K_RETURN: #finalize input and send that string to the next part of the code
                        self.evaluate_input(action)
                        self.response += "\nWhat would you like to do?"
                        print(self.response)
                        action = ""

                    # add to string
                    else: 
                        action += event.unicode
                        action = action.lower()

                    
                    self.update_graphics(action)

        ending = True
        while ending:
            for event in pygame.event.get():
                #end game when x button or escape key is pressed
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    ending = False
                    break
                
                elif (event.type == QUIT):
                    ending = False
                    break


                



    def death(self):
        print("As you climb out of the window, you realize suddenly that there is nothing underneath you.\nThe house was on the edge of a cliff! It quickly disappears into the mist as you fall to your death.\n")
        self.window.blit(DEATH_SCREEN, (0, 0))
        RUNNING = False


    def win(self):
        mixer.music.stop()
        print("You walk through a dark stone tunnel. After a while, you come to a spiral staircase descending deep into the earth.\nYou can hear rushing water nearby. At the bottom of the stairs, you discover a huge cave with a lake in it.\nThere's a boat near the edge of the lake, and in front it you can see daylight through the waterfall\nthat hides the entrance to the cave from the outside. You take the boat and follow the river back to civilization at last.")
        print(f"\nYou completed the game!\nYou found {self.bonuses_found}/3 bonuses. Play again to find them both!\n")
        RUNNING = False
        self.credits()


    def credits(self):
        
        mixer.init()
        mixer.music.load(CREDITS)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        self.response = ("\t\tRoom Explorer")
        self.update_graphics("")
        sleep(3)

        self.response = ("\nCode:\n\nRachel Dahl")
        self.response += ("\n\nSpecial thanks to Brandon Jones for helping me debug")
        self.update_graphics("")
        sleep(5)

        self.response = ("\nMusic:\n\n'Variations on Scarborough Fair'\nwritten by Calvin Custer and performed by Cas Curry\n\n'Flight of the Confused Pigeon' by Rachel and Lexi Dahl\n\n'Inverse' by Rachel Dahl\n\nAll other music and sound effects from Pixabay")
        self.update_graphics("")
        sleep(6)

        self.response = ("\nVoice Acting:\n\nNumbers station - Rachel Dahl\n\nDesperate recording - Brandon Jones\n\nBonus Record - Lexi Dahl")
        self.update_graphics("")
        sleep(5)

        self.response = ("\nGraphics:\n\nWallpapers/Background Images - \nRawpixel, Deviant Art, Freepik, Depositphotos, \nFlickr, PickPik, Stockvault, Wikimedia Commons, Creazilla\n\n3D Models - Rachel Dahl\n\nFont - Traveling Typewriter by Carl Krull")
        self.update_graphics("")
        sleep(6)

        self.response = ("\nPuzzle Ideas Assistance:\n\nBrandon Jones\n\nCaleb Davis\n\nAbby Mikulski\n\nChuck Pealer\n\nElia Browning")
        self.update_graphics("")
        sleep(5)
        
        self.response = ("\nTypewriter message:\n\nWinnifred (my cat)")
        self.update_graphics("")
        sleep(5)

        self.response = ("\nBeta Testing:\n\nLexi Dahl\n\nCaleb Davis\n")
        self.update_graphics("")
        sleep(5)

        self.response = ""
        self.update_graphics("")
        sleep(25)


        self.response = ("\nYou're still here? The game's over. Go home.")
        self.update_graphics("")
        sleep(7)

    
    def update_graphics(self, action):
        """updates images and text shown on screen"""

        #images
        self.window.blit(self.current_room.image, (0,0))

        #blank out old text
        pygame.draw.rect(self.window, PAPER, self.message_box)
        pygame.draw.rect(self.window, PAPER, self.input_box)

        #text
        self.draw_text(self.response, self.message_box)

        self.draw_text(action, self.input_box)

        pygame.display.update()


    def draw_text(self, text:str, rect:pygame.Rect):
        current_y = rect.top
        font_height = self.font.size("Tg")[1]

        text = text.split("\n")

        for line in text:
            #render text to screen
            self.window.blit(self.font.render(line, False, INK, PAPER), (rect.left, current_y))
            #move to next line
            current_y += font_height + LINE_SPACING


        
    def evaluate_input(self, action:str):

        #create response for this loop
        self.response = "Invalid input. Try the format [verb] [noun]."
        self.response += "\nType 'a' for a list of accepted commands."

        #end game
        if action in ["x","exit", "quit", "bye", "q", "farewell"]:
            RUNNING = False

        #extra actions
        if action in [
        "scream", 
        "aaa", 
        "temporarily go insane", 
        "escape", 
        "magic", 
        "teleport", 
        "time travel", 
        "cry", 
        "boo hoo", 
        "wahhh", 
        "burn house", 
        "arson", 
        "light everything on fire", 
        "commit arson", 
        "celebrate", 
        "woop woop", 
        "cheer"]:
            self.handle_special(action)
        

        #print a list of all items in inventory
        if action in ["i", "inventory"]:
            self.handle_inventory()
        
        #print the list of accepted commands
        if action in ["a", "controls", "help"]:
            self.handle_help()

        #print the map
        if action in ["m", "map"]:
            self.handle_map()
           
        #run credits sequence
        if action in ["c", "credits"]:
            self.credits()

        #print room description again
        if action in ["r", "room"]:
            self.handle_room_description()
        
                
        if action in ["h", "hint"]:
            self.hint()

        words = action.split(" ")
        if len(words) == 2:
            verb = words[0]
            noun = words[1]

            if verb in ["g", "go"]:
                self.handle_go(noun)
            elif verb in ["l", "look", "inspect"]:
                self.handle_look(noun)
            elif verb in ["t", "take", "grab"]:
                self.handle_take(noun)
            elif verb in ["d", "drop", "remove"]:
                self.handle_drop(noun)
            elif verb in ["u", "use"]:
                self.handle_use(noun)


    def input_code(self)->str:
        self.response = "Type your guess for the code below:"
        self.update_graphics("")
                    
        typing = True
        attempt = ""

        while typing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: 
            
                    # Check for backspace 
                    if event.key == K_BACKSPACE:  
                        attempt = attempt[:-1]

                    elif event.key == K_RETURN: #finalize input and send that string to the next part of the code
                        typing = False

                    # add to string
                    else: 
                        attempt += event.unicode
                        attempt = attempt.lower().replace(" ", "")

                    self.update_graphics(attempt)

        return attempt



    def restart_bg_music(self):
        """adjusts volume and restarts normal background 
        music after another sound is played"""
        mixer.music.set_volume(0.4)
        mixer.music.load(BG_MUSIC)
        mixer.music.play()

