# Datos deportivos mock y funciones de herramientas para el servidor A2A de deportes

"""
Herramientas de datos deportivos usadas por los agentes A2A.
Devuelve datos simulados para imitar una API deportiva real (p.ej. API-Football, Ergast, ESPN).
En producción, sustituye estas funciones por llamadas HTTP reales a tu proveedor de datos.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Datos mock
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
# Funciones de herramientas (tools)
# ---------------------------------------------------------------------------


def get_live_scores(sport: str) -> dict:
    """
    Devuelve marcadores en vivo y resultados recientes para un deporte dado.

    Args:
        sport: Uno de 'football', 'f1', 'basketball' o 'tennis'.

    Returns:
        Diccionario con las claves 'sport' y 'matches' con los marcadores actuales.
    """
    sport = sport.lower().strip()
    data = _LIVE_SCORES.get(sport, [])
    if not data:
        return {"sport": sport, "matches": [], "message": f"No se encontraron datos en vivo para '{sport}'."}
    return {"sport": sport, "matches": data}


def get_football_standings(league: str) -> dict:
    """
    Devuelve la clasificación actual de una liga de fútbol.

    Args:
        league: Identificador de la liga. Valores soportados: 'la_liga', 'premier_league'.

    Returns:
        Diccionario con las claves 'league' y 'table' con la clasificación.
    """
    league_key = league.lower().replace(" ", "_").replace("-", "_")
    table = _FOOTBALL_STANDINGS.get(league_key)
    if not table:
        available = list(_FOOTBALL_STANDINGS.keys())
        return {
            "league": league,
            "table": [],
            "message": f"No se encontró clasificación para '{league}'. Disponibles: {available}",
        }
    return {"league": league_key, "table": table}


def get_f1_standings(category: str = "drivers") -> dict:
    """
    Devuelve la clasificación actual del Campeonato del Mundo de Fórmula 1.

    Args:
        category: 'drivers' para el campeonato de pilotos, 'constructors' para el de constructores.

    Returns:
        Diccionario con las claves 'category' y 'standings'.
    """
    cat = category.lower().strip()
    standings = _F1_STANDINGS.get(cat)
    if not standings:
        return {
            "category": cat,
            "standings": [],
            "message": f"Categoría '{cat}' no válida. Usa 'drivers' o 'constructors'.",
        }
    return {"category": cat, "standings": standings}


def get_player_stats(player_name: str) -> dict:
    """
    Devuelve estadísticas detalladas de un jugador o piloto concreto.

    Args:
        player_name: Nombre completo o parcial del jugador (p.ej. 'Vinicius Jr', 'Verstappen').

    Returns:
        Diccionario con las estadísticas de temporada del jugador.
    """
    key = player_name.lower().strip()
    for stored_key, stats in _PLAYER_STATS.items():
        if key in stored_key or stored_key in key:
            return {"found": True, "player": stats}
    available = [s["name"] for s in _PLAYER_STATS.values()]
    return {
        "found": False,
        "message": f"No se encontraron estadísticas para '{player_name}'.",
        "jugadores_disponibles": available,
    }


def get_team_stats(team_name: str) -> dict:
    """
    Devuelve métricas de rendimiento y estadísticas de un equipo.

    Args:
        team_name: Nombre del equipo (p.ej. 'Real Madrid', 'McLaren').

    Returns:
        Diccionario con las estadísticas de temporada del equipo.
    """
    key = team_name.lower().strip()
    for stored_key, stats in _TEAM_STATS.items():
        if key in stored_key or stored_key in key:
            return {"found": True, "team": stats}
    available = [s["name"] for s in _TEAM_STATS.values()]
    return {
        "found": False,
        "message": f"No se encontraron estadísticas para '{team_name}'.",
        "equipos_disponibles": available,
    }
