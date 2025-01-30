"""
Unit tests for the optimizer module.
Test cases:
- TestOptimizerOptimalFormation: Unit tests for the optimal_formation method of the Optimizer class.
- TestOptimizerDiscountedReward: Unit tests for the discounted_reward method of the Optimizer class.
- TestOptimizerOptimizeTeam: Unit tests for the optimize_team method of the Optimizer class.
"""

import unittest
import heapq
from fpl import ExpectedPointsCalculator, Team, Player, Optimizer


def setUpModule():
    global gkp_club_1, gkp_club_2, def_club_1, def_club_2, def_club_3, def_club_4, def_club_5
    global mid_club_1, mid_club_2, mid_club_3, mid_club_4, mid_club_5
    global fwd_club_1, fwd_club_2, fwd_club_3, fwd_club_4, fwd_club_5
    global gkps, defs, mids, fwds
    global team

    # GKPs
    gkp_club_1 = Player.from_min_info(element=1, position=1, club=1, cost=40)
    gkp_club_2 = Player.from_min_info(element=2, position=1, club=2, cost=45)

    # DEFs
    def_club_1 = Player.from_min_info(element=3, position=2, club=1, cost=40)
    def_club_2 = Player.from_min_info(element=4, position=2, club=2, cost=45)
    def_club_3 = Player.from_min_info(element=5, position=2, club=3, cost=50)
    def_club_4 = Player.from_min_info(element=6, position=2, club=4, cost=55)
    def_club_5 = Player.from_min_info(element=7, position=2, club=5, cost=60)

    # MIDs
    mid_club_1 = Player.from_min_info(element=8, position=3, club=1, cost=45)
    mid_club_2 = Player.from_min_info(element=9, position=3, club=2, cost=50)
    mid_club_3 = Player.from_min_info(element=10, position=3, club=3, cost=60)
    mid_club_4 = Player.from_min_info(element=11, position=3, club=4, cost=70)
    mid_club_5 = Player.from_min_info(element=12, position=3, club=5, cost=80)

    # FWDs
    fwd_club_1 = Player.from_min_info(element=16, position=4, club=1, cost=45)
    fwd_club_2 = Player.from_min_info(element=17, position=4, club=2, cost=55)
    fwd_club_3 = Player.from_min_info(element=13, position=4, club=3, cost=60)
    fwd_club_4 = Player.from_min_info(element=14, position=4, club=4, cost=75)
    fwd_club_5 = Player.from_min_info(element=15, position=4, club=5, cost=80)

    # Frozensets
    gkps = frozenset([gkp_club_1, gkp_club_2])
    defs = frozenset([def_club_1, def_club_2, def_club_3, def_club_4, def_club_5])
    mids = frozenset([mid_club_1, mid_club_2, mid_club_3, mid_club_4, mid_club_5])
    fwds = frozenset([fwd_club_3, fwd_club_4, fwd_club_5])

    team = Team(
        gkps=gkps, defs=defs, mids=mids, fwds=fwds, money_in_bank=0, free_transfers=1
    )


