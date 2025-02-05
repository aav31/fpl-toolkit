"""
This module defines the Loader class, which provides methods to fetch data from the FPL API.
For more information on different API endpoints a useful article is:
https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19

Available functions:
- get_static_info: Return the static information from the FPL API.
- get_fixtures: Return a list of fixtures from the FPL API.
- get_fixture_info: Return the information for a particular fixture.
- get_fixtures_for_gameweek: Return the fixtures from FPL for a particular gameweek.
- get_team_basic_info: Return the information for a particular team given their team id.
- get_my_team: Get team information of current fpl team either from the api or locally.
- get_next_gameweek: Get the id of the next gameweek as an integer as of a particular UTC timestamp.
- get_my_historical_team_from_gameweek: Returns the historical team a manager used for a particular gameweek.
- get_player_basic_info: Get the basic information of a player so far this season and based on the most recent gameweek.
- get_player_detailed_info: Returns a player’s detailed information.
- get_player_historical_info_for_gameweek: Return a player's information for a particular gameweek where the information is known.
- get_player_future_info_for_gameweek: Return a player's information for a particular gameweek where the information is unknown.
- get_position_info: Get the information regarding a particular position.
- find_matching_players: Search for players whose web names partially match the search_name using fuzzy matching.
"""

import requests
from typing import List, Dict, Any, Tuple, Set
import pandas as pd
from functools import lru_cache
import warnings
import json
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fpl.team import Team
from fpl.player import Player


class Loader:
    """Static class to get data from the FPL API.
    Some methods maintain a cache of results to avoid querying the API multiple times.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_static_info() -> Dict[str, Any]:
        """Return the static information from the FPL API.
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
        """Return a list of fixtures from the FPL API.
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
            raise KeyError(
                "Gameweek {} is not between 1 and 38 inclusive".format(gameweek)
            )
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
    def get_my_team(
        login: str, password: str, manager_id: int, how: str = "api", filename: str = ""
    ) -> Team:
        """Get team information of current fpl team either from the api or locally.
        To get manager id you need to log in -> inspect -> network,
        you should see an api request e.g. myteam/3247546

        :param login: Username email address. Not used when 'how' is 'local'.
        :param password: Your password. Not used when 'how' is 'local'.
        :param manager_id: Manager id. Not used when 'how' is 'local'.
        :param how: 'local' or 'api' indicating download method.
        :param filename: Path to a local json blob.

        :return: Team object

        :raises ValueError: If arguments are specified incorrectly.
        :raises requests.exceptions.RequestException: If there is an error querying the API.
        """

        if how not in {"api", "local"}:
            raise ValueError(
                f"Invalid value for 'how': {how}. Must be 'api' or local'."
            )

        if how == "local" and not filename:
            raise ValueError("You must specify a filename when 'how' is 'local'.")

        if how == "api":
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
                d = json.loads(
                    res.content
                )  # Dictionary with three sections picks, chips, transfers
                res.raise_for_status()
            except requests.exceptions.RequestException:
                raise requests.exceptions.RequestException("Error querying API")
            finally:
                session.close()
        else:
            with open(filename) as fd:
                d = json.load(
                    fd
                )  # Dictionary with three sections picks, chips, transfers

        picks = d["picks"]
        gkps, defs, mids, fwds = set(), set(), set(), set()
        for pick in picks:
            player = Player(
                element=pick["element"],
                name=Loader.get_player_basic_info(pick["element"])["web_name"],
                position=Loader.get_player_basic_info(pick["element"])["element_type"],
                club=Loader.get_player_basic_info(pick["element"])["team"],
                cost=pick["selling_price"],
            )
            if player.position == 1:
                gkps.add(player)
            if player.position == 2:
                defs.add(player)
            if player.position == 3:
                mids.add(player)
            if player.position == 4:
                fwds.add(player)

        money_in_bank = d["transfers"]["bank"]
        free_transfers = (
            0 if d["transfers"]["limit"] is None else d["transfers"]["limit"]
        )
        team = Team(
            money_in_bank,
            free_transfers,
            frozenset(gkps),
            frozenset(defs),
            frozenset(mids),
            frozenset(fwds),
        )
        return team

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
        warnings.warn(
            "get_my_historical_team_from_gameweek is deprecated.", DeprecationWarning
        )

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

    @staticmethod
    def find_matching_players(
        search_name: str, threshold: int = 80
    ) -> List[Tuple[Player, str]]:
        """Search for players whose web names partially match the search_name using fuzzy matching.

        :param search_name: The name to search for.
        :param threshold: The minimum score for a match to be considered valid (default is 80).

        :return: A list of tuples, each containing a Player object and the full name as a string.

        :raises ValueError: If no matching players are found.
        """
        elements = Loader.get_static_info()["elements"]
        web_names = [p["web_name"] for p in elements]
        matches = process.extract(search_name, web_names, scorer=fuzz.partial_ratio)
        filtered_matches = [match for match in matches if match[1] >= threshold]
        matched_ids = [
            p["id"]
            for p in elements
            if p["web_name"] in [match[0] for match in filtered_matches]
        ]

        if not matched_ids:
            raise ValueError("No matching players found.")

        players = []
        for i in matched_ids:
            basic_info = Loader.get_player_basic_info(i)
            player = Player(
                element=i,
                name=basic_info["web_name"],
                position=basic_info["element_type"],
                club=basic_info["team"],
                cost=basic_info["now_cost"],
            )
            full_name = f"{basic_info['first_name']} {basic_info['second_name']}"
            players.append((player, full_name))

        return players
