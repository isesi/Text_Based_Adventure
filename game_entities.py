"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Item:
    """An item in our text adventure game world.
    Instance Attributes:
        - name: Name of item
        - desciption: A small description of this item
        - start_position: The location id where this item originally is
        - target_position: The location this item should be depositied at
        - target_points: Points earned by depositing item at correct location
    Representation Invariants:
        - start_position != target_position
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.
    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.
@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - brief_description: brief description of this location
        - long_description: a longer description of the location
        - available_commands: a mapping of available commands at this location to
                                the location executing that command would lead to
        - items: items that can be found at this location
        - visited: whether or not this location has been visited

    Representation Invariants:
    """
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: dict[str, Item]
    visited: bool

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id: int, brief_description: str, long_description: str, other: list[Any]) -> None:
        # vars[1] = availablecoms, 2 = items, 3 = visited bool, so that pythonTA doesn't get mad
        """Initialize a new location.
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = other[0]
        self.items = other[1]
        self.visited = other[2]

    def takeitem(self, itemid: str) -> None:
        """Take an item out of this location by picking it up"""
        if itemid is None:
            print(self.items)
            self.items.popitem()
        else:
            del self.items[itemid]

    def additem(self, it: Item) -> None:
        """Add an item to this location."""
        self.items[it.name] = it


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
