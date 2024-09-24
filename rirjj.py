import sys
import random

# Define the player's starting attributes
player_inventory = []
player_health = 100

# A dictionary to hold the rooms and their descriptions
rooms = {
    'Entrance': {
        'description': 'You are standing at the entrance of a dark cave. You see paths to the north and east.',
        'items': ['torch'],
        'north': 'Hallway',
        'east': 'Storage Room'
    },
    'Hallway': {
        'description': 'You are in a narrow hallway. The air is damp and the walls are covered with moss. There is a passage to the south and north.',
        'items': [],
        'north': 'Treasure Room',
        'south': 'Entrance',
        'enemy': None
    },
    'Storage Room': {
        'description': 'This room is filled with old crates and broken tools. There is a door to the west. You notice a small key on the floor.',
        'items': ['key'],
        'west': 'Entrance',
        'enemy': None
    },
    'Treasure Room': {
        'description': 'You have entered a grand room filled with treasure! You see a large chest in the center.',
        'items': ['treasure'],
        'south': 'Hallway',
        'enemy': 'Goblin'
    },
    'Healing Room': {
        'description': 'You find yourself in a glowing room with a healing fountain. The air is calm and you feel rejuvenated.',
        'items': ['health_potion'],
        'west': 'Hallway',
        'enemy': None
    },
    'Locked Room': {
        'description': 'There is a locked door here. You need a key to open it.',
        'items': [],
        'south': 'Treasure Room',
        'north': 'Victory Room',
        'locked': True,
        'enemy': None
    },
    'Victory Room': {
        'description': 'Congratulations! You have entered the Victory Room and won the game!',
        'items': [],
        'enemy': None
    }
}

# Current room of the player
current_room = 'Entrance'

# Function to display the current room's details
def describe_room(room_name):
    room = rooms[room_name]
    print(f"\n{room['description']}")
    if room['items']:
        print(f"You see the following items: {', '.join(room['items'])}")
    if room.get('enemy'):
        print(f"An enemy is here: {room['enemy']}")

# Function to move between rooms
def move(direction):
    global current_room
    room = rooms[current_room]
    
    if direction in room:
        if room.get('locked') and 'key' not in player_inventory:
            print("The door is locked. You need a key to proceed.")
        else:
            current_room = room[direction]
            describe_room(current_room)
    else:
        print("You can't go that way.")

# Function to pick up items
def pick_up(item):
    global rooms, player_inventory
    room = rooms[current_room]
    
    if item in room['items']:
        player_inventory.append(item)
        room['items'].remove(item)
        print(f"You picked up: {item}")
    else:
        print("That item is not here.")

# Function to show player inventory
def show_inventory():
    if player_inventory:
        print(f"Your inventory: {', '.join(player_inventory)}")
    else:
        print("Your inventory is empty.")

# Function to handle combat
def combat(enemy):
    global player_health
    print(f"You are fighting a {enemy}!")
    while True:
        action = input("Do you want to (a)ttack or (r)un? ").lower().strip()
        if action == 'a':
            damage = random.randint(5, 15)
            print(f"You hit the {enemy} for {damage} damage!")
            if random.random() > 0.5:
                enemy_damage = random.randint(5, 10)
                player_health -= enemy_damage
                print(f"The {enemy} hits you for {enemy_damage} damage! Your health is now {player_health}.")
            if player_health <= 0:
                print("You have been defeated. Game Over.")
                sys.exit()
            else:
                print(f"You defeated the {enemy}!")
                rooms[current_room]['enemy'] = None
                break
        elif action == 'r':
            print("You ran away!")
            break
        else:
            print("Invalid action. Please choose 'a' to attack or 'r' to run.")

# Function to drink a health potion
def drink_potion():
    global player_health
    if 'health_potion' in player_inventory:
        player_health += 30
        player_inventory.remove('health_potion')
        print(f"You drink a health potion. Your health is now {player_health}.")
    else:
        print("You don't have any health potions.")

# Game loop
def game_loop():
    global player_health
    print("Welcome to the Expanded Adventure Game!")
    describe_room(current_room)
    
    while True:
        command = input("\n> ").strip().lower()
        
        if command in ['quit', 'exit']:
            print("Thanks for playing!")
            break
        
        elif command in ['look', 'l']:
            describe_room(current_room)
        
        elif command.startswith('go '):
            direction = command.split()[1]
            move(direction)
        
        elif command.startswith('take '):
            item = command.split()[1]
            pick_up(item)
        
        elif command in ['inventory', 'i']:
            show_inventory()
        
        elif command == 'drink potion':
            drink_potion()
        
        elif command == 'health':
            print(f"Your current health is {player_health}.")
        
        # Check for combat
        if rooms[current_room].get('enemy'):
            combat(rooms[current_room]['enemy'])

# Start the game
if __name__ == "__main__":
    game_loop()