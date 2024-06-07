from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
    element: int  # this is the unique id of the player
    name: str
    position: int
    club: int
    cost: int
        
    def __eq__(self, other: 'Player') -> bool:
        return self.element == other.element
    
    def __lt__(self, other: 'Player') -> bool:
        return self.element < other.element
