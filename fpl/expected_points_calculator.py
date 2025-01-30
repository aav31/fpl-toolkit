"""
This module defines the ExpectedPointsCalculator class, which is an abstract base class for calculating the expected points of a player in FPL.
The ExpectedPointsCalculator class includes an abstract method to get the expected points for a player in a specific gameweek.

Available functions:
- get_expected_points: Get the expected points for a player in a specific gameweek.
"""


from abc import ABC, abstractmethod
from fpl import Loader

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

    
class SimpleExpectedPointsCalculator(ExpectedPointsCalculator):
    """Simple expected points calculator.
    Major assumption is that the candidates you put in this list are nailed on to play 90.
    """
    fixture_difficulty_to_adj_map = {
        2: 1.5,
        3: 0.75,
        4: -0.75,
        5: -1.5
    }
    
    @staticmethod
    def get_expected_points(player_id: int, gameweek: int) -> float:
        basic_info = Loader.get_player_basic_info(player_id)
        chance_of_playing_next_round = basic_info["chance_of_playing_next_round"] / 100.0 if basic_info["chance_of_playing_next_round"] is not None else 1.0
        points_per_game = float(basic_info["points_per_game"])
        form = float(basic_info["form"])
        fixtures = Loader.get_player_future_info_for_gameweek(player_id, gameweek)
        expected_points = 0
        for fixture in fixtures:
            difficulty = fixture["difficulty"]
            difficulty_adj = SimpleExpectedPointsCalculator.fixture_difficulty_to_adj_map[difficulty]
            expected_points += (0.25 * form + 0.75 * points_per_game) + difficulty_adj
            
        return chance_of_playing_next_round * expected_points