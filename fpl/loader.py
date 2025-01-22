"""
loader.py
~~~~~~~~~

This module contains the `Loader` class which provides methods to fetch data from the Fantasy Premier League (FPL) API.

For more information on different API endpoints a useful article is:
    https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19


Classes:
    Loader: A static class to get data from the FPL API with caching.

Usage example:
    from loader import Loader
    static_info = Loader.get_static_info()
"""

import requests
from typing import List, Dict, Any, Tuple, Set
import pandas as pd
from functools import lru_cache
import warnings
import json
import time


class Loader:
    """Static class to get data from the FPL API.
    
    Some methods maintain a cache of results to avoid querying the API multiple times.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_static_info() -> Dict[str, Any]:
        """Return the static information from FPL.
        The result is cached to avoid multiple API calls.
        
        :return: A dictionary containing the static information from the FPL API.
        
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """
        time.sleep(1)
        try:
            response = requests.get(
                "https://fantasy.premierleague.com/api/bootstrap-static/"
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")

        result = response.json()
        assert len(result) > 0
        return result

    @staticmethod
    @lru_cache(maxsize=1)
    def get_fixtures() -> List[Dict]:
        """Return a list of fixtures from FPL.
        The result is cached to avoid multiple API calls.
        Each fixture is identified by the key "id".
        
        :return: List of fixtures
        
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """
        time.sleep(1)
        try:
            response = requests.get("https://fantasy.premierleague.com/api/fixtures/")
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")

        result = response.json()
        assert len(result) > 0
        return result

    @staticmethod
    @lru_cache(maxsize=380)
    def get_fixture_info(fixture_id: int) -> Dict:
        """Return the information for a particular fixture.
        Finds the info for a particular fixture by performing a linear search.
        The result is cached to avoid performing a linear search multiple times.
        There are at most 380 games so the cache cannot get too big.
        
        :param fixture_id: Identifier of a particular fixture.
        
        :return: Dictionary containing fixture info.
        
        :raises KeyError: If the fixture_id is not found or is ambiguous.
        """
        fixture_infos = []
        for fixture_info in Loader.get_fixtures():
            if fixture_info["id"] == fixture_id:
                fixture_infos.append(fixture_info)

        fixture_infos.sort()
        if len(fixture_infos) == 0:
            raise KeyError("Fixture id {} not found in map".format(fixture_id))
        if len(fixture_infos) > 1:
            raise KeyError(
                "Ambiguous fixture_id {} leading to multiple fixtures".format(
                    fixture_id
                )
            )

        return fixture_infos[0]

    @staticmethod
    @lru_cache(maxsize=38)
    def get_fixtures_for_gameweek(gameweek: int) -> List[Dict]:
        """Return the fixtures from FPL for a particular gameweek.
        The result is cached to avoid multiple API calls.
        
        :param gameweek: Gameweek from 1 to 38.
        
        :return: List of fixtures for a particular gameweek.
        
        :raises KeyError: If the gameweek is not between 1 and 38 inclusive.
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """
        if not (1 <= gameweek <= 38):
            raise KeyError("Gameweek {} is not between 1 and 38 inclusive".format(gameweek))
        try:
            response = requests.get(
                "https://fantasy.premierleague.com/api/fixtures/?event={}".format(
                    gameweek
                )
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")

        result = response.json()
        assert len(result) > 0
        return result

    @staticmethod
    @lru_cache(maxsize=20)
    def get_team_basic_info(team_id: int) -> Dict:
        """Return the information for a particular team given their team id.
        The result is cached to avoid performing a linear search multiple times.
        
        :param team_id: Team identifier.
        
        :return: Dictionary giving information of a particular team.
        
        :raises KeyError: If the team_id is not found.
        """
        for team_info in Loader.get_static_info()["teams"]:
            if team_info["id"] == team_id:
                return team_info
        raise KeyError("Team id {} not found in map".format(team_id))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_my_team_from_api(
        login: str, password: str, manager_id: int
    ) -> Dict[str, Any]:
        """Get team information of current fpl team
        To get manager id you need to log in -> inspect -> network,
        you should see an api request e.g. myteam/3247546
        
        :param login: Username email address.
        :param password: Your password.
        :param manager_id: Manager id.
        
        :return: Dictionary with three sections picks, chips, transfers.
        
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """

        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1; PRO 5 Build/LMY47D)",
            "accept-language": "en",
        }
        data = {
            "login": login,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login",
        }
        url = "https://users.premierleague.com/accounts/login/"
        team_url = "https://fantasy.premierleague.com/api/my-team/{}/".format(
            manager_id
        )

        try:
            session = requests.session()
            res = session.post(url, data=data, headers=headers)
            res = session.get(team_url)
            team = json.loads(res.content)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")
        finally:
            session.close()

        return team

    @staticmethod
    def get_my_team_from_local(local_filename: str) -> Dict[str, Any]:
        """Gets your team information from a local json file.
        Local json file of team can be downloaded from the fpl website.
        
        :param local_filename: Path to a .json file.
        
        :return: Dictionary with three sections picks, chips, transfers.
        """
        with open(local_filename) as fd:
            d = json.load(fd)
        return d

    @staticmethod
    def get_next_gameweek(as_of_ts: str = "now") -> int:
        """Get the id of the next gameweek as an integer as of a particular UTC timestamp.

        :param as_of_ts: provide input as in https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html
        
        :return: Id of the next gameweek.
        """
        if as_of_ts == "now":
            as_of_ts = pd.Timestamp.now("UTC")
        else:
            as_of_ts = pd.Timestamp(as_of_ts, tz="UTC")

        df = pd.DataFrame(Loader.get_static_info()["events"])
        df["deadline_time"] = pd.to_datetime(df["deadline_time"])
        df = df[df["deadline_time"] > as_of_ts]
        return int(df.nsmallest(1, "deadline_time").iloc[0]["id"])

    @staticmethod
    @lru_cache(maxsize=None)
    def get_my_historical_team_from_gameweek(
        gameweek: int, manager_id: int
    ) -> Dict[str, Any]:
        """Returns the historical team a manager used for a particular gameweek.
        To get manager id you need to log in -> inspect -> network,
        you should see an api request e.g. myteam/3247546
        
        :param gameweek: Historical gameweek number.
        :param manager_id: Manager id.
        
        :return: Dictionary where one of the elements is picks - these are the players you chose that gameweek.
        
        :raises TypeError: If the gameweek is not an integer.
        :raises ValueError: If the gameweek is not in the valid range.
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """
        warnings.warn("get_my_historical_team_from_gameweek is deprecated.", DeprecationWarning)
        
        if not isinstance(gameweek, int):
            raise TypeError("Gameweek should be an integer")
        if not (0 < gameweek < Loader.get_next_gameweek()):
            raise ValueError("Gameweek integer needs to be in valid range")

        url = "https://fantasy.premierleague.com/api/entry/{0}/event/{1}/picks/".format(
            manager_id, gameweek
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")

        return response.json()

    @staticmethod
    @lru_cache(maxsize=100)
    def get_player_basic_info(player_id: int) -> Dict[str, Any]:
        """Get the basic information of a player so far this season and based on the most recent gameweek.
        The result is cached to avoid performing a linear search multiple times.
        
        :param player_id: Player identifier.
        
        :return: Dictionary containing player information.
        
        :raises KeyError: If player_id is not found.
        """
        for player_info in Loader.get_static_info()["elements"]:
            if player_info["id"] == player_id:
                return player_info

        raise KeyError("Player id {} not found in map".format(player_id))

    @staticmethod
    @lru_cache(maxsize=100)
    def get_player_detailed_info(player_id: int) -> Dict[str, List[Dict]]:
        """Returns a player’s detailed information.
        Information is divided into 3 sections - fixtures, history, history_past.
        fixtures - A list of player’s remaining fixtures of the season.
        history - A list of player’s previous fixtures and its match stats.
        history_past - A list of player’s previous seasons and its seasonal stats.
        
        :param player_id: player id
        
        :return: Dictionary containing player detailed information.
        
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """
        try:
            response = requests.get(
                "https://fantasy.premierleague.com/api/element-summary/{}/".format(
                    player_id
                )
            )
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Error querying API")

        return response.json()

    @staticmethod
    def get_player_historical_info_for_gameweek(
        player_id: int, gameweek: int
    ) -> List[Dict]:
        """Return a player's information for a particular gameweek where the information is known.
        The list may be more than one if double gameweek and zero if blank.
        
        :param player_id: Player id.
        :param gameweek: Gameweek between 1 and 38 inclusive.
        
        :return: List of fixtures containing the player's stats.
        """
        player_history = Loader.get_player_detailed_info(player_id)["history"]
        result = []
        for player_info in player_history:
            if player_info["round"] == gameweek:
                result.append(player_info)

        return result

    @staticmethod
    def get_player_future_info_for_gameweek(
        player_id: int, gameweek: int
    ) -> List[Dict]:
        """Return a player's information for a particular gameweek where the information is unknown.
        The list may be more than one if double gameweek and zero if blank.
        
        :param player_id: Player id.
        :param gameweek: Gameweek between 1 and 38 inclusive.
        
        :return: List of fixtures containing the player's stats.
        """
        player_history = Loader.get_player_detailed_info(player_id)["fixtures"]
        result = []
        for player_info in player_history:
            if player_info["event"] == gameweek:
                result.append(player_info)

        return result

    @staticmethod
    def get_position_info(position_id: int) -> Dict[str, Any]:
        """Get the information regarding a particular position.
        For example minimum numbers that need to play in defence, midfield and attack.
        
        :param position_id: Position identifier 1 = gkp, 2 = def, 3 = mid, 4 = fwd.
        
        :return: Dictionary with information about a particular position.
        
        :raises KeyError: If position_id is not found.
        """
        for position in Loader.get_static_info()["element_types"]:
            if position["id"] == position_id:
                return position

        raise KeyError("Position id {} not found in map".format(position_id))
