import copy
import heapq
from collections import defaultdict
from player import Player
from expected_points_calculator import ExpectedPointsCalculator
from typing import List, Dict, Tuple
from fpl_loader import FplLoader
from functools import total_ordering

@total_ordering
class Team:
    def __init__(self, player_list: List[Player], money_in_bank: int, free_transfers: int):
        '''
        Representation of a team in FPL
        '''
        self.players = defaultdict(set) # mapping of position to List of players i.e. int: List[Player]
        for player in player_list:
            self.players[player.position].add(player)
        
        self.money_in_bank = money_in_bank
        self.free_transfers = free_transfers
        
    def __eq__(self, other: 'Team'):
        for element_type in range(1, 5):
            if self.players[element_type] != other.players[element_type]:
                return False
        return (self.money_in_bank == other.money_in_bank) and (self.free_transfers == other.free_transfers)
    
    def __lt__(self, other: 'Team'):
        return (self.money_in_bank, self.free_transfers) < (other.money_in_bank, other.free_transfers)
    
    def __hash__(self):
        tuple_1 = tuple(sorted(list(self.players[1])))
        tuple_2 = tuple(sorted(list(self.players[2])))
        tuple_3 = tuple(sorted(list(self.players[3])))
        tuple_4 = tuple(sorted(list(self.players[4])))
        return hash( (tuple_1, tuple_2, tuple_3, tuple_4, self.money_in_bank, self.free_transfers) )
            
    def __str__(self):
        result = ''
        position_delimiter = '-' * 75 + '\n'
        for position, player_list in sorted(self.players.items()):
            result += position_delimiter
            position_name_short = FplLoader.get_position_info(position)['singular_name_short']
            result += '{}\n'.format(position_name_short)
            for player in player_list:
                result += "{}\n".format(player)
        result += position_delimiter
        result += 'MONEY IN BANK: {}\n'.format(self.money_in_bank)
        result += 'FREE TRANSFERS: {}'.format(self.free_transfers)
        return result
        
    def is_feasible(self) -> bool:
        '''
        Return whether an FPL team is feasible or not
        :return: bool indicating whether enough money, players in one club < 3, correct number players in each position
        '''
        if self.money_in_bank < 0: return False
        
        club_count = defaultdict(int)
        for player_type, player_list in self.players.items():
            for player in player_list:
                club_count[player.club] += 1
                
        if any(n_players > 3 for n_players in club_count.values()): return False
        
        for element_type in range(1,5):
            if len(self.players[element_type]) != FplLoader.get_position_info(element_type)['squad_select']:
                return False
        
        return True
    
    def optimal_formation(self, epc: ExpectedPointsCalculator, gameweek: int, as_of_gameweek: int) -> Dict[int, List[Tuple[Player, float]]]:
        '''
        Return optimal formation of an fpl team for a particular gameweek
        :param epc: expected points calculator
        :param gameweek: gameweek for which you want to optimal formation calculated for
        :param as_of_gameweek: you have information up to and including this gameweek
        :return: mapping of position to a list of (player, expected points) tuples
        '''
        def pop_n_elements(lst, n):
            popped_elements = set()
            for _ in range(n):
                try:
                    popped_elements.add(lst.pop())
                except IndexError:  # The list is empty
                    break
            return popped_elements
        
        position_to_sorted_list = {}
        for position, player_set in self.players.items():
            player_list = [(player, epc.get_expected_points(player.element, gameweek, as_of_gameweek)) for player in player_set]
            position_to_sorted_list[position] = sorted(player_list, key=lambda x: x[1])
            
        result = {}
        remaining_list = []
        for pos in position_to_sorted_list:
            result[pos] = pop_n_elements(position_to_sorted_list[pos], FplLoader.get_position_info(pos)['squad_min_play'])
            remaining_list.extend(position_to_sorted_list[pos])
            
        remaining_list = sorted(remaining_list, key=lambda x: x[1])
        i = len(remaining_list)-1
        while sum(len(player_list) for player_list in result.values()) < 11:
            player, exp_points = remaining_list[i]
            if len(result[player.position]) < FplLoader.get_position_info(player.position)['squad_max_play']:
                result[player.position].add( (player, exp_points) )
            i -= 1
        
        return result
    
    def score(self, epc: ExpectedPointsCalculator, gameweek: int, as_of_gameweek: int, horizon: int) -> float:
        '''
        Return score you can expect from the team over a particular horizon
        '''
        transfer_adjustment = 0
        if self.free_transfers == 0: transfer_adjustment = -2
        if self.free_transfers < 0: transfer_adjustment = self.free_transfers * 4
        expected_points = 0
        for h in range(horizon):
            optimal_formation_for_h = self.optimal_formation(epc, gameweek + h, as_of_gameweek)
            expected_points_for_h = sum(sum(y[1] for y in x) for x in optimal_formation_for_h.values())
            captain_expected_points_for_h = max(max(y[1] for y in x) for x in optimal_formation_for_h.values())
            expected_points = expected_points + expected_points_for_h + captain_expected_points_for_h
            
        return expected_points + transfer_adjustment

    
def make_transfer(team: Team, out_player: Player, in_player: Player) -> Team:
    '''
    Makes a single transfer giving a new team
    :param team: team before the transfer
    :param out_player: player to be transfered out
    :param in_player: player to be transfered in
    :return: copy of team which contains updated squad, money in bank and free transfers
    '''
    assert out_player.position == in_player.position
    new_team = copy.deepcopy(team)
    new_team.players[out_player.position].remove(out_player)
    new_team.players[out_player.position].add(in_player)
    new_team.free_transfers -= 1
    new_team.money_in_bank += (out_player.cost - in_player.cost)
    return new_team

def optimize_team(team: Team, 
                  candidates: List[Player], 
                  max_transfers: int,
                  epc: ExpectedPointsCalculator, 
                  gameweek: int, 
                  as_of_gameweek: int, 
                  horizon: int
                 ) -> List[Team]:
    '''
    Find top three teams
    
    :param team: team you wish to optimize
    :param candidates: list of player candidates you wish to transfer in
    :param max_transfers: maximum number of transfers you wish to take on
    :return: list of top three teams based on score
    '''
    top_three = [(team.score(epc, gameweek, as_of_gameweek, horizon), team)]
    heapq.heapify(top_three)
    heap_set = set([team])
    
    currLayer = [team]
    for i in range(max_transfers):
        nextLayer = []
        for u_team in currLayer:
            for candidate in candidates:
                out_players = u_team.players[candidate.position]
                if candidate not in out_players:
                    for out_player in out_players:
                        v_team = make_transfer(u_team, out_player, candidate)
                        v_score = v_team.score(epc, gameweek, as_of_gameweek, horizon)
                        if v_team.is_feasible() and (v_team not in heap_set):
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