import unittest
from fpl import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.p1 = Player.from_min_info(
            **{"element": 1, "position": 1, "cost": 50, "club": 1}
        )
        self.p2 = Player.from_min_info(
            **{"element": 1, "position": 1, "cost": 40, "club": 1}
        )
        self.p3 = Player.from_min_info(
            **{"element": 2, "position": 1, "cost": 50, "club": 1}
        )

    def test_lt_eq(self):
        self.assertEqual(self.p1, self.p2)
        self.assertNotEqual(self.p1, self.p3)
