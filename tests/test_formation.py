from unittest import TestCase, skip
from unittest.mock import patch
from dataclasses import FrozenInstanceError
from fpl import Player, Formation


class TestFormation(TestCase):
    """
    Unit tests for the Formation dataclass to ensure proper initialization and validation.
    """

    @staticmethod
    def side_effect(position_id: int) -> dict:
        """Function to provide the side_effect for the mock of fpl.Loader.get_position_info"""
        if position_id == 1:
            return {"squad_min_play": 1, "squad_max_play": 1}
        elif position_id == 2:
            return {"squad_min_play": 3, "squad_max_play": 5}
        elif position_id == 3:
            return {"squad_min_play": 2, "squad_max_play": 5}
        elif position_id == 4:
            return {"squad_min_play": 1, "squad_max_play": 3}
        else:
            self.fail("Called with an invalid position integer")

    def setUp(self):
        self.gkp = Player(element=1, name="GKP1", position=1, club=1, cost=50)
        self.def1 = Player(element=2, name="DEF1", position=2, club=1, cost=50)
        self.def2 = Player(element=3, name="DEF2", position=2, club=1, cost=50)
        self.def3 = Player(element=4, name="DEF3", position=2, club=1, cost=50)
        self.def4 = Player(element=5, name="DEF4", position=2, club=1, cost=50)
        self.mids1 = Player(element=6, name="MID1", position=3, club=1, cost=50)
        self.mids2 = Player(element=7, name="MID2", position=3, club=1, cost=50)
        self.mids3 = Player(element=8, name="MID3", position=3, club=1, cost=50)
        self.fwd1 = Player(element=9, name="FWD1", position=4, club=1, cost=50)
        self.fwd2 = Player(element=10, name="FWD2", position=4, club=1, cost=50)
        self.fwd3 = Player(element=11, name="FWD3", position=4, club=1, cost=50)
        self.fwd4 = Player(element=12, name="FWD4", position=4, club=1, cost=50)
        self.captain = self.fwd1

    @patch("fpl.Loader.get_position_info")
    def test_valid_formation(self, mock_get_position_info):
        mock_get_position_info.side_effect = self.side_effect
        formation = Formation(
            total_exp_points=100,
            gkps=frozenset([self.gkp]),
            defs=frozenset([self.def1, self.def2, self.def3, self.def4]),
            mids=frozenset([self.mids1, self.mids2, self.mids3]),
            fwds=frozenset([self.fwd1, self.fwd2, self.fwd3]),
            captain=self.captain,
        )
        total_players = (
            len(formation.gkps)
            + len(formation.defs)
            + len(formation.mids)
            + len(formation.fwds)
        )
        self.assertEqual(total_players, 11)
        self.assertEqual(formation.captain.name, "FWD1")

    @patch("fpl.Loader.get_position_info")
    def test_invalid_formation_type_error(self, mock_get_position_info):
        mock_get_position_info.side_effect = self.side_effect
        with self.assertRaises(TypeError, msg="Goalkeeper isn't the correct type"):
            Formation(
                total_exp_points=100,
                gkps={"allison"},
                defs=frozenset([self.def1, self.def2, self.def3, self.def4]),
                mids=frozenset([self.mids1, self.mids2, self.mids3]),
                fwds=frozenset([self.fwd1, self.fwd2, self.fwd3]),
                captain=self.captain,
            )

    @patch("fpl.Loader.get_position_info")
    def test_invalid_formation_value_error(self, mock_get_position_info):
        mock_get_position_info.side_effect = self.side_effect
        with self.assertRaises(ValueError, msg="Not 11 players"):
            Formation(
                total_exp_points=100,
                gkps=frozenset([self.gkp]),
                defs=frozenset([self.def1, self.def2]),
                mids=frozenset([self.mids1, self.mids2, self.mids3]),
                fwds=frozenset([self.fwd1, self.fwd2, self.fwd3]),
                captain=self.captain,
            )

        with self.assertRaises(ValueError, msg="Too many strikers"):
            Formation(
                total_exp_points=100,
                gkps=frozenset([self.gkp]),
                defs=frozenset([self.def1, self.def2, self.def3]),
                mids=frozenset([self.mids1, self.mids2, self.mids3]),
                fwds=frozenset([self.fwd1, self.fwd2, self.fwd3, self.fwd4]),
                captain=self.captain,
            )

    @patch("fpl.Loader.get_position_info")
    def test_frozen_instance(self, mock_get_position_info):
        mock_get_position_info.side_effect = self.side_effect
        formation = Formation(
            total_exp_points=100,
            gkps=frozenset([self.gkp]),
            defs=frozenset([self.def1, self.def2, self.def3, self.def4]),
            mids=frozenset([self.mids1, self.mids2, self.mids3]),
            fwds=frozenset([self.fwd1, self.fwd2, self.fwd3]),
            captain=self.captain,
        )
        with self.assertRaises(
            FrozenInstanceError, msg="Can't change fields of frozen instance"
        ):
            formation.total_exp_points = 200

    @skip("TODO: Implement this test")
    def test_str(self):
        pass
