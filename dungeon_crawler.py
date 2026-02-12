import random
import time
import sys
import json

# Player Class with Character Classes
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.inventory = []
        self.experience = 0
        self.level = 1

        # Class-based attributes
        if player_class == 'Warrior':
            self.attack += 5
            self.defense += 5
        elif player_class == 'Mage':
            self.attack += 10
            self.defense += 2
        elif player_class == 'Archer':
            self.attack += 7
            self.defense += 3

    def display_stats(self):
        print(f"Name: {self.name} | Class: {self.player_class} | Health: {self.health} | Attack: {self.attack} | Defense: {self.defense}")
        print(f"Level: {self.level} | Experience: {self.experience}")
        print("Inventory:", ", ".join(self.inventory) if self.inventory else "Empty")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def attack_enemy(self, enemy):
        damage = max(0, self.attack - enemy.defense)
        print(f"You attack the {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def level_up(self):
        if self.experience >= 100 * self.level:
            self.level += 1
            self.attack += 5
            self.defense += 3
            print(f"{self.name} leveled up to level {self.level}!")

# Enemy Class
class Enemy:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.health = 50 + (level * 10)
        self.attack = 8 + (level * 2)
        self.defense = 3 + (level * 1)

    def display_stats(self):
        print(f"{self.name} | Level: {self.level} | Health: {self.health} | Attack: {self.attack} | Defense: {self.defense}")

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack_player(self, player):
        damage = max(0, self.attack - player.defense)
        print(f"The {self.name} attacks you for {damage} damage!")
        player.take_damage(damage)

# Dungeon Generation with Traps and Secrets
def generate_dungeon(size=5, level=1):
    dungeon = []
    for _ in range(size):
        row = []
        for _ in range(size):
            # Randomly assign rooms, walls, or items
            room_type = random.choice(["empty", "enemy", "item", "trap", "secret", "exit"])
            row.append(room_type)
        dungeon.append(row)
    return dungeon

# Saving and Loading Game
def save_game(player, dungeon, filename="savegame.json"):
    save_data = {
        "player": {
            "name": player.name,
            "class": player.player_class,
            "health": player.health,
            "attack": player.attack,
            "defense": player.defense,
            "inventory": player.inventory,
            "experience": player.experience,
            "level": player.level,
        },
        "dungeon": dungeon
    }
    with open(filename, 'w') as file:
        json.dump(save_data, file)

def load_game(filename="savegame.json"):
    with open(filename, 'r') as file:
        save_data = json.load(file)
    player_data = save_data["player"]
    player = Player(player_data["name"], player_data["class"])
    player.health = player_data["health"]
    player.attack = player_data["attack"]
    player.defense = player_data["defense"]
    player.inventory = player_data["inventory"]
    player.experience = player_data["experience"]
    player.level = player_data["level"]
    return player, save_data["dungeon"]

# Main Game Loop
def main():
    print("Welcome to the Dungeon Crawler!")
    choice = input("Do you want to (n)ew game or (l)oad game? ").lower()

    if choice == 'n':
        name = input("Enter your character's name: ")
        player_class = input("Choose your class (Warrior, Mage, Archer): ")
        player = Player(name, player_class)
        dungeon_size = 5
        dungeon = generate_dungeon(dungeon_size)
    elif choice == 'l':
        player, dungeon = load_game()
    else:
        print("Invalid choice. Exiting.")
        return

    current_x, current_y = 0, 0  # Player's starting position
    level = 1

    while player.health > 0:
        print("\n" + "-"*30)
        print(f"Current Position: ({current_x}, {current_y})")
        player.display_stats()

        # Check the room type
        room = dungeon[current_x][current_y]

        if room == "enemy":
            print("\nYou encounter an enemy!")
            enemy = Enemy("Goblin", level)
            enemy.display_stats()
            action = input("Do you want to fight (f) or flee (l)? ")
            if action.lower() == "f":
                # Combat loop
                while player.health > 0 and enemy.health > 0:
                    player.attack_enemy(enemy)
                    if enemy.health > 0:
                        time.sleep(1)
                        enemy.attack_player(player)
                    time.sleep(1)
                    if player.health == 0:
                        print("\nYou have been defeated!")
                        break
                if enemy.health == 0:
                    print("\nYou defeated the enemy!")
                    player.experience += 20
                    player.level_up()
                    player.inventory.append("Health Potion")
                    dungeon[current_x][current_y] = "empty"
        elif room == "item":
            print("\nYou find a Health Potion!")
            player.inventory.append("Health Potion")
            dungeon[current_x][current_y] = "empty"
        elif room == "trap":
            print("\nOh no! You stepped on a trap!")
            player.take_damage(10)
            dungeon[current_x][current_y] = "empty"
        elif room == "secret":
            print("\nYou found a secret room with treasure!")
            player.inventory.append("Gold Coin")
            dungeon[current_x][current_y] = "empty"
        elif room == "exit":
            print("\nYou found the exit!")
            level += 1
            dungeon = generate_dungeon(dungeon_size, level)
            current_x, current_y = 0, 0
            print(f"Entering level {level}...")

        # Player move
        move = input("\nWhere do you want to go? (w/a/s/d) ")
        if move == "w" and current_x > 0:
            current_x -= 1
        elif move == "s" and current_x < dungeon_size - 1:
            current_x += 1
        elif move == "a" and current_y > 0:
            current_y -= 1
        elif move == "d" and current_y < dungeon_size - 1:
            current_y += 1
        else:
            print("Invalid move! Try again.")

        # Save the game
        save_choice = input("Do you want to save the game? (y/n): ")
        if save_choice.lower() == 'y':
            save_game(player, dungeon)

        time.sleep(1)

    print("Game Over!")

if __name__ == "__main__":
    main()
