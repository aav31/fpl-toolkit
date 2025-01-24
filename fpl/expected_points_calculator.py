"""
This module defines the ExpectedPointsCalculator class, which is an abstract base class for calculating the expected points of a player in FPL.
The ExpectedPointsCalculator class includes an abstract method to get the expected points for a player in a specific gameweek.

Available functions:
- get_expected_points: Get the expected points for a player in a specific gameweek.
"""


from abc import ABC, abstractmethod


class ExpectedPointsCalculator(ABC):
    """Class to calculate the points that a particular player will get.
    """

    @staticmethod
    @abstractmethod
    def get_expected_points(player_id: int, gameweek: int) -> float:
        """Get the expected points for a player in a specific gameweek.

        :param player_id: The unique ID of the player.
        :param gameweek: The gameweek for which to calculate the expected points.

        :return: The expected points for the player in the specified gameweek.
        """
        pass