class TestOptimizerOptimalFormation(unittest.TestCase):
    """Unit tests for the optimal_formation method of the Optimizer class."""

    def setUp(self):
        self.player_map = {
            1: gkp_club_1,
            2: gkp_club_2,
            3: def_club_1,
            4: def_club_2,
            5: def_club_3,
            6: def_club_4,
            7: def_club_5,
            8: mid_club_1,
            9: mid_club_2,
            10: mid_club_3,
            11: mid_club_4,
            12: mid_club_5,
            13: fwd_club_3,
            14: fwd_club_4,
            15: fwd_club_5,
        }

        self.expected_points_map_A = {
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
        self.expected_points_map_B = {
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
        self.expected_points_map_C = {
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
        self.expected_points_map_D = {
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

    def test_optimal_formation_A_442(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.expected_points_map_A[player_id]

        result = Optimizer.optimal_formation(team, MockCalculator, 0)
        # check formation is 442 as expected
        self.assertEqual(result["gkps"], {self.player_map[1]})
        self.assertEqual(
            result["defs"],
            {
                self.player_map[3],
                self.player_map[4],
                self.player_map[5],
                self.player_map[6],
            },
        )
        self.assertEqual(
            result["mids"],
            {
                self.player_map[8],
                self.player_map[9],
                self.player_map[10],
                self.player_map[11],
            },
        )
        self.assertEqual(result["fwds"], {self.player_map[13], self.player_map[14]})
        self.assertAlmostEqual(result["total_exp_points"], 60)

    def test_optimal_formation_B_343(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.expected_points_map_B[player_id]

        result = Optimizer.optimal_formation(team, MockCalculator, 0)
        # check formation is 343 as expected
        self.assertEqual(result["gkps"], {self.player_map[2]})
        self.assertEqual(
            result["defs"], {self.player_map[5], self.player_map[6], self.player_map[7]}
        )
        self.assertEqual(
            result["mids"],
            {
                self.player_map[9],
                self.player_map[10],
                self.player_map[11],
                self.player_map[12],
            },
        )
        self.assertEqual(
            result["fwds"],
            {self.player_map[13], self.player_map[14], self.player_map[15]},
        )
        self.assertAlmostEqual(result["total_exp_points"], 119)

    def test_optimal_formation_C_541(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.expected_points_map_C[player_id]

        result = Optimizer.optimal_formation(team, MockCalculator, 0)
        # check formation is 541 as expected
        self.assertEqual(result["gkps"], {self.player_map[1]})
        self.assertEqual(
            result["defs"],
            {
                self.player_map[3],
                self.player_map[4],
                self.player_map[5],
                self.player_map[6],
                self.player_map[7],
            },
        )
        self.assertEqual(
            result["mids"],
            {
                self.player_map[8],
                self.player_map[9],
                self.player_map[10],
                self.player_map[11],
            },
        )
        self.assertEqual(result["fwds"], {self.player_map[13]})
        self.assertAlmostEqual(result["total_exp_points"], 114)

    def test_optimal_formation_D_523(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return self.expected_points_map_D[player_id]

        result = Optimizer.optimal_formation(team, MockCalculator, 0)
        # check formation is 523 as expected
        self.assertEqual(result["gkps"], {self.player_map[2]})
        self.assertEqual(
            result["defs"],
            {
                self.player_map[3],
                self.player_map[4],
                self.player_map[5],
                self.player_map[6],
                self.player_map[7],
            },
        )
        self.assertEqual(result["mids"], {self.player_map[11], self.player_map[12]})
        self.assertEqual(
            result["fwds"],
            {self.player_map[13], self.player_map[14], self.player_map[15]},
        )
        self.assertAlmostEqual(result["total_exp_points"], 21)

    def test_captain_functionality(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id == 1:
                    return 10.0  # Normal expected points for player 1
                return 0.0  # Expected points for other players

        result = Optimizer.optimal_formation(team, MockCalculator, 0)

        # Check if captain's points are doubled
        self.assertEqual(
            result["gkps"], {self.player_map[1]}, "Goalkeeper 1 is the captain"
        )
        self.assertAlmostEqual(
            result["total_exp_points"], 20.0, "Check captain's points are doubled"
        )


class TestOptimizerDiscountedReward(unittest.TestCase):
    """Unit tests for the discounted_reward method of the Optimizer class."""

    def setUp(self):
        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if gameweek == 1:
                    return 10
                if gameweek == 2:
                    return 20
                if gameweek == 3:
                    return 30

        self.mock_calculator = MockCalculator

    def test_transfer_adjustment_with_five_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=5,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = 12 * (10 + 20 + 30)  # 12 players including captain for each gameweek
        self.assertAlmostEqual(
            actual, expected, msg="No transfer adjustment should be applied"
        )

    def test_transfer_adjustment_with_four_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=4,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = 12 * (10 + 20 + 30)  # 12 players including captain for each gameweek
        self.assertAlmostEqual(
            actual, expected, msg="No transfer adjustment should be applied"
        )

    def test_transfer_adjustment_with_three_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=3,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = (
            12 * (10 + 20 + 30) - 0.8
        )  # 12 players including captain for each gameweek minus penalty
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

    def test_transfer_adjustment_with_two_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=2,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = (
            12 * (10 + 20 + 30) - 1.6
        )  # 12 players including captain for each gameweek minus penalty
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

    def test_transfer_adjustment_with_zero_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=0,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = (
            12 * (10 + 20 + 30) - 3.2
        )  # 12 players including captain for each gameweek minus penalty
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

    def test_transfer_adjustment_with_negative_free_transfers(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=-1,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=3,
        )
        expected = 12 * (10 + 20 + 30) - 4
        self.assertAlmostEqual(actual, expected, msg="Penalty applied")

    def test_horizon(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=5,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=1,
        )
        expected = 12 * 10
        self.assertAlmostEqual(actual, expected, msg="one week")

    def test_gamma(self):
        actual = Optimizer.discounted_reward(
            Team(
                gkps=gkps,
                defs=defs,
                mids=mids,
                fwds=fwds,
                money_in_bank=0,
                free_transfers=5,
            ),
            self.mock_calculator,
            gameweek=1,
            horizon=2,
            gamma=0.5,
        )
        expected_points_for_week_1 = 12 * 10
        expected_points_for_week_2 = 12 * 20
        expected = expected_points_for_week_1 + 0.5 * expected_points_for_week_2
        self.assertAlmostEqual(actual, expected)


class TestOptimizerOptimizeTeam(unittest.TestCase):
    """Unit tests for the optimize_team method of the Optimizer class."""

    def setUp(self):
        class MockCalculatorZero(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return 0

        self.epcZero = MockCalculatorZero

    def test_optimize_team_no_candidates(self):
        candidates = []
        top_three = Optimizer.optimize_team(
            team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(
            len(top_three), 1, "Only one team possible because no candidates specified"
        )
        x_score, x_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            x_score, -2.4, "self.team has 1 free transfers corresponding to -2.4 points"
        )
        self.assertEqual(x_team.money_in_bank, 0, "No transfers made")
        self.assertEqual(x_team.free_transfers, 1, "No transfers made")

    def test_optimize_team_invalid_candidates(self):
        # cannot fit candidates in as not enough money or too many of one team
        candidates = [
            Player(element=200, name="Salah", position=3, club=20, cost=120),
            Player(element=300, name="Potato man", position=4, club=1, cost=40),
        ]
        top_three = Optimizer.optimize_team(
            team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(
            len(top_three),
            1,
            "Invalid candidates so only the original team is feasible",
        )
        x_score, x_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            x_score, -2.4, "self.team has 1 free transfers corresponding to -2.4 points"
        )
        self.assertEqual(x_team.money_in_bank, 0)
        self.assertEqual(x_team.free_transfers, 1)

    def test_optimize_team_neutral_candidate(self):
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
            team,
            candidates,
            epc=self.epcZero,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            third_best_score,
            -3.2,
            "One transfer made - transferred out striker costing 70",
        )
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 0)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            second_best_score,
            -3.2,
            "One transfer made - transferred out striker costing 80",
        )
        self.assertEqual(second_best_team.money_in_bank, 10)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(first_best_score, -2.4, "No transfers made")
        self.assertEqual(first_best_team.money_in_bank, 0)
        self.assertEqual(first_best_team.free_transfers, 1)

    def test_optimize_team_amazing_candidate(self):
        # one candidate who dramatically improves the team and is set as captain
        candidates = [Player(element=200, name="Doaky", position=4, club=20, cost=70)]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                return 10 if player_id == 200 else 0

        top_three = Optimizer.optimize_team(
            team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            third_best_score,
            -2.4,
            "No transfer made can't transfer out fwd_club_3 out as too cheap",
        )
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 1)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            second_best_score,
            -3.2 + 2 * 10,
            "One transfer made - fwd_club_4 costing 75 out",
        )
        self.assertEqual(second_best_team.money_in_bank, 5)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertAlmostEqual(
            first_best_score,
            -3.2 + 2 * 10,
            "One transfer made - fwd_club_5 costing 80 out",
        )
        self.assertEqual(first_best_team.money_in_bank, 10)
        self.assertEqual(first_best_team.free_transfers, 0)

    def test_optimize_team_good_candidate(self):
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
            team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=1,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        self.assertEqual(
            third_best_score,
            10 + 10 - 2.4,
            "No transfer made can't transfer out fwd_club_3 out as too cheap",
        )
        self.assertEqual(third_best_team.money_in_bank, 0)
        self.assertEqual(third_best_team.free_transfers, 1)

        second_best_score, second_best_team = heapq.heappop(top_three)
        self.assertEqual(
            second_best_score,
            10 + 10 + 3 - 3.2,
            "One transfer made - fwd_club_4 costing 75 out",
        )
        self.assertEqual(second_best_team.money_in_bank, 5)
        self.assertEqual(second_best_team.free_transfers, 0)

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(
            first_best_score,
            10 + 10 + 3 - 3.2,
            "One transfer made - fwd_club_5 costing 80 out",
        )
        self.assertEqual(first_best_team.money_in_bank, 10)
        self.assertEqual(first_best_team.free_transfers, 0)

    def test_optimize_team_horizon(self):
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

        # one week horizon
        top_three = Optimizer.optimize_team(
            team,
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
        self.assertEqual(
            first_best_team.free_transfers,
            1,
            "Based on a one week horizon you shouldn't transfer him in",
        )

        # two week horizon
        top_three = Optimizer.optimize_team(
            team,
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
        self.assertEqual(
            second_best_team.money_in_bank,
            5,
            "Sold striker worth 75 bought striker worth 70",
        )
        self.assertEqual(
            second_best_team.free_transfers,
            0,
            "Based on two week horizon you should transfer him in",
        )

        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(first_best_score, 20 + 20 + 4 - 3.2)
        self.assertEqual(
            first_best_team.money_in_bank,
            10,
            "Sold striker worth 80 bought striker worth 70",
        )
        self.assertEqual(
            first_best_team.free_transfers,
            0,
            "Based on two week horizon you should transfer him in",
        )

    def test_optimize_team_two_candidates(self):
        candidates = [
            Player.from_min_info(element=200, position=3, club=20, cost=70),
            Player.from_min_info(element=300, position=4, club=20, cost=70),
        ]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id in [200, 300]:
                    return 5
                else:
                    return 0

        top_three = Optimizer.optimize_team(
            team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=2,
            wildcard=False,
        )
        self.assertEqual(len(top_three), 3)

        third_best_score, third_best_team = heapq.heappop(top_three)
        second_best_score, second_best_team = heapq.heappop(top_three)
        first_best_score, first_best_team = heapq.heappop(top_three)
        self.assertEqual(
            first_best_score,
            5 + 5 + 5 - 4,
            "Two new players, captain one of them lose points for the transfer",
        )
        self.assertEqual(first_best_team.money_in_bank, 20)
        self.assertEqual(first_best_team.free_transfers, -1)
        self.assertEqual(
            second_best_score,
            5 + 5 + 5 - 4,
            "Two new players, captain one of them lose points for the transfer",
        )
        self.assertEqual(second_best_team.money_in_bank, 15)
        self.assertEqual(second_best_team.free_transfers, -1)
        self.assertEqual(
            third_best_score,
            5 + 5 + 5 - 4,
            "Two new players, captain one of them lose points for the transfer",
        )
        self.assertEqual(third_best_team.money_in_bank, 10)
        self.assertEqual(third_best_team.free_transfers, -1)

    def test_optimize_team_max_transfers(self):
        candidates = [
            Player.from_min_info(element=200, position=3, club=20, cost=70),
            Player.from_min_info(element=300, position=4, club=20, cost=70),
        ]

        class MockCalculator(ExpectedPointsCalculator):
            def get_expected_points(player_id: int, gameweek: int) -> float:
                if player_id in [200, 300]:
                    return 5
                else:
                    return 0

        top_three_one_max_transfers = Optimizer.optimize_team(
            team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=1,
            wildcard=False,
        )

        top_three_two_max_transfers = Optimizer.optimize_team(
            team,
            candidates,
            epc=MockCalculator,
            gameweek=1,
            horizon=1,
            max_transfers=2,
            wildcard=False,
        )

        self.assertEqual(len(top_three_one_max_transfers), 3)
        _, _ = heapq.heappop(top_three_one_max_transfers)
        _, _ = heapq.heappop(top_three_one_max_transfers)
        first_best_score_one_max_transfers, first_best_team_one_max_transfers = (
            heapq.heappop(top_three_one_max_transfers)
        )
        self.assertEqual(
            first_best_score_one_max_transfers,
            5 + 5 - 3.2,
            "One new player as the captain",
        )
        self.assertEqual(
            first_best_team_one_max_transfers.money_in_bank,
            10,
            "Only one player transferred out to net 10",
        )
        self.assertEqual(first_best_team_one_max_transfers.free_transfers, 0)

        self.assertEqual(len(top_three_two_max_transfers), 3)
        _, _ = heapq.heappop(top_three_two_max_transfers)
        _, _ = heapq.heappop(top_three_two_max_transfers)
        first_best_score_two_max_transfers, first_best_team_two_max_transfers = (
            heapq.heappop(top_three_two_max_transfers)
        )
        self.assertEqual(
            first_best_score_two_max_transfers,
            5 + 5 + 5 - 4,
            "Two new players, captain one of them lose points for the transfer",
        )
        self.assertEqual(
            first_best_team_two_max_transfers.money_in_bank,
            20,
            "Two players transferred out to make 20 profit",
        )
        self.assertEqual(first_best_team_two_max_transfers.free_transfers, -1)

    @unittest.skip("TODO: Implement this test")
    def test_optimize_team_wildcard(self):
        pass

    @unittest.skip("TODO: Implement this test")
    def test_optimize_team_gamma(self):
        pass
