import unittest
from fpl import ExpectedPointsCalculator, Team, Player, Optimizer
import heapq

# TODO: add tests for discounted reward for discounting
# TODO: add tests to optimize team for discounting


class TestOptimizer(unittest.TestCase):
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

        self.team = Team(
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

        # player map
        self.pm = {
            1: self.gkp_club_1,
            2: self.gkp_club_2,
            3: self.def_club_1,
            4: self.def_club_2,
            5: self.def_club_3,
            6: self.def_club_4,
            7: self.def_club_5,
            8: self.mid_club_1,
            9: self.mid_club_2,
            10: self.mid_club_3,
            11: self.mid_club_4,
            12: self.mid_club_5,
            13: self.fwd_club_3,
            14: self.fwd_club_4,
            15: self.fwd_club_5,
        }

        # expected points map
        self.epm_A = {
            1: 5.0,
            2: 1.0,
            3: 5.0,
            4: 5.0,
            5: 5.0,
            6: 5.0,
            7: 1.0,
            8: 5.0,
            9: 5.0,
            10: 5.0,
            11: 5.0,
            12: 1.0,
            13: 5.0,
            14: 5.0,
            15: 1.0,
        }

        self.epm_B = {
            1: 1.0,
            2: 2.0,
            3: 3.0,
            4: 4.0,
            5: 5.0,
            6: 6.0,
            7: 7.0,
            8: 8.0,
            9: 9.0,
            10: 10.0,
            11: 11.0,
            12: 12.0,
            13: 13.0,
            14: 14.0,
            15: 15.0,
        }

        self.epm_C = {
            1: 15.0,
            2: 14.0,
            3: 13.0,
            4: 12.0,
            5: 11.0,
            6: 10.0,
            7: 9.0,
            8: 8.0,
            9: 7.0,
            10: 6.0,
            11: 5.0,
            12: 4.0,
            13: 3.0,
            14: 2.0,
            15: 1.0,
        }

        self.epm_D = {
            1: 0.0,
            2: 1.0,
            3: 2.0,
            4: 2.0,
            5: 2.0,
            6: 2.0,
            7: 2.0,
            8: 0.0,
            9: 0.0,
            10: 0.0,
            11: 1.0,
            12: 1.0,
            13: 2.0,
            14: 2.0,
            15: 2.0,
        }

        class MockCalculatorZero(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return 0

        self.epcZero = MockCalculatorZero

    def test_optimal_formation(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.epm_A[player_id]

        result = Optimizer.optimal_formation(self.team, MockCalculator, 0)
        self.assertEqual(result["gkps"], set([self.pm[1]]))
        self.assertEqual(
            result["defs"], set([self.pm[3], self.pm[4], self.pm[5], self.pm[6]])
        )
        self.assertEqual(
            result["mids"], set([self.pm[8], self.pm[9], self.pm[10], self.pm[11]])
        )
        self.assertEqual(result["fwds"], set([self.pm[13], self.pm[14]]))
        self.assertAlmostEqual(result["total_exp_points"], 60)

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.epm_B[player_id]

        result = Optimizer.optimal_formation(self.team, MockCalculator, 0)
        self.assertEqual(result["gkps"], set([self.pm[2]]))
        self.assertEqual(result["defs"], set([self.pm[5], self.pm[6], self.pm[7]]))
        self.assertEqual(
            result["mids"], set([self.pm[9], self.pm[10], self.pm[11], self.pm[12]])
        )
        self.assertEqual(result["fwds"], set([self.pm[13], self.pm[14], self.pm[15]]))
        self.assertAlmostEqual(result["total_exp_points"], 119)

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.epm_C[player_id]

        result = Optimizer.optimal_formation(self.team, MockCalculator, 0)
        self.assertEqual(result["gkps"], set([self.pm[1]]))
        self.assertEqual(
            result["defs"],
            set([self.pm[3], self.pm[4], self.pm[5], self.pm[6], self.pm[7]]),
        )
        self.assertEqual(
            result["mids"], set([self.pm[8], self.pm[9], self.pm[10], self.pm[11]])
        )
        self.assertEqual(result["fwds"], set([self.pm[13]]))
        self.assertAlmostEqual(result["total_exp_points"], 114)

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.epm_D[player_id]

        result = Optimizer.optimal_formation(self.team, MockCalculator, 0)
        self.assertEqual(result["gkps"], set([self.pm[2]]))
        self.assertEqual(
            result["defs"],
            set([self.pm[3], self.pm[4], self.pm[5], self.pm[6], self.pm[7]]),
        )
        self.assertEqual(result["mids"], set([self.pm[11], self.pm[12]]))
        self.assertEqual(result["fwds"], set([self.pm[13], self.pm[14], self.pm[15]]))
        self.assertAlmostEqual(result["total_exp_points"], 21)

    def test_discounted_reward_simple(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if gameweek == 1:
                    return 10
                if gameweek == 2:
                    return 20
                if gameweek == 3:
                    return 30

        team = Team(
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
            free_transfers=5,
        )
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=3
        )
        expected = 12 * (10 + 20 + 30)
        self.assertAlmostEqual(
            actual, expected, msg="No transfer adjustment should be applied"
        )

        team = Team(
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
            free_transfers=4,
        )
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=3
        )
        expected = 12 * (10 + 20 + 30)
        self.assertAlmostEqual(
            actual, expected, msg="No transfer adjustment should be applied"
        )

        team = Team(
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
            free_transfers=3,
        )
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=3
        )
        expected = 12 * (10 + 20 + 30) - 0.8
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

        team = Team(
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
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=3
        )
        expected = 12 * (10 + 20 + 30) - 3.2
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

        team = Team(
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
            free_transfers=-1,
        )
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=3
        )
        expected = 12 * (10 + 20 + 30) - 4
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

        team = Team(
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
        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=1
        )
        expected = 12 * (10) - 3.2
        self.assertAlmostEqual(
            actual, expected, msg="Penalty applied but only one week horizon"
        )

    def test_discounted_reward_complex(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if gameweek == 1:
                    return self.epm_B[player_id]
                if gameweek == 2:
                    return self.epm_C[player_id]

        team = Team(
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
            free_transfers=5,
        )

        actual = Optimizer.discounted_reward(
            team, MockCalculator, gameweek=1, horizon=2, gamma=0.5
        )
        expected = 104 + 15 + 0.5 * (99 + 15)
        self.assertAlmostEqual(actual, expected)

    def test_optimize_team_1(self):
        # no candidates
        candidates = []
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 1)
        x_score, x_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            x_score, -2.4, "self.team has 1 free transfers corresponding to -2.4 points"
        )
        self.assertEqual(x_team.money_in_bank, 0)
        self.assertEqual(x_team.free_transfers, 1)

    def test_optimize_team_2(self):
        # cannot fit candidates in as not enough money or too many of one team
        candidates = [
            Player(element=200, name="Salah", position=3, club=20, cost=120),
            Player(element=300, name="Potato man", position=4, club=1, cost=40),
        ]
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 1)
        x_score, x_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            x_score, -2.4, "self.team has 1 free transfers corresponding to -2.4 points"
        )
        self.assertEqual(x_team.money_in_bank, 0)
        self.assertEqual(x_team.free_transfers, 1)

    def test_optimize_team_3(self):
        # one candidate who doesn't improve the team
        candidates = [
            Player(
                element=200,
                name="Candidate who does nothing for you",
                position=3,
                club=20,
                cost=70,
            )
        ]
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(third_best_score, -3.2, "One transfer made")
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 0)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(second_best_score, -3.2, "One transfer made")
        self.assertEqual(second_best_team.money_in_bank, 10)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(first_best_score, -2.4)
        self.assertEqual(first_best_team.money_in_bank, 0)
        self.assertEqual(first_best_team.free_transfers, 1)

    def test_optimize_team_4(self):
        # one candidate who dramatically improves the team and is set as captain, also 3 max transfers should not affect
        candidates = [Player(element=200, name="Doaky", position=4, club=20, cost=70)]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return 10 if player_id == 200 else 0

        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=3,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(third_best_score, -2.4, "No transfer made")
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 1)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(second_best_score, -3.2 + 2 * 10, "One transfer made")
        self.assertEqual(second_best_team.money_in_bank, 5)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(first_best_score, -3.2 + 2 * 10, "One transfer made")
        self.assertEqual(first_best_team.money_in_bank, 10)
        self.assertEqual(first_best_team.free_transfers, 0)

    def test_optimize_team_5(self):
        # one candidate who improves the team but not as good as the captain
        candidates = [Player(element=200, name="Doaky", position=4, club=20, cost=70)]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id == 7:
                    return 10
                if player_id == 200:
                    return 3
                return 0

        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertEqual(third_best_score, 10 + 10 - 2.4)
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 1)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertEqual(second_best_score, 10 + 10 + 3 - 3.2)
        self.assertEqual(second_best_team.money_in_bank, 5)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(first_best_score, 10 + 10 + 3 - 3.2)
        self.assertEqual(first_best_team.money_in_bank, 10)
        self.assertEqual(first_best_team.free_transfers, 0)

    def test_optimize_team_6(self):
        # one candidate who is bad for the next game but good over the long run - not as good as capitain
        candidates = [Player(element=200, name="Doaky", position=4, club=20, cost=70)]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id == 7:
                    return 10
                if player_id == 200:
                    if gameweek == 1:
                        return 0
                    if gameweek == 2:
                        return 4
                return 0

        max_transfers = 1
        epc = MockCalculator()
        gameweek = 1
        as_of_gameweek = 0

        # one week horizon
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertEqual(third_best_score, 10 + 10 - 3.2)
        self.assertEqual(third_best_team.money_in_bank, 5)
        self.assertEqual(third_best_team.free_transfers, 0)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertEqual(second_best_score, 10 + 10 - 3.2)
        self.assertEqual(second_best_team.money_in_bank, 10)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(first_best_score, 10 + 10 - 2.4)
        self.assertEqual(first_best_team.money_in_bank, 0)
        self.assertEqual(first_best_team.free_transfers, 1)

        # two week horizon
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=2,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertEqual(third_best_score, 20 + 20 - 2.4)
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 1)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertEqual(second_best_score, 20 + 20 + 4 - 3.2)
        self.assertEqual(second_best_team.money_in_bank, 5)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(first_best_score, 20 + 20 + 4 - 3.2)
        self.assertEqual(first_best_team.money_in_bank, 10)
        self.assertEqual(first_best_team.free_transfers, 0)

    def test_optimize_team_7(self):
        # transfer out two expensive players and non-expensive player for two average cost players who are better overall
        candidates = [
            Player.from_min_info(element=200, position=3, club=20, cost=70),
            Player.from_min_info(element=300, position=4, club=20, cost=70),
        ]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id in [200, 300]:
                    return 1
                else:
                    return 0

        max_transfers = 1
        epc = MockCalculator()
        gameweek = 1
        as_of_gameweek = 0

        # one week horizon
        top_three = Optimizer.optimize_team(
            self.team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=2,
            wildcard=True,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        second_best_score, second_best_team = heapq.heappop(top_three)
        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(
            first_best_score, 3
        )  # should be three from transferring in the two new players and wildcard
        self.assertEqual(first_best_team.money_in_bank, 20)
        self.assertEqual(first_best_team.free_transfers, -1)
        self.assertEqual(
            second_best_score, 3
        )  # should be three from transferring in the two new players and wildcard
        self.assertEqual(second_best_team.money_in_bank, 15)
        self.assertEqual(second_best_team.free_transfers, -1)
        self.assertEqual(
            third_best_score, 3
        )  # should be three from transferring in the two new players and wildcard
        self.assertEqual(third_best_team.money_in_bank, 10)
        self.assertEqual(third_best_team.free_transfers, -1)
