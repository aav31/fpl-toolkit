import unittest
from fpl import Loader, Player
from unittest.mock import patch

class TestLoader(unittest.TestCase):
    def test_get_static_info(self):
        static_info = Loader.get_static_info()
        self.assertEqual(len(static_info["events"]), 38, "Should be 38 gameweeks")
        self.assertEqual(len(static_info["teams"]), 20)
        self.assertEqual(
            len(static_info["element_types"]),
            4,
            "Should be 4 different player types GKP, DEF, MID, FWD",
        )
        self.assertIn("web_name", static_info["elements"][0])
        self.assertIn("total_points", static_info["elements"][0])
        for p in static_info["elements"]:
            if p["web_name"] == "Palmer":
                self.assertEqual(
                    182, p["id"], "Player unique identifier should not change"
                )

    def test_get_fixtures(self):
        fixtures = Loader.get_fixtures()
        self.assertEqual(len(fixtures), 380)
        for fixture in fixtures:
            if (fixture["event"] == 4) and (fixture["team_h"] == 18):
                self.assertEqual(
                    fixture["team_a"], 1, "Spurs play Arsenal in gameweek 4"
                )
                self.assertEqual(
                    fixture["kickoff_time"],
                    "2024-09-15T13:00:00Z",
                    "The game occurs at 13:00 UTC",
                )

    def test_get_fixture_info(self):
        fixture_info = Loader.get_fixture_info(39)
        self.assertEqual(fixture_info["event"], 4, "Spurs play Arsenal in gameweek 4")
        self.assertEqual(fixture_info["team_h"], 18, "Spurs play Arsenal in gameweek 4")
        self.assertEqual(fixture_info["team_a"], 1, "Spurs play Arsenal in gameweek 4")
        self.assertEqual(
            fixture_info["kickoff_time"],
            "2024-09-15T13:00:00Z",
            "The game occurs at 13:00 UTC",
        )

    def test_get_fixtures_for_gameweek(self):
        fixtures = Loader.get_fixtures_for_gameweek(1)
        self.assertEqual(len(fixtures), 10, "No blanks")

        def is_chelsea_man_city(x):
            return (x["team_h"] == 6) and (x["team_a"] == 13)

        def is_man_utd_fulham(x):
            return (x["team_h"] == 14) and (x["team_a"] == 9)

        self.assertTrue(any(is_chelsea_man_city(fixture) for fixture in fixtures))
        self.assertTrue(any(is_man_utd_fulham(fixture) for fixture in fixtures))

    def test_get_team_basic_info(self):
        man_city = Loader.get_team_basic_info(13)
        self.assertEqual(man_city["short_name"], "MCI")
        self.assertEqual(man_city["strength"], 5)
        arsenal = Loader.get_team_basic_info(1)
        self.assertEqual(arsenal["short_name"], "ARS")

    def test_get_my_team_from_api(self):
        result = Loader.get_my_team_from_api(
            "aledvaghela@gmail.com", "NCP@jxy7pau-bvm3cuf", 3247546
        )
        self.assertIn("transfers", result)
        self.assertIn("chips", result)
        self.assertEqual(len(result["picks"]), 15)

    def test_get_my_team_from_local(self):
        my_team = Loader.get_my_team_from_local("./tests/my_team.json")
        self.assertEqual(len(my_team["picks"]), 15)
        self.assertEqual(my_team["transfers"]["limit"], 1)

    def test_get_next_gameweek(self):
        self.assertEqual(
            Loader.get_next_gameweek("2024-08-16 17:00:00"), 1, "Before deadline"
        )
        self.assertEqual(
            Loader.get_next_gameweek("2024-08-16 21:00:00"), 2, "After deadline"
        )

    def test_get_my_historical_team_from_gameweek(self):
        print(
            "Warning: test_get_my_historical_team_for_gameweek needs to be implemented"
        )
        return
        my_historical_team = FplLoader.get_my_historical_team_from_gameweek(1, 3247546)
        self.assertEqual(
            my_historical_team["entry_history"]["points"],
            32,
            "Very poor week, only scored 32 points!",
        )
        self.assertEqual(len(my_historical_team["picks"]), 15)

    def test_get_player_basic_info(self):
        # TODO: should probs add more stuff here
        player_basic_info = Loader.get_player_basic_info(182)
        self.assertEqual(player_basic_info["web_name"], "Palmer")
        self.assertEqual(player_basic_info["first_name"], "Cole")

    def test_get_player_detailed_info(self):
        player_detailed_info = Loader.get_player_detailed_info(182)
        self.assertIn("fixtures", player_detailed_info)
        self.assertIn("history", player_detailed_info)
        self.assertIn("history_past", player_detailed_info)

    def test_get_player_historical_info_for_gameweek(self):
        print(
            "Warning: test_get_player_historical_info_for_gameweek needs to be implemented"
        )
        return
        palmer = Loader.get_player_historical_info_for_gameweek(182, 1)
        self.assertEqual(palmer[0]["total_points"], 12, "Cole Palmer got 12 points")
        self.assertEqual(palmer[0]["expected_goals"], "0.83", "0.83 xG")
        burnley_player = FplLoader.get_player_historical_info_for_gameweek(178, 2)
        self.assertEqual(len(burnley_player), 0, "Burnley blanked this gameweek")
        burnley_player = FplLoader.get_player_historical_info_for_gameweek(178, 3)
        self.assertEqual(len(burnley_player), 1, "Burnley did not blank this gameweek")

    def test_get_player_future_info_for_gameweek(self):
        player_future_info = Loader.get_player_future_info_for_gameweek(182, 38)
        self.assertEqual(
            len(player_future_info), 1, "Chelsea have one game in the final gameweek"
        )
        self.assertEqual(
            player_future_info[0]["team_a"],
            6,
            "Chelsea (away) play Nottingham Forest (home) on the final day",
        )

    def test_get_position_info(self):
        self.assertEqual(Loader.get_position_info(1)["singular_name_short"], "GKP")
        self.assertEqual(Loader.get_position_info(2)["singular_name_short"], "DEF")
        self.assertEqual(Loader.get_position_info(3)["singular_name_short"], "MID")
        self.assertEqual(Loader.get_position_info(4)["singular_name_short"], "FWD")
        
    def setUp(self):
        self.mock_elements = [
            {"id": 1, "web_name": "John Doe"},
            {"id": 2, "web_name": "Jane Smith"},
            {"id": 3, "web_name": "Johnny Appleseed"}
        ]
        self.mock_player_info = {
            1: {
                "web_name": "John Doe",
                "element_type": "Midfielder",
                "team": "Team A",
                "now_cost": 100,
                "first_name": "John",
                "second_name": "Doe"
            },
            2: {
                "web_name": "Jane Smith",
                "element_type": "Defender",
                "team": "Team B",
                "now_cost": 90,
                "first_name": "Jane",
                "second_name": "Smith"
            },
            3: {
                "web_name": "Johnny Appleseed",
                "element_type": "Forward",
                "team": "Team C",
                "now_cost": 110,
                "first_name": "Johnny",
                "second_name": "Appleseed"
            }
        }

    @patch('fpl.loader.Loader.get_static_info')
    @patch('fpl.loader.Loader.get_player_basic_info')
    def test_find_matching_players(self, mock_get_player_basic_info, mock_get_static_info):
        # Set up mock return values
        mock_get_static_info.return_value = {"elements": self.mock_elements}
        mock_get_player_basic_info.side_effect = lambda i: self.mock_player_info[i]

        # Test case
        search_name = "John"
        threshold = 80
        result = Loader.find_matching_players(search_name, threshold)

        # Expected result
        expected_players = [
            Player(
                element=1,
                name="John Doe",
                position="Midfielder",
                club="Team A",
                cost=100
            ),
            Player(
                element=3,
                name="Johnny Appleseed",
                position="Forward",
                club="Team C",
                cost=110
            )
        ]
        expected_full_names = ["John Doe", "Johnny Appleseed"]
        expected_result = list(zip(expected_players, expected_full_names))

        self.assertEqual(result, expected_result)

    @patch('fpl.loader.Loader.get_static_info')
    def test_find_matching_players_no_match(self, mock_get_static_info):
        # Set up mock return values
        mock_get_static_info.return_value = {"elements": self.mock_elements}

        # Test case
        search_name = "Alice"
        threshold = 80

        with self.assertRaises(ValueError):
            Loader.find_matching_players(search_name, threshold)