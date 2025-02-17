import pandas as pd
from unittest import TestCase
from unittest.mock import patch
from fpl import find_matching_players, compute_points_per_game, compute_form, Player


class TestUtils(TestCase):
    """Unit tests for the utils module."""

    def setUp(self):
        self.mock_elements = [
            {"id": 1, "web_name": "John"},
            {"id": 2, "web_name": "Jane"},
            {"id": 3, "web_name": "Johnny"},
        ]
        # in the static info these are all the rounds - i.e. length 38
        self.mock_events = [
            {"id": 1, "deadline_time": "2024-08-01T17:30:00Z"},
            {"id": 2, "deadline_time": "2024-08-08T17:30:00Z"},
            {"id": 3, "deadline_time": "2024-09-05T17:30:00Z"},
            {"id": 4, "deadline_time": "2024-12-05T17:30:00Z"},
        ]
        self.mock_static_info = {
            "elements": self.mock_elements,
            "events": self.mock_events,
        }

        self.mock_player_basic_info = {
            1: {
                "web_name": "John",
                "element_type": 3,
                "team": "Team A",
                "now_cost": 100,
                "first_name": "John",
                "second_name": "Doe",
            },
            2: {
                "web_name": "Jane",
                "element_type": 3,
                "team": "Team B",
                "now_cost": 90,
                "first_name": "Jane",
                "second_name": "Smith",
            },
            3: {
                "web_name": "Johnny",
                "element_type": 3,
                "team": "Team C",
                "now_cost": 110,
                "first_name": "Johnny",
                "second_name": "Doesmith",
            },
        }

        # mapping of gameweek to historical info
        self.fixtures_gameweek_1 = [
            {
                "total_points": 1,
                "minutes": 90,
                "kickoff_time": "2024-08-01T17:30:00Z",
            },
        ]

        self.fixtures_gameweek_2 = [
            {
                "total_points": 4,
                "minutes": 90,
                "kickoff_time": "2024-08-08T17:30:00Z",
            },
            {
                "total_points": 0,
                "minutes": 0,
                "kickoff_time": "2024-08-13T17:30:00Z",
            },
        ]

        self.mock_player_historical_info_for_gameweek = {
            1: self.fixtures_gameweek_1,
            2: self.fixtures_gameweek_2,
            3: {},
        }

    @patch("fpl.loader.Loader.get_static_info")
    @patch("fpl.loader.Loader.get_player_basic_info")
    def test_find_matching_players(
        self, mock_get_player_basic_info, mock_get_static_info
    ):
        mock_get_static_info.return_value = self.mock_static_info
        mock_get_player_basic_info.side_effect = lambda i: self.mock_player_basic_info[
            i
        ]
        result = find_matching_players(search_name="John", threshold=80)
        expected_players = [
            Player(
                element=1,
                name=self.mock_player_basic_info[1]["web_name"],
                position=self.mock_player_basic_info[1]["element_type"],
                club=self.mock_player_basic_info[1]["team"],
                cost=self.mock_player_basic_info[1]["now_cost"],
            ),
            Player(
                element=3,
                name=self.mock_player_basic_info[3]["web_name"],
                position=self.mock_player_basic_info[3]["element_type"],
                club=self.mock_player_basic_info[3]["team"],
                cost=self.mock_player_basic_info[3]["now_cost"],
            ),
        ]
        expected_full_names = ["John Doe", "Johnny Doesmith"]
        expected_result = list(zip(expected_players, expected_full_names))

        self.assertEqual(result, expected_result)

    @patch("fpl.loader.Loader.get_static_info")
    def test_find_matching_players_no_match(self, mock_get_static_info):
        mock_get_static_info.return_value = self.mock_static_info
        with self.assertRaises(ValueError):
            find_matching_players(search_name="Alice", threshold=80)

    @patch("fpl.loader.Loader.get_player_historical_info_for_gameweek")
    def test_compute_points_per_game(
        self, mock_get_player_historical_info_for_gameweek
    ):
        # first argument unused
        mock_get_player_historical_info_for_gameweek.side_effect = (
            lambda x, y: self.mock_player_historical_info_for_gameweek[y]
        )
        scenarios = [
            {
                "name": "as_of_gameweek 1",
                "input": 1,
                "expected": 0.0,
                "msg": "No gameweeks to compute an average over therefore returns zero",
            },
            {
                "name": "as_of_gameweek 2",
                "input": 2,
                "expected": 1.0,
                "msg": "Compute an average only over the first gameweek",
            },
            {
                "name": "as_of_gameweek 3",
                "input": 3,
                "expected": 2.5,
                "msg": "Compute an average over 2 gameweeks but exclude games with 0 minutes",
            },
        ]

        for scenario in scenarios:
            with self.subTest(name=scenario["name"], msg=scenario["msg"]):
                actual = compute_points_per_game(
                    player_id=1, as_of_gameweek=scenario["input"]
                )
                self.assertAlmostEqual(
                    actual, scenario["expected"], msg=scenario["msg"]
                )

    @patch("pandas.Timestamp.now")
    @patch("fpl.loader.Loader.get_next_gameweek")
    @patch("fpl.loader.Loader.get_static_info")
    @patch("fpl.loader.Loader.get_player_historical_info_for_gameweek")
    def test_compute_form(
        self,
        mock_get_player_historical_info_for_gameweek,
        mock_get_static_info,
        mock_get_next_gameweek,
        mock_now,
    ):
        # first argument unused
        mock_get_player_historical_info_for_gameweek.side_effect = (
            lambda x, y: self.mock_player_historical_info_for_gameweek[y]
        )
        mock_get_static_info.return_value = self.mock_static_info
        mock_get_next_gameweek.return_value = 4
        mock_now.return_value = pd.Timestamp("2024-09-05T17:30:00Z", tz="UTC")
        scenarios = [
            {
                "name": "as_of_gameweek 1",
                "input": 1,
                "expected": 0.0,
                "msg": "No gameweeks to compute an average over therefore returns zero",
            },
            {
                "name": "as_of_gameweek 2",
                "input": 2,
                "expected": 1.0,
                "msg": "Compute an average only over the first gameweek",
            },
            {
                "name": "as_of_gameweek 3",
                "input": 3,
                "expected": 2.0,
                "msg": "Compute an average only over gameweek 2 because first gameweek is more than 30 days ago",
            },
            {
                "name": "as_of_gameweek 4",
                "input": 4,
                "expected": 2.0,
                "msg": "Even though deadline way in the future, computation as of now contains a single game played in gameweek 2",
            },
        ]

        for scenario in scenarios:
            with self.subTest(name=scenario["name"], msg=scenario["msg"]):
                actual = compute_form(player_id=1, as_of_gameweek=scenario["input"])
                self.assertAlmostEqual(
                    actual, scenario["expected"], msg=scenario["msg"]
                )
