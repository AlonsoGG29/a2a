# Copyright (c) Microsoft. All rights reserved.
# Agent definitions and AgentCard factories for the Sports A2A server

from __future__ import annotations

from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from sports_data import (
    get_f1_standings,
    get_football_standings,
    get_live_scores,
    get_player_stats,
    get_team_stats,
)

# ---------------------------------------------------------------------------
# Agent instructions
# ---------------------------------------------------------------------------

RESULTS_INSTRUCTIONS = """\
You are a sports results expert specializing in recent match results and standings.
You cover football (soccer), Formula 1, basketball, and tennis.

Use your tools to look up:
- Live scores and recent match results
- League standings and championship tables
- Formula 1 driver and constructor standings

Always present results clearly with scores, dates, and relevant context.
If asked about a sport or league you don't have data for, say so honestly.
"""

STATS_INSTRUCTIONS = """\
You are a sports statistics analyst with deep knowledge of player and team performance.
You cover football (soccer), Formula 1, basketball, and tennis.

Use your tools to provide:
- Detailed player statistics (goals, assists, rating, etc.)
- Team performance metrics (wins, losses, goals scored/conceded, etc.)
- Historical comparisons and trend analysis

Present statistics in a clear, structured format. Add context to help the user
understand what the numbers mean (e.g. how a stat compares to league average).
"""

# ---------------------------------------------------------------------------
# Agent factories
# ---------------------------------------------------------------------------


def create_results_agent(client: FoundryChatClient) -> Agent:
    """Creates the results agent with live score and standings tools."""
    return Agent(
        client=client,
        name="SportsResultsAgent",
        instructions=RESULTS_INSTRUCTIONS,
        tools=[get_live_scores, get_football_standings, get_f1_standings],
    )


def create_stats_agent(client: FoundryChatClient) -> Agent:
    """Creates the stats agent with player and team stat tools."""
    return Agent(
        client=client,
        name="SportsStatsAgent",
        instructions=STATS_INSTRUCTIONS,
        tools=[get_player_stats, get_team_stats],
    )


# ---------------------------------------------------------------------------
# AgentCard factories
# ---------------------------------------------------------------------------

_CAPABILITIES = AgentCapabilities(streaming=True, push_notifications=False)


def get_results_agent_card(url: str) -> AgentCard:
    """Returns the A2A AgentCard for the results agent."""
    return AgentCard(
        name="SportsResultsAgent",
        description="Provides live scores, recent results, and standings for football, F1, basketball, and tennis.",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=_CAPABILITIES,
        supported_interfaces=[AgentInterface(url=url, protocol_binding="JSONRPC")],
        skills=[
            AgentSkill(
                id="live_scores",
                name="LiveScores",
                description="Returns live scores and recent results for a sport or competition.",
                tags=["sports", "scores", "results", "live"],
                examples=["What are today's football scores?", "Show me F1 race results"],
            ),
            AgentSkill(
                id="standings",
                name="Standings",
                description="Returns current league or championship standings.",
                tags=["sports", "standings", "table", "ranking"],
                examples=["Show me the Premier League table", "F1 driver standings 2025"],
            ),
        ],
    )


def get_stats_agent_card(url: str) -> AgentCard:
    """Returns the A2A AgentCard for the stats agent."""
    return AgentCard(
        name="SportsStatsAgent",
        description="Provides detailed player and team statistics for major sports.",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=_CAPABILITIES,
        supported_interfaces=[AgentInterface(url=url, protocol_binding="JSONRPC")],
        skills=[
            AgentSkill(
                id="player_stats",
                name="PlayerStats",
                description="Returns detailed statistics for a specific player.",
                tags=["sports", "stats", "player", "performance"],
                examples=["Stats for Vinicius Jr this season", "Verstappen's 2025 stats"],
            ),
            AgentSkill(
                id="team_stats",
                name="TeamStats",
                description="Returns performance metrics and statistics for a team.",
                tags=["sports", "stats", "team", "metrics"],
                examples=["Real Madrid stats this season", "Barcelona attack statistics"],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

AGENT_FACTORIES = {
    "results": create_results_agent,
    "stats": create_stats_agent,
}

AGENT_CARD_FACTORIES = {
    "results": get_results_agent_card,
    "stats": get_stats_agent_card,
}
