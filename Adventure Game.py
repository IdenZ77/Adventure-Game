class Player:
    def __init__(self, starting_room, inventory=None, HP=None):
        if inventory is None:
            inventory = []
        if HP is None:
            HP = int(100)
        self.current_room = starting_room
        self.HP = HP
        self.inventory = inventory

    # reports health attribute of player via print
    def status(self):
        print(f"Player Health: {self.HP}")

    # prints inventory attribute of player
    def check_inv(self):
        if self.inventory == []:
            print("My inventory is empty...")
        elif self.inventory != []:
            print("My inventory consists of:")
            for item in self.inventory:
                print(f"a(n) {item.item}")

    # function to move to another room, takes an argument.
    def move_to(self, new_room):
        # checks if an item is required to go to the room, if there is it will check your inventory to see if you have the item, if you don't have it it will tell you to go look for the item.
        if new_room.required_item != None:
            if new_room.required_item in self.inventory:
                self.current_room = new_room
                # lets the player know
                print(f"Success! All I needed was the {new_room.required_item.item}")
                print(f"I entered the new room, {self.current_room.room_desc}")
            elif new_room.required_item not in self.inventory:
                print(f"Sorry, it looks like you need an item to get through this door")
        if new_room.required_item == None:
            self.current_room = new_room
            print(f"{self.current_room.room_desc}")

    # iterates through the room object list, printing the .item method (name) of each game object stored within the room's list.
    def look_around(self):
        print(f"In this room I see:")
        for item in self.current_room.room_items:
            print(f"{item.item}")
        for item in self.current_room.other_rooms:
            print(f"{item.room}")

    # this function allows you to grab items, it iterates through the rooms list and checks if the item_name argument is equivalent to the .item method (name) of the game object, if it is, the object is appended to
    # the inventory list and is removed from the room's list.
    def grab(self, item_name):
        if len(self.inventory) == 4:
            print("My inventory is full, I can only hold 4 items... I should drop something")
        elif len(self.inventory) < 4:
            for item in self.current_room.room_items:
                if item.item.lower() == item_name.lower():
                    print(f"I just added {item.item} to my inventory!")
                    self.inventory.append(item)
                    self.current_room.room_items.remove(item)

    # Pretty much just a reverse of the grab function.
    def drop(self, item_name):
        for item in self.inventory:
            if item.item.lower() == item_name.lower():
                print(f"I just droped the {item.item}")
                self.current_room.room_items.append(item)
                self.inventory.remove(item)

    # inspect function, first for loop checks if argument (item_name) is same as .item method of index item (which is a game object) if it is it continues to check if the item does damage, if it does it lets you know it damaged you
    # second for loop does the same thing but tells you .item_desc of item if there is one.
    def inspect(self, item_name):
        for item in self.current_room.room_items:
            if item.item.lower() == item_name.lower():
                if item.DMG > int(0):
                    self.HP = self.HP - item.DMG
                    print(f"Oh no! Something was wrong with the {item.item} you just took: {item.DMG} damage!")
        for item in self.current_room.room_items:
            if item.item.lower() == item_name.lower():
                if item.item_desc != None:
                    print(f"{item.item_desc}")
                elif item.item_desc == None:
                    print(f"Not much else to it, its just a(n) {item.item}")

    # function to check .clue attribute of the item and report it back to you
    def clue(self, item_name):
        for item in self.current_room.room_items:
            if item.item.lower() == item_name.lower():
                if item.hint != None:
                    print(f"Here is the clue: {item.hint}")
                elif item.hint == None:
                    print(f"No clues found for: {item.item}")


# class for game objects, allows me to create new instances throughout the game, contains name of item, description of item, and hint if I choose to give the item a hint as well as a requirement like a key.
class game_object:
    def __init__(self, item, item_desc=None, hint=None, DMG=int(0)):
        self.item = item
        self.item_desc = item_desc
        self.hint = hint
        self.DMG = DMG


# This is a class to create a game room with the name of the room, a description of the room, and a list consisting of game objects (instances of the game_object class)
class game_room:
    def __init__(self, room, room_desc, other_rooms=None, room_items=None, required_item=None, enemy_char=None):
        if room_items is None:
            room_items = []
        if other_rooms is None:
            other_rooms = []
        if enemy_char == None:
            enemy_char = []
        self.other_rooms = other_rooms
        self.room = room
        self.room_desc = room_desc
        self.room_items = room_items
        self.required_item = required_item

#class for enemy type, this is just for the wizard.
class enemy:
    def __init__(self, starting_room, name, desc, clue, required=[], needed=None, happiness=int(0)):
        if needed == None:
            needed = []
        self.name = name
        self.desc = desc
        self.clue = clue
        self.required = required
        self.happiness = happiness
        self.starting_room = starting_room
        self.needed = needed

