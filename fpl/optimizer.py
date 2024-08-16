from fpl import Player, Team, ExpectedPointsCalculator, Loader
from typing import Dict, Any, Type, List
import heapq

class Optimizer:
    @staticmethod
    def optimal_formation(team: Team, epc: Type[ExpectedPointsCalculator], gameweek: int) -> Dict[str, Any]:
        """
        Return optimal formation of an fpl team for a particular gameweek
        :param team:
        :param epc: expected points calculator
        :param gameweek: gameweek for which you want to optimal formation calculated for
        
        :return: Dictionary containing gkps, defs, mids, fwds, captain, expected points
        """
        
        def pop_n_elements(lst, n):
            popped_elements = set()
            for _ in range(n):
                try:
                    popped_elements.add(lst.pop())
                except IndexError:  # The list is empty
                    break
            return popped_elements
        
        # for each position create a list in increasing size of expected points
        gkps_sorted_list = sorted([(player, epc.get_expected_points(player.element, gameweek)) for player in team.gkps], key=lambda x: x[1])
        defs_sorted_list = sorted([(player, epc.get_expected_points(player.element, gameweek)) for player in team.defs], key=lambda x: x[1])
        mids_sorted_list = sorted([(player, epc.get_expected_points(player.element, gameweek)) for player in team.mids], key=lambda x: x[1])
        fwds_sorted_list = sorted([(player, epc.get_expected_points(player.element, gameweek)) for player in team.fwds], key=lambda x: x[1])
        
        # fill up the minimal number of players for each position
        gkps, defs, mids, fwds = set(), set(), set(), set()
        remaining_list = []
        gkps = pop_n_elements(gkps_sorted_list, Loader.get_position_info(1)["squad_min_play"])
        defs = pop_n_elements(defs_sorted_list, Loader.get_position_info(2)["squad_min_play"])
        mids = pop_n_elements(mids_sorted_list, Loader.get_position_info(3)["squad_min_play"])
        fwds = pop_n_elements(fwds_sorted_list, Loader.get_position_info(4)["squad_min_play"])
        
        # for the remaining players we pick the best
        remaining_list.extend(gkps_sorted_list + defs_sorted_list + mids_sorted_list + fwds_sorted_list)    
        remaining_list = sorted(remaining_list, key=lambda x: x[1])
        i = len(remaining_list)-1
        while len(gkps) + len(defs) + len(mids) + len(fwds) < 11:
            player, exp_points = remaining_list[i]
            if player.position == 1 and len(gkps) < Loader.get_position_info(1)["squad_max_play"]:
                gkps.add((player, exp_points))
            elif player.position == 2 and len(defs) < Loader.get_position_info(2)["squad_max_play"]:
                defs.add((player, exp_points))
            elif player.position == 3 and len(mids) < Loader.get_position_info(3)["squad_max_play"]:
                mids.add((player, exp_points))
            elif player.position == 4 and len(fwds) < Loader.get_position_info(4)["squad_max_play"]:
                fwds.add((player, exp_points))
            i -= 1
            
        # compute the total expected points and find the captain
        total_exp_points, max_exp_points, captain = 0, 0, None
        for player, exp_points in gkps | defs | mids | fwds:
            if exp_points > max_exp_points:
                captain = player
                max_exp_points = exp_points
            
            total_exp_points += exp_points
        
        # need to double the captain's points
        total_exp_points += max_exp_points
        
        return {
            "gkps": frozenset(x[0] for x in gkps),
            "defs": frozenset(x[0] for x in defs),
            "mids": frozenset(x[0] for x in mids),
            "fwds": frozenset(x[0] for x in fwds),
            "captain": captain,
            "total_exp_points": total_exp_points
        }
    
    @staticmethod
    def discounted_reward(team: Team,
                          epc: Type[ExpectedPointsCalculator],
                          gameweek: int,
                          horizon: int,
                          gamma: float = 1,
                          wildcard: bool = False
                         ) -> float:
        """The discounted reward you can expect from your team over a particular horizon
        :param team:
        :param epc: expected points calculator
        :param gameweek: gameweek for which you want to start accumulating the reward
        :param horizon: how many gameweeks you want to accumulate the reward
        :param gamma: discount factor
        :param wildcard: if you are wildcarding or not, this is a switch to turn off the transfer adjustment
        
        :return: discounted reward of your team over a particular horizon including a transfer adjustment
        """
        # draw a graph - each free transfer is roughly worth 0.8 points
        transfer_adjustment = 0
        if team.free_transfers <= -1:
            transfer_adjustment = 4 * team.free_transfers
        elif team.free_transfers >= 4:
            transfer_adjustment = 0
        else:
            transfer_adjustment = -4 + (team.free_transfers + 1) * 0.8
        
        # unlimited transfers
        if wildcard: transfer_adjustment = 0
            
        discounted_reward = 0
        discount_factor = 1
        for h in range(horizon):
            d = Optimizer.optimal_formation(team, epc, gameweek + h)
            discounted_reward += discount_factor * d["total_exp_points"]
            discount_factor *= gamma
            
        return discounted_reward + transfer_adjustment
    
    @staticmethod
    def optimize_team(team: Team,
                      candidates: List[Player],
                      epc: Type[ExpectedPointsCalculator],
                      gameweek: int,
                      horizon: int,
                      max_transfers: int,
                      gamma: float = 1,
                      wildcard: bool = False
                     ) -> List[Team]:
        """
        Find top three teams

        :param team: team you wish to optimize
        :param candidates: list of player candidates you wish to transfer in
        :param max_transfers: maximum number of transfers you wish to take on
        
        :return: list of top three teams based on score
        """
        top_three = [(Optimizer.discounted_reward(team, epc, gameweek, horizon, gamma, wildcard), team)]
        heapq.heapify(top_three)
        heap_set = set([team])

        currLayer = [team]
        for i in range(max_transfers):
            nextLayer = []
            for u_team in currLayer:
                for candidate in candidates:
                    out_players = None
                    if candidate.position == 1:
                        out_players = u_team.gkps
                    elif candidate.position == 2:
                        out_players = u_team.defs
                    elif candidate.position == 3:
                        out_players = u_team.mids
                    elif candidate.position == 4:
                        out_players = u_team.fwds
                    else:
                        raise ValueError("Invalid player position.")
                    if candidate not in out_players:
                        for out_player in out_players:
                            v_team = u_team.transfer_player(out_player, candidate)
                            v_score = Optimizer.discounted_reward(v_team, epc, gameweek, horizon, gamma, wildcard)
                            if v_team.is_feasible and (v_team not in heap_set):
                                if len(top_three) < 3:
                                    heapq.heappush(top_three, (v_score, v_team))
                                    heap_set.add(v_team)
                                else:
                                    _, team_popped = heapq.heappushpop(top_three, (v_score, v_team))
                                    heap_set.add(v_team)
                                    heap_set.remove(team_popped)
                            nextLayer.append(v_team)
            currLayer = nextLayer

        return top_three
        