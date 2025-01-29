import unittest
from fpl import Team, Player


class TestTeam(unittest.TestCase):
    """Unit tests for the team module.
    """
    def setUp(self):
        # GKPs
        self.gkp_club_1 = Player.from_min_info(element=1, position=1, club=1, cost=40)
        self.gkp_club_2 = Player.from_min_info(element=2, position=1, club=2, cost=45)
        # DEFs
        self.def_club_1 = Player.from_min_info(element=3, position=2, club=1, cost=40)
        self.def_club_2 = Player.from_min_info(element=4, position=2, club=2, cost=45)
        self.def_club_3 = Player.from_min_info(element=5, position=2, club=3, cost=50)
        self.def_club_4 = Player.from_min_info(element=6, position=2, club=4, cost=55)
        self.def_club_5 = Player.from_min_info(element=7, position=2, club=5, cost=60)
        # MIDs
        self.mid_club_1 = Player.from_min_info(element=8, position=3, club=1, cost=45)
        self.mid_club_2 = Player.from_min_info(element=9, position=3, club=2, cost=50)
        self.mid_club_3 = Player.from_min_info(element=10, position=3, club=3, cost=60)
        self.mid_club_4 = Player.from_min_info(element=11, position=3, club=4, cost=70)
        self.mid_club_5 = Player.from_min_info(element=12, position=3, club=5, cost=80)
        # FWDs
        self.fwd_club_3 = Player.from_min_info(element=13, position=4, club=3, cost=60)
        self.fwd_club_4 = Player.from_min_info(element=14, position=4, club=4, cost=75)
        self.fwd_club_5 = Player.from_min_info(element=15, position=4, club=5, cost=80)
        self.fwd_club_1 = Player.from_min_info(element=16, position=4, club=1, cost=45)
        self.fwd_club_2 = Player.from_min_info(element=17, position=4, club=2, cost=55)
        
        self.team_1 = Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=0,
            free_transfers=1,
        )
        
        # has a different forward to team 1
        self.team_2 = Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_1]),
            money_in_bank=0,
            free_transfers=1,
        )
        
        # has one less free transfers than team 1
        self.team_3 = Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=0,
            free_transfers=0,
        )
        
        # has one less free transfers than team 1 but more money
        self.team_4 = Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=5,
            free_transfers=0,
        )
        
        # same as team 1 with players in different order
        self.team_5 = Team(
            gkps=frozenset([self.gkp_club_2, self.gkp_club_1]),
            defs=frozenset(
                [
                    self.def_club_5,
                    self.def_club_4,
                    self.def_club_3,
                    self.def_club_2,
                    self.def_club_1,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_5,
                    self.mid_club_4,
                    self.mid_club_3,
                    self.mid_club_2,
                    self.mid_club_1,
                ]
            ),
            fwds=frozenset([self.fwd_club_5, self.fwd_club_4, self.fwd_club_3]),
            money_in_bank=0,
            free_transfers=1,
        )
        
    def test_post_init(self):
        with self.assertRaises(TypeError, msg="Expected TypeError when money_in_bank is not an integer"):
            Team(money_in_bank="10", free_transfers=2, gkps=frozenset(), defs=frozenset(), mids=frozenset(), fwds=frozenset())
        
        with self.assertRaises(TypeError, msg="Expected TypeError gkps is a set not frozenset"):
            Team(money_in_bank=10, free_transfers=2, gkps=set(), defs=frozenset(), mids=frozenset(), fwds=frozenset())
            
        with self.assertRaises(TypeError, msg="Expected TypeError when element of gkps isn't a player"):
            Team(money_in_bank=10, free_transfers=2, gkps=frozenset(1), defs=frozenset(), mids=frozenset(), fwds=frozenset())
            
        # should not throw any errors in initialization, however the team is not feasible
        Team(money_in_bank=10, free_transfers=2, gkps=frozenset(), defs=frozenset(), mids=frozenset(), fwds=frozenset())

    def test_eq(self):
        self.assertNotEqual(self.team_1, self.team_2, "Have different teams")
        self.assertNotEqual(self.team_1, self.team_3, "Have different free transfers")
        self.assertEqual(self.team_1, self.team_5, "Have the same team")

    def test_lt(self):
        self.assertLess(
            self.team_3, self.team_1, "Team 1 has more free transfers than team 3 therefore better"
        )
        self.assertLess(self.team_1, self.team_4,"Even though team 4 has less free transfers it has more money in the bank so better")
    
    @unittest.skip("TODO: Implement this test")
    def test_str(self):
        pass

    def test_is_feasible(self):
        self.assertTrue(Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=0,
            free_transfers=-5,
        ).is_feasible, "Negative free transfers not a problem - is feasible")

        self.assertFalse(Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=-1,
            free_transfers=1,
        ).is_feasible, "Money in the bank is negative so is not feasible")

        self.assertFalse(Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [
                    self.mid_club_1,
                    self.mid_club_2,
                    self.mid_club_3,
                    self.mid_club_4,
                    self.mid_club_5,
                ]
            ),
            fwds=frozenset([self.fwd_club_1, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=1,
            free_transfers=1,
        ).is_feasible, "Too many of one club so is not feasible")

        self.assertFalse(Team(
            gkps=frozenset([self.gkp_club_1, self.gkp_club_2]),
            defs=frozenset(
                [
                    self.def_club_1,
                    self.def_club_2,
                    self.def_club_3,
                    self.def_club_4,
                    self.def_club_5,
                ]
            ),
            mids=frozenset(
                [self.mid_club_1, self.mid_club_2, self.mid_club_3, self.mid_club_4]
            ),
            fwds=frozenset([self.fwd_club_3, self.fwd_club_4, self.fwd_club_5]),
            money_in_bank=0,
            free_transfers=-5,
        ).is_feasible, "Not enough mids so not feasible")
    
    def test_transfer_player(self):
        # Substitute a goalkeeper that costs too much
        gkp_club_10 = Player.from_min_info(element=100, position=1, club=10, cost=50)
        new_team = self.team_1.transfer_player(self.gkp_club_1, gkp_club_10)
        self.assertEqual(new_team.money_in_bank, -10, "Money in bank should be -10 after transferring in an expensive goalkeeper")
        self.assertEqual(new_team.free_transfers, 0, "Free transfers should be 0 after one transfer")
        self.assertFalse(new_team.is_feasible, "Team should not be feasible with negative money in bank")
        self.assertTrue(gkp_club_10 in new_team.gkps, "New goalkeeper should be in the team")
        self.assertTrue(self.gkp_club_1 not in new_team.gkps, "Old goalkeeper should be out of the team")

        # Following the first substitution, substitute a forward which is cheap
        fwd_club_10 = Player.from_min_info(element=120, position=4, club=10, cost=50)
        new_new_team = new_team.transfer_player(self.fwd_club_5, fwd_club_10)
        self.assertEqual(new_new_team.money_in_bank, 20, "Money in bank should be 20 after transferring in a cheap forward")
        self.assertEqual(new_new_team.free_transfers, -1, "Free transfers should be -1 after two transfers")
        self.assertTrue(new_new_team.is_feasible, "Team should be feasible with positive money in bank")
        self.assertTrue(fwd_club_10 in new_new_team.fwds, "New forward should be in the team")
        self.assertTrue(self.fwd_club_5 not in new_new_team.fwds, "Old forward should be out of the team")
        self.assertNotEqual(new_team, self.team_1, "New team should not be equal to the original team after transfers")

        # Try to make another transfer into another club 1 player - should not be feasible as too many players
        another_mid_club_1 = Player.from_min_info(element=130, position=3, club=1, cost=50)
        team_too_many_from_one_club = self.team_1.transfer_player(self.mid_club_5, another_mid_club_1)
        self.assertEqual(team_too_many_from_one_club.money_in_bank, 30, "Money in bank should be 30 after transferring in another midfielder")
        self.assertEqual(team_too_many_from_one_club.free_transfers, 0, "Free transfers should be 0 after one transfer")
        self.assertFalse(team_too_many_from_one_club.is_feasible, "Team should not be feasible with too many players from one club")
        self.assertTrue(another_mid_club_1 in team_too_many_from_one_club.mids, "New midfielder should be in the team")
        self.assertTrue(self.mid_club_5 not in team_too_many_from_one_club.mids, "Old midfielder should be out of the team")
