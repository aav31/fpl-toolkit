"""
This module defines the ExpectedPointsCalculator class, which is an abstract base class for calculating the expected points of a player in FPL. It also defines the SimpleExpectedPointsCalculator class, which is a concrete implementation of the ExpectedPointsCalculator.

Available classes:
- ExpectedPointsCalculator: Abstract base class for calculating the expected points of a player in FPL.
- SimpleExpectedPointsCalculator: A simple implementation of the ExpectedPointsCalculator.

Available functions:
- get_expected_points: Get the expected points for a player in a specific gameweek.
"""

from abc import ABC, abstractmethod
from fpl import Loader


class ExpectedPointsCalculator(ABC):
    """Class to calculate the points that a particular player will get."""

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
    """A concrete implementation of an ExpectedPointsCalculator using a linear regression model.
    For more information: https://github.com/aav31/fpl-toolkit/blob/main/regression.ipynb

    Major assumption is that the candidates here will play at least 0 minutes.

    This implementation calculates expected points by considering the player's form,
    points per game, and fixture difficulty.
    """

    alpha = 5.9697
    beta_form = 0.1202
    beta_points_per_game = 0.4604
    beta_fixture_difficulty = -0.0041

    @staticmethod
    def get_expected_points(player_id: int, gameweek: int) -> float:
        """Get the expected points for a player in a specific gameweek.

        :param player_id: The unique ID of the player.
        :param gameweek: The gameweek for which to calculate the expected points.

        :return: The expected points for the player in the specified gameweek.
        """
        basic_info = Loader.get_player_basic_info(player_id)
        points_per_game = float(basic_info["points_per_game"])
        form = float(basic_info["form"])
        gameweek_info = Loader.get_player_future_info_for_gameweek(player_id, gameweek)

        expected_points = 0
        # A player can play multiple fixtures in a single gameweek i.e. a "double" gameweek
        for fixture_info in gameweek_info:
            is_home = fixture_info["is_home"]
            opponent_team_id = (
                fixture_info["team_a"] if is_home else fixture_info["team_h"]
            )
            opponent_team_info = Loader.get_team_basic_info(opponent_team_id)
            fixture_difficulty = (
                opponent_team_info["strength_overall_away"]
                if is_home
                else opponent_team_info["strength_overall_home"]
            )
            expected_points += (
                SimpleExpectedPointsCalculator.alpha
                + SimpleExpectedPointsCalculator.beta_form * form
                + SimpleExpectedPointsCalculator.beta_points_per_game * points_per_game
                + SimpleExpectedPointsCalculator.beta_fixture_difficulty
                * fixture_difficulty
            )

        return expected_points
