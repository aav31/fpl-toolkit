from abc import ABC, abstractmethod

class ExpectedPointsCalculator(ABC):
    '''
    Class to calculate the points that a particular player will get
    '''
    @abstractmethod
    def get_expected_points(self, player_id: int, gameweek: int, as_of_gameweek: int) -> float:
        '''
        Get expected points using all information up to and including as_of_gameweek
        '''
        ...