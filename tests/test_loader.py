import unittest
from fpl import Loader, Player
from unittest.mock import patch

class TestLoader(unittest.TestCase):
    """Unit tests for the loader module.
    """
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

    @unittest.skip("TODO: Implement this test")
    def test_get_my_team_from_api(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_get_my_team_from_local(self):
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