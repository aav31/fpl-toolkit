import unittest
from fpl import Team, Player


class TestTeam(unittest.TestCase):
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

    def test_eq(self):
        team_1 = Team(
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

        team_2 = Team(
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
        self.assertNotEqual(team_1, team_2, "Have different teams")

        team_3 = Team(
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
        self.assertNotEqual(team_1, team_3, "Have different free transfers")

        team_4 = Team(
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
        self.assertEqual(team_1, team_4)

    def test_lt(self):
        team_1 = Team(
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

        team_2 = Team(
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
            free_transfers=2,
        )

        self.assertLess(
            team_1, team_2, "Team 2 has more free transfers therefore better"
        )

        team_3 = Team(
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
            money_in_bank=1,
            free_transfers=1,
        )

        self.assertLess(
            team_2,
            team_3,
            "Even though team 3 has less free transfers it has more money in the bank so better",
        )

    def test_is_feasible(self):
        team_1 = Team(
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
        )
        self.assertTrue(team_1.is_feasible)

        team_2 = Team(
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
        )
        self.assertFalse(team_2.is_feasible, "Money in the bank is negative")

        team_3 = Team(
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
        )
        self.assertFalse(team_3.is_feasible, "Too many of one club")

        team_4 = Team(
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
        )
        self.assertFalse(team_4.is_feasible, "Not enough mids")

    def test_transfer_player(self):
        old_team = Team(
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

        # substitute a goalkeeper that costs too much
        gkp_club_10 = Player.from_min_info(element=100, position=1, club=10, cost=50)
        new_team = old_team.transfer_player(self.gkp_club_1, gkp_club_10)
        self.assertEqual(new_team.money_in_bank, -10)
        self.assertEqual(new_team.free_transfers, -1)
        self.assertFalse(new_team.is_feasible)
        self.assertTrue(gkp_club_10 in new_team.gkps)
        self.assertTrue(self.gkp_club_1 not in new_team.gkps)

        # following the first substitution substitute a fwd which is cheap
        fwd_club_10 = Player.from_min_info(element=120, position=4, club=10, cost=50)
        new_new_team = new_team.transfer_player(self.fwd_club_5, fwd_club_10)
        self.assertEqual(new_new_team.money_in_bank, 20)
        self.assertEqual(new_new_team.free_transfers, -2)
        self.assertTrue(new_new_team.is_feasible)
        self.assertTrue(fwd_club_10 in new_new_team.fwds)
        self.assertTrue(self.fwd_club_5 not in new_new_team.fwds)
        self.assertNotEqual(new_team, old_team)

        # try instead to make another transfer into another club 1 player - should not be feasible as too many players
        another_mid_club_1 = Player.from_min_info(
            element=130, position=3, club=1, cost=50
        )
        team_too_many_from_one_club = old_team.transfer_player(
            self.mid_club_5, another_mid_club_1
        )
        self.assertEqual(team_too_many_from_one_club.money_in_bank, 30)
        self.assertEqual(team_too_many_from_one_club.free_transfers, -1)
        self.assertFalse(team_too_many_from_one_club.is_feasible)
        self.assertTrue(another_mid_club_1 in team_too_many_from_one_club.mids)
        self.assertTrue(self.mid_club_5 not in team_too_many_from_one_club.mids)
