"""
This module provides a collection of utility functions designed to support various tasks and operations across the project. These functions are general-purpose and do not fit into the specific scope of other modules. They enhance code reusability and maintainability by offering common functionalities that can be easily integrated into different parts of the application.

Functions included in this module cover a range of operations, such as data manipulation, computation, and other helper tasks that streamline and simplify the development process.

Available functions:
- find_matching_players: Search for players whose web names partially match the search_name using fuzzy matching.
- compute_points_per_game: Compute points per game a player would have had right before a particular as_of_gameweek occured.
- compute_form: Compute form a player would have had right before a particular as_of_gameweek occured.
"""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fpl import Loader, Player


def find_matching_players(
    search_name: str, threshold: int = 80
) -> list[tuple[Player, str]]:
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


def compute_points_per_game(player_id: int, as_of_gameweek: int) -> float:
    """Compute points per game a player would have had right before a particular as_of_gameweek occured.
    Points per game are conditional on the player having started that game.

    :param player_id: The unique identifier of the player.
    :param as_of_gameweek: The next gameweek following the gameweeks where the average is calculated over.

    :return: Average points per game.
    """
    historical_fixtures = [
        info
        for i in range(1, as_of_gameweek)
        for info in Loader.get_player_historical_info_for_gameweek(player_id, i)
    ]
    points_array = [
        fixture["total_points"]
        for fixture in historical_fixtures
        if fixture["minutes"] > 0
    ]
    return round(sum(points_array) / len(points_array), 1) if len(points_array) else 0.0


def _kickoff_time_30_days_before_gameweek(
    kickoff_time: str, as_of_gameweek: int
) -> bool:
    """Get whether the kick off time of a particular game was 30 days before the start of the gameweek.
    Useful for computing the form of a player.

    :param kickoff_time: Kick off time of a particular game.
    :param as_of_gameweek: The gameweek which you want to find whether the game occured 30 days before.

    :return: Bool indicating whether that game occured 30 days before the gameweek.
    """
    as_of_timestring = [
        x["deadline_time"]
        for x in Loader.get_static_info()["events"]
        if x["id"] == as_of_gameweek
    ][0]
    as_of_timestamp = (
        pd.Timestamp.now(tz="UTC")
        if as_of_gameweek == Loader.get_next_gameweek()
        else pd.Timestamp(as_of_timestring)
    )
    thirty_days_ago = as_of_timestamp - pd.Timedelta(days=30)
    kickoff_time_timestamp = pd.Timestamp(kickoff_time, tz="UTC")
    return thirty_days_ago <= kickoff_time_timestamp


def compute_form(player_id: int, as_of_gameweek: int) -> float:
    """Compute form a player would have had right before a particular as_of_gameweek occured.
    Points per game are here are **not** conditional on the player having started that game.
    There is no minutes > 0 condition.

    :param player_id: The unique identifier of the player.
    :param as_of_gameweek: The next gameweek following the gameweeks where the average is calculated over.

    :return: Average points per game.
    """
    historical_fixtures = [
        info
        for i in range(1, as_of_gameweek)
        for info in Loader.get_player_historical_info_for_gameweek(player_id, i)
    ]
    points_array = [
        fixture["total_points"]
        for fixture in historical_fixtures
        if _kickoff_time_30_days_before_gameweek(
            fixture["kickoff_time"], as_of_gameweek
        )
    ]
    return round(sum(points_array) / len(points_array), 1) if len(points_array) else 0.0
