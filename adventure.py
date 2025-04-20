from __future__ import annotations
import json
from datetime import datetime, timedelta
import random
from typing import Optional
from game_entities import Location, Item
from proj1_event_logger import Event, EventList


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - _locations: Mapping from ID to location object
        - _items: a list of items held by the player
        - current_location_id: ID of current location
        - ongoing_sim:  bool 1 is True if game is being played, False if it has ended,
                        and bool 2 determines if the game is simmed.
        - inventory: a list of all Items held by the player
        - score: The current amount of points held by the player
        - turnsleft: The number of turns you can take before the game ends

    Representation Invariants:
        - current_location_id > 0
        - turnsleft >= 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing_sim: list[bool]  # Suggested attribute, can be removed
    inventory: list[Item]
    score: int
    turnsleft: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        self._locations, self._items = self.load_game_data(game_data_file)

        for k in self._locations:
            self._locations[k].items = {j: self.get_item(j) for j in self._locations[k].items}

        self.current_location_id = initial_location_id
        self.ongoing_sim = [True, False]
        self.inventory = []
        self.score = 0

    @staticmethod
    def load_game_data(filen: str) -> tuple[dict[int, Location], dict[str, Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filen, 'r') as fl:
            data = json.load(fl)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    [loc_data['available_commands'], loc_data['items'], False])
            locations[loc_data['id']] = location_obj

        items = {}
        for itemdata in data["items"]:
            item = Item(itemdata["name"], itemdata["description"], itemdata["start_position"],
                        itemdata["target_position"], itemdata["target_points"])
            items[itemdata["name"]] = item

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def get_item(self, itemid: str) -> Item:
        """Return Item object associated with ID."""
        return self._items[itemid]

    def sim(self) -> None:
        "Sets game.ongoing_sim[1] to True to signal that this game is being simmed."
        self.ongoing_sim[1] = True


