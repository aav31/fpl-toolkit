"""
This module defines the Formation class, which represents a valid formation of players in a Fantasy Premier League (FPL) team.
The Formation class includes the 11 outfield players which can play in the four types of position, the captain and total expected points.
It also provides post initialization checking to see that the team is indeed the right size.

Available functions:
- __post_init__: Validates the the formation after initialization.
- __str__: Return a string representation of the formation.
"""

from dataclasses import dataclass
from typing import FrozenSet
from fpl import Player, Loader


@dataclass(frozen=True)
class Formation:
    total_exp_points: int
    gkps: FrozenSet[Player]
    defs: FrozenSet[Player]
    mids: FrozenSet[Player]
    fwds: FrozenSet[Player]
    captain: Player

    def __post_init__(self):
        """Validates the the formation after initialization.

        :raises ValueError: If there isn't 11 players or we have an invalid formation.
        :raises TypeError: If any of the attributes are not of the expected type.
        """
        if not isinstance(self.gkps, frozenset) or not all(
            isinstance(player, Player) for player in self.gkps
        ):
            raise TypeError("gkps must be a FrozenSet of Player instances")
        if not isinstance(self.defs, frozenset) or not all(
            isinstance(player, Player) for player in self.defs
        ):
            raise TypeError("defs must be a FrozenSet of Player instances")
        if not isinstance(self.mids, frozenset) or not all(
            isinstance(player, Player) for player in self.mids
        ):
            raise TypeError("mids must be a FrozenSet of Player instances")
        if not isinstance(self.fwds, frozenset) or not all(
            isinstance(player, Player) for player in self.fwds
        ):
            raise TypeError("fwds must be a FrozenSet of Player instances")

        total_players = (
            len(self.gkps) + len(self.defs) + len(self.mids) + len(self.fwds)
        )
        if total_players != 11:
            raise ValueError(
                f"Total number of players must be 11, but got {total_players}"
            )

        min_play_gkps = Loader.get_position_info(1)["squad_min_play"]
        max_play_gkps = Loader.get_position_info(1)["squad_max_play"]
        min_play_defs = Loader.get_position_info(2)["squad_min_play"]
        max_play_defs = Loader.get_position_info(2)["squad_max_play"]
        min_play_mids = Loader.get_position_info(3)["squad_min_play"]
        max_play_mids = Loader.get_position_info(3)["squad_max_play"]
        min_play_fwds = Loader.get_position_info(4)["squad_min_play"]
        max_play_fwds = Loader.get_position_info(4)["squad_max_play"]

        if not (min_play_gkps <= len(self.gkps) <= max_play_gkps):
            raise ValueError(
                f"Total number of goalkeepers ({len(self.gkps)}) is out of range ({min_play_gkps}-{max_play_gkps})"
            )

        if not (min_play_defs <= len(self.defs) <= max_play_defs):
            raise ValueError(
                f"Total number of defenders ({len(self.defs)}) is out of range ({min_play_defs}-{max_play_defs})"
            )

        if not (min_play_mids <= len(self.mids) <= max_play_mids):
            raise ValueError(
                f"Total number of midfielders ({len(self.mids)}) is out of range ({min_play_mids}-{max_play_mids})"
            )

        if not (min_play_fwds <= len(self.fwds) <= max_play_fwds):
            raise ValueError(
                f"Total number of forwards ({len(self.fwds)}) is out of range ({min_play_fwds}-{max_play_fwds})"
            )

    def __str__(self):
        """Return a string representation of the formation.

        :return: A string representation of the formation, including players in each position, money in bank, and free transfers.
        """
        result = ""
        position_delimiter = "-" * 75 + "\n"

        result += position_delimiter
        result += "{GKPS}\n"
        for player in sorted(list(self.gkps)):
            result += "{}\n".format(player)

        result += position_delimiter
        result += "{DEFS}\n"
        for player in sorted(list(self.defs)):
            result += "{}\n".format(player)

        result += position_delimiter
        result += "{MIDS}\n"
        for player in sorted(list(self.mids)):
            result += "{}\n".format(player)

        result += position_delimiter
        result += "{FWDS}\n"
        for player in sorted(list(self.fwds)):
            result += "{}\n".format(player)

        result += position_delimiter
        result += "TOTAL EXPECTED POINTS: {}\n".format(self.total_exp_points)
        result += "CAPTAIN: {}".format(self.captain)
        return result