#function to give items to the wizard, he has a list (self.needed) consisting of his needed items, and an empty list. The function compares the item you're trying to give to the wizard with his list of needed items
#if it is a match this function appends the item to his required list (originally empty) once he has his four items in his inventory you win, each append increases his happiness by 25, 4 times 25 = 100, once the wizard.happiness
#equals 100 the while loop in the game_loop function breaks ending the game.
    def give(self, item_name):
        for item in player.inventory:
            if item.item.lower() == item_name.lower():
                if item in self.needed:
                    self.required.append(item)
                    player.inventory.remove(item)
                    self.happiness += 25
                    print(f"The {item.item} was one of the wizard's required items! You are now %{round((int(self.happiness) / int(100) * int(100)))} of the way out of here!")
                elif item not in self.needed:
                    print(f"The {item.item} was not one of the wizard's required items.")

#simple function to check the wizard's inventory
    def check_wiz(self):
        for item in self.required:
            print(f"Items in wizard's inventory:")
            print(f"{item.item}")

#snack game objects
Doritos = game_object("Bag of Chips","This appears to be a bag of flaming hot doritos! So Spicy!","Could this be the snack the wizard wants?",25)
Sour = game_object("Cylinder of Snacks","This appears to be a pringles sour cream and onion!","Could this be the snack the wizard wants?")
Funyun = game_object("Bag of Onion Snacks","This appears to be a bag of funyuns!","Could this be the snack the wizard wants? I mean I like funyuns but I don't know how many other people like them...")
Gummy = game_object("Bag of Gummy Snacks","This is a bag of gummy worms, ouch the sour kind!","Could this be the snack the wizard wants?",15)
Lays = game_object("Family Size Chips","This is just a bag of Lay's potato chips, kinda basic.","Maybe the wizard has some 'vanilla' preferences?")

#comic game objects
Spider_man = game_object("Comic Book with Red Superhero","This is issue #14 of the original Spiderman Comic Series! A classic! Oh gosh a spider is on it!","Could this be the comic the wizard wanted?",5)
Xmen = game_object("Comic Book with an X on it","This is a classic XMEN comic, super cool! It's not in mint condition though...","Could this be the comic the old wizard wanted?")
Superman = game_object("Comic Book with Blue Guy","This is a classic Superman Comic! It's in mint condition! The lamination is kind of sharp...","Could this be the comic the old wizard wanted?",7)

#misc objects
OldBook = game_object("Old Book","This book looks to be centuries old, the cover implies it covers spells!","On the last page there is a written in clue: A key marks the path to my favorite comic book!")
Computer = game_object("Old Computer","This is a super old PC which appears to be running Windows Vista, yikes.","I found a file called 'do not enter PRIVATE!' it says snack preference: hot to the touch")
Mirror = game_object("Mirror on the Wall","This mirror is smudged, oh my a ghost has appeared in it's reflection! It just spit on me...",None,20)
Roller = game_object("Roller","This is a hair roller, usually used by balding men, it's spikey!",None,5)
iphone = game_object("Iphone 13","This is just a midnight black iphone, mint condition","Is the wizard an apple guy?")
BB = game_object("Blackberry","This is an old Blackberry phone, it used to be considered 'smart' but I don't know...","The wizard is old, maybe his phone preferences are older too?")
android = game_object("Samsung Galaxy S9","This is a Samsung Galaxy S9, a crack runs on the back from top to bottom","Is the wizard an android guy?")

#medication objects
Med1 = game_object("Orange Pill Bottle","This is Lexapro","Could this be the medication the Wizard was wanting?")
Med2 = game_object("Blue Medical Bottle","This is Rogaine, I wonder if the Wizard is balding?","Could this be the medication the Wizard was wanting?")
Med3 = game_object("White Medical Bottle","This is allergy medication","Could this be the medication the Wizard was wanting?")

#key objects, some required for progression.
Key1 = game_object("Rusty Key","This key is super rusty and sharp to the touch!","Could this open a door somewhere?",5)
Key2 = game_object("Fancy Key","This key is made out of gold with white stripes!","Could this open a door somewhere?")
Key3 = game_object("Old Key","This is an old key, a little dull but not sharp!","Could this open a door somewhere?")
Key4 = game_object("Basic Key","This is a basic key","Could this open a door somewhere?")

#rooms
Room1 = game_room("Wooden Door", "Wood all over like a cabin! It's a little 'musky' in here")
Room2 = game_room("Metal Door", "This room is full metal, like literally, 'full of metal' from the floors to the ceiling...")
Room3 = game_room("Cobblestone Door", "This room is made out of Mossy Cobblestone!")
Cell1 = game_room("Rusty Cell Door", "This is a really rusty prison cell, smells fishy")
Cell2 = game_room("Fancy Door", "This room is so fancy! Red velvet drapes and hard-wood flooring!")
Room4 = game_room("Screen Door", "This is a room that looks to be an exact replica of Peter Griffin's living room...")
Wizard_Hall = game_room("The Wizard Hall", "Everything in the room is super clean with gold flooring along with strange self-portraits on the wall, its giving squidward vibes")

