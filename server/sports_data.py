# Copyright (c) Microsoft. All rights reserved.
# Mock sports data and tool functions for the Sports A2A server

"""
Sports data tools used by the A2A agents.
Returns mock data to simulate a real sports API (e.g. API-Football, Ergast, ESPN).
In production, replace these stubs with real HTTP calls to your data provider.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

_LIVE_SCORES = {
    "football": [
        {"home": "Real Madrid", "away": "Barcelona", "score": "2-1", "minute": 67, "competition": "La Liga"},
        {"home": "Manchester City", "away": "Arsenal", "score": "0-0", "minute": 45, "competition": "Premier League"},
        {"home": "Bayern Munich", "away": "Dortmund", "score": "3-1", "minute": 90, "competition": "Bundesliga"},
    ],
    "f1": [
        {"driver": "Max Verstappen", "team": "Red Bull", "position": 1, "gap": "LEADER", "race": "Monaco GP"},
        {"driver": "Lando Norris", "team": "McLaren", "position": 2, "gap": "+4.2s", "race": "Monaco GP"},
        {"driver": "Charles Leclerc", "team": "Ferrari", "position": 3, "gap": "+8.7s", "race": "Monaco GP"},
    ],
    "basketball": [
        {"home": "LA Lakers", "away": "Boston Celtics", "score": "108-101", "quarter": "Q4", "competition": "NBA"},
    ],
    "tennis": [
        {"player1": "Carlos Alcaraz", "player2": "Novak Djokovic", "score": "6-4, 3-6, 7-5", "round": "Final", "tournament": "Roland Garros"},
    ],
}

_FOOTBALL_STANDINGS = {
    "la_liga": [
        {"pos": 1, "team": "Real Madrid",    "played": 34, "won": 26, "drawn": 4, "lost": 4, "gf": 82, "ga": 31, "pts": 82},
        {"pos": 2, "team": "Barcelona",       "played": 34, "won": 23, "drawn": 5, "lost": 6, "gf": 75, "ga": 42, "pts": 74},
        {"pos": 3, "team": "Atletico Madrid", "played": 34, "won": 21, "drawn": 7, "lost": 6, "gf": 63, "ga": 38, "pts": 70},
        {"pos": 4, "team": "Athletic Bilbao", "played": 34, "won": 18, "drawn": 6, "lost": 10,"gf": 55, "ga": 40, "pts": 60},
        {"pos": 5, "team": "Villarreal",      "played": 34, "won": 16, "drawn": 8, "lost": 10,"gf": 52, "ga": 47, "pts": 56},
    ],
    "premier_league": [
        {"pos": 1, "team": "Arsenal",         "played": 35, "won": 25, "drawn": 7, "lost": 3, "gf": 83, "ga": 28, "pts": 82},
        {"pos": 2, "team": "Manchester City",  "played": 35, "won": 24, "drawn": 6, "lost": 5, "gf": 78, "ga": 39, "pts": 78},
        {"pos": 3, "team": "Liverpool",        "played": 35, "won": 22, "drawn": 8, "lost": 5, "gf": 76, "ga": 41, "pts": 74},
        {"pos": 4, "team": "Chelsea",          "played": 35, "won": 18, "drawn": 6, "lost": 11,"gf": 69, "ga": 54, "pts": 60},
        {"pos": 5, "team": "Tottenham",        "played": 35, "won": 15, "drawn": 9, "lost": 11,"gf": 61, "ga": 57, "pts": 54},
    ],
}

_F1_STANDINGS = {
    "drivers": [
        {"pos": 1, "driver": "Max Verstappen",  "team": "Red Bull Racing", "pts": 195},
        {"pos": 2, "driver": "Lando Norris",    "team": "McLaren",         "pts": 171},
        {"pos": 3, "driver": "Charles Leclerc", "team": "Ferrari",         "pts": 148},
        {"pos": 4, "driver": "Carlos Sainz",    "team": "Williams",        "pts": 127},
        {"pos": 5, "driver": "Oscar Piastri",   "team": "McLaren",         "pts": 119},
    ],
    "constructors": [
        {"pos": 1, "team": "McLaren",           "pts": 290},
        {"pos": 2, "team": "Red Bull Racing",   "pts": 260},
        {"pos": 3, "team": "Ferrari",           "pts": 248},
        {"pos": 4, "team": "Mercedes",          "pts": 183},
        {"pos": 5, "team": "Williams",          "pts": 145},
    ],
}

_PLAYER_STATS = {
    "vinicius jr": {
        "name": "Vinicius Jr.", "team": "Real Madrid", "position": "LW", "nationality": "Brazil",
        "season": "2024/25",
        "goals": 24, "assists": 14, "matches": 32, "minutes": 2710,
        "shots_on_target": 68, "dribbles_completed": 112, "key_passes": 57,
        "rating": 8.4,
    },
    "max verstappen": {
        "name": "Max Verstappen", "team": "Red Bull Racing", "nationality": "Netherlands",
        "season": "2025",
        "wins": 7, "podiums": 11, "poles": 5, "fastest_laps": 4,
        "points": 195, "dnfs": 1, "avg_finish": 2.1,
        "rating": 9.1,
    },
    "carlos alcaraz": {
        "name": "Carlos Alcaraz", "team": "Spain", "nationality": "Spain",
        "season": "2025",
        "titles": 3, "finals": 5, "matches_won": 42, "matches_lost": 7,
        "win_pct": 85.7, "aces": 312, "ranking": 2,
        "rating": 8.9,
    },
}

_TEAM_STATS = {
    "real madrid": {
        "name": "Real Madrid", "league": "La Liga", "season": "2024/25",
        "matches": 34, "wins": 26, "draws": 4, "losses": 4,
        "goals_scored": 82, "goals_conceded": 31, "goal_diff": 51,
        "clean_sheets": 14, "xg": 79.3, "xga": 33.8,
        "possession_avg": 58.2, "pass_accuracy": 89.1,
        "points": 82, "form": ["W", "W", "W", "D", "W"],
    },
    "mclaren": {
        "name": "McLaren", "series": "Formula 1", "season": "2025",
        "races": 9, "wins": 3, "podiums": 7, "poles": 2,
        "points": 290, "dnfs": 2, "avg_points_per_race": 32.2,
        "fastest_laps": 3, "form": ["1st", "2nd", "1st", "3rd", "2nd"],
    },
}

# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------


def get_live_scores(sport: str) -> dict:
    """
    Returns live scores and recent results for a given sport.

    Args:
        sport: One of 'football', 'f1', 'basketball', or 'tennis'.

    Returns:
        A dict with 'sport' and 'matches' keys containing current scores.
    """
    sport = sport.lower().strip()
    data = _LIVE_SCORES.get(sport, [])
    if not data:
        return {"sport": sport, "matches": [], "message": f"No live data found for '{sport}'."}
    return {"sport": sport, "matches": data}


def get_football_standings(league: str) -> dict:
    """
    Returns the current standings table for a football league.

    Args:
        league: League identifier. Supported values: 'la_liga', 'premier_league'.

    Returns:
        A dict with 'league' and 'table' keys containing the standings.
    """
    league_key = league.lower().replace(" ", "_").replace("-", "_")
    table = _FOOTBALL_STANDINGS.get(league_key)
    if not table:
        available = list(_FOOTBALL_STANDINGS.keys())
        return {
            "league": league,
            "table": [],
            "message": f"No standings found for '{league}'. Available: {available}",
        }
    return {"league": league_key, "table": table}


def get_f1_standings(category: str = "drivers") -> dict:
    """
    Returns the current Formula 1 championship standings.

    Args:
        category: 'drivers' for the driver championship, 'constructors' for the team championship.

    Returns:
        A dict with 'category' and 'standings' keys.
    """
    cat = category.lower().strip()
    standings = _F1_STANDINGS.get(cat)
    if not standings:
        return {
            "category": cat,
            "standings": [],
            "message": f"Invalid category '{cat}'. Use 'drivers' or 'constructors'.",
        }
    return {"category": cat, "standings": standings}


def get_player_stats(player_name: str) -> dict:
    """
    Returns detailed statistics for a specific player or driver.

    Args:
        player_name: Full or partial player name (e.g. 'Vinicius Jr', 'Verstappen').

    Returns:
        A dict containing the player's season statistics.
    """
    key = player_name.lower().strip()
    # Partial match support
    for stored_key, stats in _PLAYER_STATS.items():
        if key in stored_key or stored_key in key:
            return {"found": True, "player": stats}
    available = [s["name"] for s in _PLAYER_STATS.values()]
    return {
        "found": False,
        "message": f"No stats found for '{player_name}'.",
        "available_players": available,
    }


def get_team_stats(team_name: str) -> dict:
    """
    Returns performance metrics and statistics for a team.

    Args:
        team_name: Team name (e.g. 'Real Madrid', 'McLaren').

    Returns:
        A dict containing the team's season statistics.
    """
    key = team_name.lower().strip()
    for stored_key, stats in _TEAM_STATS.items():
        if key in stored_key or stored_key in key:
            return {"found": True, "team": stats}
    available = [s["name"] for s in _TEAM_STATS.values()]
    return {
        "found": False,
        "message": f"No stats found for '{team_name}'.",
        "available_teams": available,
    }
