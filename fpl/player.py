"""
This module defines the Player class, which represents a player in the Fantasy Premier League (FPL).
The Player class includes attributes such as the player's unique ID, name, position, club, and cost.
It also provides methods for comparing players and creating player instances with minimal information.

Available functions:
- __eq__: Checks if two players are equal based on their unique ID.
- __lt__: Compares two players based on their unique ID.
- from_min_info: Creates a Player instance with minimal information, using the player's unique ID as the name.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    element: int # this is the unique id of the player
    name: str
    position: int # 1 = GKP, 2 = DEF, 3 = MID, 4 = FWD
    club: int
    cost: int

    def __eq__(self, other: "Player") -> bool:
        """Check if two players are equal based on their unique ID.
        We need this defined so we can sort players.
        
        :param other: Another Player instance to compare with.

        :return: True if the players have the same unique ID, False otherwise.
        """
        return self.element == other.element

    def __lt__(self, other: "Player") -> bool:
        """Compare two players based on their unique ID.
        We need this defined so we can sort players.
        
        :param other: Another Player instance to compare with.

        :return: True if this player's unique ID is less than the other player's unique ID, False otherwise.
        """
        return self.element < other.element

    @classmethod
    def from_min_info(
        cls, element: int, position: int, club: int, cost: int
    ) -> "Player":
        """Create a Player instance with minimal information, using the player's unique ID as the name.
        Allows players to be constructed without needing to specify a name
        
        :param element: The unique ID of the player.
        :param position: The position of the player.
        :param club: The club ID of the player.
        :param cost: The cost of the player.

        :return: A Player instance with the specified attributes.
        """
        name = str(element)
        return cls(element, name, position, club, cost)
