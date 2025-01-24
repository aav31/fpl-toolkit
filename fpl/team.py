"""
This module defines the Team class, which represents a Fantasy Premier League (FPL) team.
The Team class includes attributes such as the team's money in the bank, free transfers, and sets of players in different positions.
It also provides methods for comparing teams, checking team feasibility, and transferring players.

Available functions:
- __post_init__: Validates the types of the attributes after the object is initialized.
- __eq__: Checks if two teams are equal based on their attributes.
- __lt__: Compares two teams based on their money in the bank and free transfers.
- __str__: Returns a string representation of the team.
- is_feasible: Checks if the team is feasible based on FPL rules.
- transfer_player: Transfers a player in and out of the team and returns a new team instance.
"""

from collections import defaultdict
from fpl import Player
from typing import FrozenSet
from dataclasses import dataclass, replace
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Team:
    money_in_bank: int
    free_transfers: int
    gkps: FrozenSet[Player]
    defs: FrozenSet[Player]
    mids: FrozenSet[Player]
    fwds: FrozenSet[Player]

    def __post_init__(self):
        """Validate the types of the attributes after the object is initialized.
        
        :raises TypeError: If any of the attributes are not of the expected type.
        """
        if not isinstance(self.money_in_bank, int):
            raise TypeError("money_in_bank must be an integer")
        if not isinstance(self.free_transfers, int):
            raise TypeError("free_transfers must be an integer")
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

    def __eq__(self, other: "Team") -> bool:
        """Check if two teams are equal based on their sets of players, money in bank, and free transfers.
        Teams are equal when their sets of players, money in bank, free transfers are equal.
        
        :param other: Another Team instance to compare with.

        :return: True if the teams have the same sets of players, money in bank, and free transfers, False otherwise.
        """
        if self.gkps != other.gkps:
            return False
        if self.defs != other.defs:
            return False
        if self.mids != other.mids:
            return False
        if self.fwds != other.fwds:
            return False
        return (self.money_in_bank == other.money_in_bank) and (
            self.free_transfers == other.free_transfers
        )

    def __lt__(self, other: "Team") -> bool:
        """Compare two teams based on their money in the bank and free transfers.
        One team is worse than the the other when its money in the bank is less than the other.
        If the money in the bank is equal, then it goes to free transfers.
        
        :param other: Another Team instance to compare with.

        :return: True if this team's money in the bank is less than the other team's, or if they are equal, 
                 if this team's free transfers are less than the other team's, False otherwise.
        """
        return (self.money_in_bank, self.free_transfers) < (
            other.money_in_bank,
            other.free_transfers,
        )

    def __str__(self):
        """Return a string representation of the team.

        :return: A string representation of the team, including players in each position, money in bank, and free transfers.
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
        result += "MONEY IN BANK: {}\n".format(self.money_in_bank)
        result += "FREE TRANSFERS: {}".format(self.free_transfers)
        return result

    @property
    def is_feasible(self) -> bool:
        """Return whether an FPL team is feasible or not.

        :return: bool indicating whether the team has enough money, players in one club < 3, 
                 and the correct number of players in each position.
        """
        if self.money_in_bank < 0:
            return False

        club_count = defaultdict(int)
        for player in self.gkps:
            club_count[player.club] += 1
        for player in self.defs:
            club_count[player.club] += 1
        for player in self.mids:
            club_count[player.club] += 1
        for player in self.fwds:
            club_count[player.club] += 1
        if any(n_players > 3 for n_players in club_count.values()):
            return False

        if len(self.gkps) != 2:
            return False
        if len(self.defs) != 5:
            return False
        if len(self.mids) != 5:
            return False
        if len(self.fwds) != 3:
            return False

        return True

    def transfer_player(self, out_player: Player, in_player: Player) -> "Team":
        """Make a single transfer, giving a new team.

        :param out_player: Player to be transferred out.
        :param in_player: Player to be transferred in.

        :return: A copy of the team with the updated squad, money in bank, and free transfers.

        :raises ValueError: If the positions of the players being transferred do not match.
        """
        if out_player.position != in_player.position:
            raise ValueError("Both players must have the same position for a transfer.")

        new_money_in_bank = self.money_in_bank + out_player.cost - in_player.cost
        new_free_transfers = self.free_transfers - 1

        if out_player.position == 1:
            new_gkps = frozenset(
                player for player in self.gkps if player != out_player
            ) | frozenset([in_player])
            return replace(
                self,
                gkps=new_gkps,
                money_in_bank=new_money_in_bank,
                free_transfers=new_free_transfers,
            )
        elif out_player.position == 2:
            new_defs = frozenset(
                player for player in self.defs if player != out_player
            ) | frozenset([in_player])
            return replace(
                self,
                defs=new_defs,
                money_in_bank=new_money_in_bank,
                free_transfers=new_free_transfers,
            )
        elif out_player.position == 3:
            new_mids = frozenset(
                player for player in self.mids if player != out_player
            ) | frozenset([in_player])
            return replace(
                self,
                mids=new_mids,
                money_in_bank=new_money_in_bank,
                free_transfers=new_free_transfers,
            )
        elif out_player.position == 4:
            new_fwds = frozenset(
                player for player in self.fwds if player != out_player
            ) | frozenset([in_player])
            return replace(
                self,
                fwds=new_fwds,
                money_in_bank=new_money_in_bank,
                free_transfers=new_free_transfers,
            )
        else:
            raise ValueError("Invalid player position.")
