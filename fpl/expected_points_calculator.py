from abc import ABC, abstractmethod

class ExpectedPointsCalculator(ABC):
    """
    Class to calculate the points that a particular player will get
    """
    @staticmethod
    @abstractmethod
    def get_expected_points(player_id: int, gameweek: int) -> float:
        """
        Get expected points
        """
        pass