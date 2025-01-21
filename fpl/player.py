from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    element: int  # this is the unique id of the player
    name: str
    position: int
    club: int
    cost: int

    def __eq__(self, other: "Player") -> bool:
        """We need this defined so we can sort players"""
        return self.element == other.element

    def __lt__(self, other: "Player") -> bool:
        """We need this defined so we can sort players"""
        return self.element < other.element

    @classmethod
    def from_min_info(
        cls, element: int, position: int, club: int, cost: int
    ) -> "Player":
        """Allows players to be constructed without needing to specify a name"""
        name = str(element)
        return cls(element, name, position, club, cost)