if __name__ == "__main__":

    game_log = EventList()

    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit", "drop",
            "submit"]
    choice = None

    game.turnsleft = 25  # Adjust maximum turns here
    lastcommand = None
    choice2 = None

    # Timer not required, can be commented out
    duration = timedelta(seconds=600)
    stime = datetime.now()

    while game.ongoing_sim[0]:
        print(game.ongoing_sim[1])
        elapsed = datetime.now() - stime
        remtime = duration - elapsed
        location = game.get_location()

        game_log.add_event(Event(location.id_num, location.long_description, None, None, None), choice)

        if not game.get_location().visited:
            game.get_location().visited = True
            temp = game.get_location().long_description.split(" ")
            res = [" ".join(temp[y:y + 25]) for y in range(0, len(temp), 25)]
            for x in res:
                print(x)
            print()

        else:
            temp = game.get_location().brief_description.split(" ")
            res = [" ".join(temp[z:z + 25]) for z in range(0, len(temp), 25)]
            for w in res:
                print(w)
            print()

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit, drop, submit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and choice not in location.items:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        # print("====================")
        print("You decided to:", choice)
        if choice in menu:
            helditems = [itm.name for itm in game.inventory]
            if choice == "log":
                game_log.display_events()
            if choice == "submit":
                if (
                        location.id_num == 4
                        and (
                        all(
                            game.get_item(it1) in game.inventory
                            for it1 in ["charger", "lucky mug", "usb drive"]
                        )
                        or all(
                        it2 in game.get_location().items.keys()
                        for it2 in ["charger", "lucky mug", "usb drive"]
                        )
                        )
                ):

                    game.ongoing_sim[0] = False
                    print()
                    print("You've successfully submitted the assignment on time. Congratulations!!")
                    print(f"Final score: {game.score}")
                else:
                    print("You need to be in your dorm room with your charger, lucky mug, and usb drive to submit!")
            if choice == "drop":
                if len(game.inventory) > 0:
                    choice2 = input("\nEnter item: ").lower().strip()
                    while choice2 not in helditems:
                        print(f"The {choice2} is not in your inventory, try again.")
                        choice2 = input("\nEnter item: ").lower().strip()
                    if game.get_item(choice2).target_position == game.get_location().id_num:
                        game.inventory.pop(game.inventory.index(game.get_item(choice2)))
                        print(f"You dropped a {choice2} in your dorm room!",
                              f"You got {game.get_item(choice2).target_points} points!")
                        game.score += game.get_item(choice2).target_points
                        game.get_location().items[choice2] = game.get_item(choice2)

                    else:
                        print("Don't drop this off here! You should bring it back to your dorm room.")
                else:
                    print("Your inventory is empty.")

            if choice == "inventory":
                print()
                print("You currently have: ")
                if len(game.inventory) == 0:
                    print("Your inventory is empty.")
                else:
                    res = []
                    for i in game.inventory:
                        print(f"{i.name}: {i.description}")
            if choice == "score":
                print(f"Current score: {game.score}")
            if choice == "quit":
                game.ongoing_sim[0] = False
            if choice == "undo":
                if lastcommand is None:
                    print("You can't undo on turn 1!")
                elif lastcommand in game.get_location(game_log.last.prev.id_num).available_commands:
                    game_log.remove_last_event()
                    game.current_location_id = game_log.last.id_num
                    game.turnsleft += 1
                elif lastcommand in helditems:
                    game.inventory.pop(game.inventory.index(game.get_item(lastcommand)))
                    location.additem(game.get_item(lastcommand))
                    game.score -= game.get_item(lastcommand).target_points
                    if lastcommand == "lucky mug":
                        game.inventory.append(game.get_item("tcard"))
                elif lastcommand == "undo":
                    print("You can't undo an undo command!")
                elif lastcommand == "drop":
                    if choice2 is not None:
                        game.get_location().takeitem()
                        game.inventory.append(game.get_item(choice2))
                        game.score -= game.get_item(choice2).target_points
                    else:
                        print("You didn't drop anything during your last action.")

                else:
                    print("Invalid. Last action did not change gamestate.")

            if choice == "look":
                temp = game.get_location().long_description.split(" ")
                res = [" ".join(temp[t:t + 25]) for t in range(0, len(temp), 25)]
                for r in res:
                    print(r)
        elif choice in location.items:
            if not game.ongoing_sim[1]:
                if choice.lower().strip() == "lucky mug".lower().strip() and game.get_location().id_num == 7:
                    print("The porter says, 'do you have your TCard?'")
                    if game.get_item("tcard") in game.inventory:
                        game.inventory.pop(game.inventory.index(game.get_item("tcard")))
                        game.inventory.append(game.get_item("lucky mug"))
                        game.score += game.get_item("lucky mug").target_points
                        print("You show the porter your TCard, and in return you get the lucky mug!")
                elif choice.lower().strip() == "charger" and game.get_location().id_num == 3:
                    print("You go to where you were studying earlier, and you see your charger plugged into the wall!")
                    print("You ask the person sitting there to get the charger for you, ")
                    print("but they insist that you beat them in a best of 5 rock paper scissors match!")
                    options = ["rock", "paper", "scissors"]
                    scores = [0, 0]
                    while scores[0] < 3 and scores[1] < 3:
                        inpt = ""
                        cpu = options[random.randint(0, 2)]
                        while inpt not in options:
                            inpt = input("\nEnter your move: ").lower().strip()
                        if inpt == cpu:
                            print("Tie! try again.")
                        elif (inpt == "rock" and cpu == "scissors") or (inpt == "scissors" and cpu == "paper"):
                            scores[0] += 1
                            print(f"Opponent's move: {cpu}")
                            print(f"Current score: {scores[0]}-{scores[1]}")
                        elif inpt == "paper" and cpu == "rock":
                            scores[0] += 1
                            print(f"Opponent's move: {cpu}")
                            print(f"Current score: {scores[0]}-{scores[1]}")
                        else:
                            scores[1] += 1
                            print(f"Opponent's move: {cpu} ")
                            print(f"Current score: {scores[0]}-{scores[1]}")
                    if scores[0] > scores[1]:
                        print("You won! You received your charger!")
                        game.inventory.append(game.get_item("charger"))
                        game.score += game.get_item("charger").target_points
                        location.takeitem("charger")
                        game.turnsleft -= 1
                    else:
                        game.turnsleft -= 1
                        print("You lost! try again.")
                elif choice.lower().strip() == "USB drive".lower().strip() and game.get_location().id_num == 6:
                    print("You take the elevator up to the 6th floor lecture room. Could this be where the USB is?")
                    print("The class taking place just ended, so you go to where you were sitting earlier today.")
                    print("There is someone there, and next to them on the ground you see your USB!")
                    print("You ask them to grab it for you, but they said that it was theirs!")
                    print("You get into an argument, but the other person won't budge.")
                    print()
                    print(
                        "Finally, they challenge you to a game: 'Beat these two word games and i'll give you the key!'")
                    print()
                    print("Game 1: Wordle! You have 6 guesses.")
                    print("-O-: correct, -/-: in the word but incorrect position, -X-: not in word.")
                    filename = "words.txt"
                    words = []
                    with open(filename) as f:
                        for line in f:
                            words.append(line[0:5])
                    index = random.randint(0, len(words) - 1)
                    choice3 = ""
                    goal = words[index]
                    correct = False
                    turns = 6
                    while choice3 != goal and not correct and turns > 0:
                        check = []
                        choice3 = input("\nEnter a 5 letter word: ").lower().strip()
                        print(f"Goal: {goal}")
                        if not isinstance(choice3, str) or len(choice3) != 5 or choice3 not in words:
                            print("Please enter a valid 5 letter word: ")
                        else:
                            print("====================")
                            if list(choice3) == list(goal):
                                correct = True
                                print("You got it!")
                            else:
                                ind = 0
                                for char in list(choice3):
                                    if char in list(goal) and list(choice3)[ind] == list(goal)[ind]:
                                        check.append("-O-")
                                    elif char in list(goal):
                                        check.append("-/-")
                                    else:
                                        check.append("-X-")
                                    ind += 1
                            print(f"Your entry: {choice3}")
                            print(f"result: {check}")
                            turns -= 1
                            print(f"Turns left: {turns}")
                            if correct:
                                print()
                                print("Game 2: Beat this word unscrambling game to receive the USB drive!")
                                print(
                                    "You will have 5 scrambled words, and you need to guess what the original word is.")
                                print("Hint: The words are related to your life as a CS student at UofT! ")
                                words = ["Computer", "Science", "Toronto", "University", "Canada", "Ontario", "Project"]
                                correct = True
                                random.shuffle(words)
                                for i in words[0:5]:
                                    if correct:
                                        temp = list(i)
                                        random.shuffle(temp)
                                        print("".join(temp))
                                        inp = input("\nUnscrambled word: ")
                                        if inp.lower() == i.lower():
                                            print("Correct!")
                                        else:
                                            print("Incorrect. You'll have to try again!")
                                            correct = False
                                            game.turnsleft -= 1
                                if correct:
                                    game.turnsleft -= 1
                                    print()
                                    print("Congratulations! You got 5/5!")
                                    print("You picked up a USB drive!")
                                    print()
                                    location.takeitem(choice)

                                    game.inventory.append(game.get_item(choice))
                                    game.score += game.get_item(choice).target_points
                            else:
                                if turns == 0:
                                    print("You ran out of tries! try again.")
                                    game.turnsleft -= 1
                else:
                    print(f"\nYou picked up a {choice}!")
                    location.takeitem(choice)
                    print(game.get_item(choice).description)
                    game.inventory.append(game.get_item(choice))
                    game.score += game.get_item(choice).target_points

            else:
                print(f"\nYou picked up a {choice}!")
                location.takeitem(choice)
                print(game.get_item(choice).description)
                game.inventory.append(game.get_item(choice))
                game.score += game.get_item(choice).target_points

            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result
            game.turnsleft -= 1

        print("====================")
        if game.ongoing_sim[0]:
            if remtime.total_seconds() <= 0:
                game.ongoing_sim[0] = False
                print("Your time ran out!")
            else:
                mins, secs = divmod(int(remtime.total_seconds()), 60)
                print()
                print()
                print(f"Time left: {mins}mins, {secs}secs")
            if game.turnsleft <= 0 and game.score < 70:
                print("You ran out of turns! Game Over.")
                game.ongoing_sim[0] = False
            else:
                print(f"You have {game.turnsleft} turns left.")
                print()
            lastcommand = choice
