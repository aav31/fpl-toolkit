import unittest
from fpl import Loader, Player
from unittest.mock import patch


class TestLoader(unittest.TestCase):
    """Unit tests for the loader module."""

    def setUp(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_static_info(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_fixtures(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_fixture_info(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_fixtures_for_gameweek(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_team_basic_info(self):
        pass

    def test_get_my_team(self):
        with self.assertRaises(
            ValueError, msg="The 'how' argument must be api or local."
        ):
            Loader.get_my_team(
                login="", password="", manager_id="", how="wrong_arg", filename=""
            )

        with self.assertRaises(
            ValueError, msg="When 'how' argument is local filename must be non-empty."
        ):
            Loader.get_my_team(
                login="", password="", manager_id="", how="local", filename=""
            )

        my_team = Loader.get_my_team(
            login="",
            password="",
            manager_id="",
            how="local",
            filename="./resources/my_team.json",
        )
        self.assertEqual(len(my_team.gkps), 2)
        self.assertEqual(len(my_team.defs), 5)
        self.assertEqual(len(my_team.mids), 5)
        self.assertEqual(len(my_team.fwds), 3)
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_next_gameweek(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_my_historical_team_from_gameweek(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_player_basic_info(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_player_detailed_info(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_player_historical_info_for_gameweek(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_player_future_info_for_gameweek(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_position_info(self):
        pass
