from unittest import TestCase
from unittest.mock import patch
from fpl import SimpleExpectedPointsCalculator, Loader


class TestSimpleExpectedPointsCalculator(TestCase):
    """Unit tests for the SimpleExpectedPointsCalculator class"""

    def setUp(self):
        # a dictionary representing a player expecting to score one point
        self.basic_info_player_expected_one_point = {
            "chance_of_playing_next_round": 100,
            "points_per_game": 1,
            "form": 1,
        }

        self.future_info_easy_fixture = [{"difficulty": 2}]

    @patch("fpl.Loader.get_player_future_info_for_gameweek")
    @patch("fpl.Loader.get_player_basic_info")
    def test_get_expected_points_fixtures(
        self, mock_get_player_basic_info, mock_get_player_future_info_for_gameweek
    ):
        test_cases = [
            {
                "name": "no_fixtures",
                "future_info": [],
                "expected_points": 0,
                "msg": "Should be zero since player has no future fixtures",
            },
            {
                "name": "easy_fixture",
                "future_info": [{"difficulty": 3}],
                "expected_points": 1 + 0.75,
                "msg": "Should be above one as easy fixture",
            },
            {
                "name": "hard_fixture",
                "future_info": [{"difficulty": 4}],
                "expected_points": 1 - 0.75,
                "msg": "Should be below one as hard fixture",
            },
            {
                "name": "two_fixtures",
                "future_info": [{"difficulty": 4}, {"difficulty": 4}],
                "expected_points": 2 - 1.5,
                "msg": "Should account for both fixtures",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["name"]):
                mock_get_player_basic_info.return_value = (
                    self.basic_info_player_expected_one_point
                )
                mock_get_player_future_info_for_gameweek.return_value = test_case[
                    "future_info"
                ]
                actual = SimpleExpectedPointsCalculator.get_expected_points(
                    player_id=1, gameweek=1
                )
                self.assertAlmostEqual(
                    actual, test_case["expected_points"], msg=test_case["msg"]
                )

    @patch("fpl.Loader.get_player_future_info_for_gameweek")
    @patch("fpl.Loader.get_player_basic_info")
    def test_get_expected_points_chance_of_playing_next_round(
        self, mock_get_player_basic_info, mock_get_player_future_info_for_gameweek
    ):
        chance_of_playing_dict_0 = {
            "chance_of_playing_next_round": 0,
            "points_per_game": 1,
            "form": 1,
        }

        chance_of_playing_dict_50 = {
            "chance_of_playing_next_round": 50,
            "points_per_game": 1,
            "form": 1,
        }

        test_cases = [
            {
                "name": "0_pct_chance_of_playing",
                "basic_info": chance_of_playing_dict_0,
                "expected_points": 0,
                "msg": "Should be zero since player has no chance of playing",
            },
            {
                "name": "50_pct_chance_of_playing",
                "basic_info": chance_of_playing_dict_50,
                "expected_points": 0.5 * (1 + 1.5),
                "msg": "Should be fifty percent times what you expect",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["name"]):
                mock_get_player_basic_info.return_value = test_case["basic_info"]
                mock_get_player_future_info_for_gameweek.return_value = (
                    self.future_info_easy_fixture
                )
                actual = SimpleExpectedPointsCalculator.get_expected_points(
                    player_id=1, gameweek=1
                )
                self.assertAlmostEqual(
                    actual, test_case["expected_points"], msg=test_case["msg"]
                )

    @patch("fpl.Loader.get_player_future_info_for_gameweek")
    @patch("fpl.Loader.get_player_basic_info")
    def test_get_expected_points_points_per_game_form(
        self, mock_get_player_basic_info, mock_get_player_future_info_for_gameweek
    ):
        points_per_game_1_form_1 = self.basic_info_player_expected_one_point

        points_per_game_2_form_4 = {
            "chance_of_playing_next_round": 100,
            "points_per_game": 2,
            "form": 4,
        }

        test_cases = [
            {
                "name": "points_per_game_1_form_1",
                "basic_info": points_per_game_1_form_1,
                "expected_points": 1 + 1.5,
                "msg": "Should score one point not accounting for fixture difficulty",
            },
            {
                "name": "points_per_game_2_form_4",
                "basic_info": points_per_game_2_form_4,
                "expected_points": (2 * 0.75) + (4 * 0.25) + 1.5,
                "msg": "Points per game weighted more than form",
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case["name"]):
                mock_get_player_basic_info.return_value = test_case["basic_info"]
                mock_get_player_future_info_for_gameweek.return_value = (
                    self.future_info_easy_fixture
                )
                actual = SimpleExpectedPointsCalculator.get_expected_points(
                    player_id=1, gameweek=1
                )
                self.assertAlmostEqual(
                    actual, test_case["expected_points"], msg=test_case["msg"]
                )
