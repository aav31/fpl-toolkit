from unittest import TestCase
from unittest.mock import patch
from fpl import SimpleExpectedPointsCalculator, Loader


class TestSimpleExpectedPointsCalculator(TestCase):
    """Unit tests for the SimpleExpectedPointsCalculator class"""

    def setUp(self):
        self.basic_info_player = {
            "points_per_game": 1,
            "form": 4,
        }

        team_2 = {
            "strength_overall_home": 1000,
            "strength_overall_away": 0,
        }

        self.mock_team_basic_info = {
            2: team_2,
        }

    @patch("fpl.Loader.get_team_basic_info")
    @patch("fpl.Loader.get_player_future_info_for_gameweek")
    @patch("fpl.Loader.get_player_basic_info")
    def test_get_expected_points(
        self,
        mock_get_player_basic_info,
        mock_get_player_future_info_for_gameweek,
        mock_get_team_basic_info,
    ):
        expected_points_easy_fixture = (
            SimpleExpectedPointsCalculator.alpha
            + SimpleExpectedPointsCalculator.beta_form * self.basic_info_player["form"]
            + SimpleExpectedPointsCalculator.beta_points_per_game
            * self.basic_info_player["points_per_game"]
        )
        expected_points_hard_fixture = (
            expected_points_easy_fixture
            + 1000 * SimpleExpectedPointsCalculator.beta_fixture_difficulty
        )
        test_cases = [
            {
                "name": "no_fixtures",
                "future_info": [],
                "expected_points": 0,
                "msg": "Should be zero since player has no future fixtures",
            },
            {
                "name": "easy_fixture",
                "future_info": [{"is_home": True, "team_h": 1, "team_a": 2}],
                "expected_points": expected_points_easy_fixture,
                "msg": "Should be above one as easy fixture",
            },
            {
                "name": "hard_fixture",
                "future_info": [{"is_home": False, "team_h": 2, "team_a": 1}],
                "expected_points": expected_points_hard_fixture,
                "msg": "Should be below one as hard fixture",
            },
            {
                "name": "two_fixtures",
                "future_info": [
                    {"is_home": True, "team_h": 1, "team_a": 2},
                    {"is_home": False, "team_h": 2, "team_a": 1},
                ],
                "expected_points": expected_points_easy_fixture
                + expected_points_hard_fixture,
                "msg": "Should account for both fixtures",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["name"]):
                mock_get_player_basic_info.return_value = self.basic_info_player
                mock_get_player_future_info_for_gameweek.return_value = test_case[
                    "future_info"
                ]
                mock_get_team_basic_info.side_effect = (
                    lambda i: self.mock_team_basic_info[i]
                )
                actual = SimpleExpectedPointsCalculator.get_expected_points(
                    player_id=1, gameweek=1
                )
                self.assertAlmostEqual(
                    actual, test_case["expected_points"], msg=test_case["msg"]
                )