#I found trouble with setting the arguments above for referencing items and other rooms, this is because the code runs top to bottom and I can't reference Room2 in Room1 if Room2 object hasn't been created yet
#so I append the items to each parameter below
Room1.other_rooms = [Room2, Room3,Wizard_Hall]
Room1.room_items += [Xmen, Gummy, Key4]
Room2.other_rooms = [Cell1, Room4]
Room2.room_items += [android, Sour, Mirror, Roller, Med2, Key3]
Room3.other_rooms = [Room4, Room1, Cell2]
Room3.room_items += [Key1, OldBook, Funyun]
Cell1.other_rooms = [Room2]
Cell1.room_items += [Spider_man, Med1, Doritos]
Cell1.required_item = Key1
Cell2.other_rooms = [Room3]
Cell2.room_items += [iphone, Med3, Superman]
Cell2.required_item = Key2
Room4.other_rooms = [Room2, Room3]
Room4.room_items += [BB, Key2]
Wizard_Hall.other_rooms = [Room1]
Wizard_Hall.room_items += [Computer, Lays]

#creates wizard character and player character
wizard = enemy(Wizard_Hall, "The Evil Wizard","Bro has not showered in ages, his big white beard is touching the ground","My spell binds your soul to this place, if you want to leave I need 4 items: My snack, my smartphone, my comic book, and my medication! I'm about to sneeze!",[],[Doritos,Med3,Spider_man,android])
player = Player(Wizard_Hall)

print("""Welcome to Iden's Text Based Adventure Game!
This game features an inventory system, a health system, and the use of classes in Python to store attributes to allow you to move around the world!
You are a lost adventurer stuck in a dungeon and you must escape! You are in the wizard's hall, type inspect wizard to talk to the wizard to know what to do!
To get started type help to see a list of commands to use, enjoy!""")

#game loop runs on while look while the wizard's happiness does not equal 100 and as long as your personal health is above 0.
def game_loop():
    while wizard.happiness != int(100) and player.HP > 0:
        command = input("\nType Command:").strip().lower()
        #everything below is just input processing.
        if command == "help":
            print("\nlook \nplayer health \ninspect 'item' \nenter 'room name' \ninventory \ngrab 'item' \ndrop 'item' \ngive 'item \nclue 'item' \ncheck wizard inventory \nglance at wizardh \ntalk to wizard")

        elif command == "look":
            player.look_around()

        elif command == "player health":
            player.status()

        elif command == "inventory":
            player.check_inv()

        elif command.startswith("inspect "):
            item_name = command[8:]
            player.inspect(item_name)

        elif command.startswith("grab "):
            item_name = command[5:]
            player.grab(item_name)

        elif command.startswith("drop "):
            item_name = command[5:]
            player.drop(item_name)

        elif command.startswith("clue "):
            item_name = command[5:]
            player.clue(item_name)

        elif command.startswith("enter "):
            room_name = command[6:]
            for rooms in player.current_room.other_rooms:
                if rooms.room.lower() == room_name.lower():
                    player.move_to(rooms)

        elif command.startswith("give "):
            item_name = command[5:]
            if player.current_room == Wizard_Hall:
                wizard.give(item_name)
            elif player.current_room != Wizard_Hall:
                print("You must be in the Wizard Hall to interact with the Wizard!")
        #code makes sure the player's current room is equal to the wizard hall i.e where the wizard is, if it is not it will tell you to go to the wizard hall to interact with the wizard
        #check wizard inventory, glance at wizard, and talk to wizard all have this logic applied
        elif command == "check wizard inventory":
            if player.current_room != Wizard_Hall:
                print("You must be in the Wizard Hall to interact with the Wizard!")
            elif player.current_room == Wizard_Hall:
                if wizard.required == []:
                    print("There is nothing in the Wizard's inventory...")
                elif wizard.required != []:
                    wizard.check_wiz()

        elif command == "glance at wizard":
            if player.current_room != Wizard_Hall:
                print("You must be in the Wizard Hall to interact with the Wizard!")
            elif player.current_room == Wizard_Hall:
                print(f"{wizard.desc}")

        elif command == "talk to wizard":
            if player.current_room != Wizard_Hall:
                print("You must be in the Wizard Hall to interact with the Wizard!")
            elif player.current_room == Wizard_Hall:
                print(f"{wizard.clue}")
        #if none of the user input matches any of the processing logic above it tells you to enter a valid command
        else:
            print("Incorrect command, please type help to see a list of commands!")

    #code to run when loop breaks, either you win, or you lose.
    if wizard.happiness == 100 and player.HP > 0:
        print("""The Wizard has all his items he lost, he appreciates your help because he has ADHD and loses track of everything!
        he lifts the spell and sets you free! You win!""")
    elif player.HP <= 0:
        print("You died, please try again.")

game_loop()

