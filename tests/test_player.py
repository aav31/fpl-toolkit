import unittest
from fpl import Player
        
        
class TestPlayer(unittest.TestCase):
    def test_eq(self):
        player1 = Player(element=1, name="Player1", position=3, club=1, cost=50)
        player2 = Player(element=1, name="Player1", position=3, club=1, cost=40)
        player3 = Player(element=2, name="Player1", position=3, club=1, cost=50)
        self.assertEqual(player1, player2)
        self.assertNotEqual(player1, player3)

    def test_lt(self):
        player1 = Player(element=1, name="Player1", position=3, club=1, cost=1000)
        player2 = Player(element=2, name="Player2", position=3, club=1, cost=90)
        self.assertLess(player1, player2) # less than in this case means in terms of id
        self.assertGreater(player2, player1)

    def test_from_min_info(self):
        player = Player.from_min_info(element=1, position=3, club=10, cost=100)
        self.assertEqual(player.element, 1)
        self.assertEqual(player.name, "1")
        self.assertEqual(player.position, 3)
        self.assertEqual(player.club, 10)
        self.assertEqual(player.cost, 100)
