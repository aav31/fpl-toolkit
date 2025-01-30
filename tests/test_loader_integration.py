import unittest
from fpl import Loader, Team, Player
from unittest.mock import patch

class TestLoaderIntegration(unittest.TestCase):
    """Integration tests for the loader module.
    We want to make sure we get back what we expect from the FPL API.
    """
    def test_get_static_info(self):
        static_info = Loader.get_static_info()
        self.assertEqual(len(static_info["events"]), 38, "Should be 38 gameweeks")
        self.assertEqual(len(static_info["teams"]), 20)
        self.assertEqual(
            len(static_info["element_types"]),
            5,
            "Should be 5 different player types GKP, DEF, MID, FWD, MNG",
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
        self.assertEqual(man_city["strength"], 4)
        arsenal = Loader.get_team_basic_info(1)
        self.assertEqual(arsenal["short_name"], "ARS")

    @unittest.skip("TODO: Implement this test")
    def test_get_my_team_from_api(self):
        pass

    def test_get_my_team_from_local(self):
        my_team = Loader.get_my_team_from_local("./resources/my_team.json")
        self.assertEqual(len(my_team.gkps), 2)
        self.assertEqual(len(my_team.defs), 5)
        self.assertEqual(len(my_team.mids), 5)
        self.assertEqual(len(my_team.fwds), 3)

    def test_get_next_gameweek(self):
        self.assertEqual(
            Loader.get_next_gameweek("2024-08-16 17:00:00"), 1, "Before deadline"
        )
        self.assertEqual(
            Loader.get_next_gameweek("2024-08-16 21:00:00"), 2, "After deadline"
        )
    
    @unittest.skip("TODO: Implement this test")
    def test_get_my_historical_team_from_gameweek(self):
        pass
        
    def test_get_player_basic_info(self):
        player_basic_info = Loader.get_player_basic_info(182)
        self.assertEqual(player_basic_info["web_name"], "Palmer")
        self.assertEqual(player_basic_info["first_name"], "Cole")

    def test_get_player_detailed_info(self):
        player_detailed_info = Loader.get_player_detailed_info(182)
        self.assertIn("fixtures", player_detailed_info)
        self.assertIn("history", player_detailed_info)
        self.assertIn("history_past", player_detailed_info)
        
    @unittest.skip("TODO: Implement this test again")
    def test_get_player_historical_info_for_gameweek(self):
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
    
    @unittest.skip("TODO: Implement this test")
    def test_find_matching_players(self):
        pass