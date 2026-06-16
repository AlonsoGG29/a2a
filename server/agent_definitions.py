# Definiciones de agentes y AgentCards para el servidor A2A de deportes

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
# Instrucciones de los agentes
# ---------------------------------------------------------------------------

RESULTS_INSTRUCTIONS = """\
Eres un experto en resultados deportivos especializado en resultados recientes y clasificaciones.
Cubres fútbol, Fórmula 1, baloncesto y tenis.

Usa tus herramientas para consultar:
- Marcadores en vivo y resultados recientes de partidos
- Clasificaciones de ligas y campeonatos
- Clasificación de pilotos y constructores de Fórmula 1

Presenta siempre los resultados de forma clara con marcadores, fechas y contexto relevante.
Si te preguntan por un deporte o liga para el que no tienes datos, indícalo con honestidad.
Responde siempre en español.
"""

STATS_INSTRUCTIONS = """\
Eres un analista de estadísticas deportivas con amplio conocimiento del rendimiento de jugadores y equipos.
Cubres fútbol, Fórmula 1, baloncesto y tenis.

Usa tus herramientas para proporcionar:
- Estadísticas detalladas de jugadores (goles, asistencias, valoración, etc.)
- Métricas de rendimiento de equipos (victorias, derrotas, goles a favor/en contra, etc.)
- Comparaciones históricas y análisis de tendencias

Presenta las estadísticas en un formato claro y estructurado. Añade contexto para ayudar
al usuario a entender qué significan los números (p.ej. cómo se compara una estadística
con la media de la liga).
Responde siempre en español.
"""

# ---------------------------------------------------------------------------
# Factorías de agentes
# ---------------------------------------------------------------------------


def create_results_agent(client: FoundryChatClient) -> Agent:
    """Crea el agente de resultados con herramientas de marcadores y clasificaciones."""
    return Agent(
        client=client,
        name="AgenteResultadosDeportivos",
        instructions=RESULTS_INSTRUCTIONS,
        tools=[get_live_scores, get_football_standings, get_f1_standings],
    )


def create_stats_agent(client: FoundryChatClient) -> Agent:
    """Crea el agente de estadísticas con herramientas de jugadores y equipos."""
    return Agent(
        client=client,
        name="AgenteEstadisticasDeportivas",
        instructions=STATS_INSTRUCTIONS,
        tools=[get_player_stats, get_team_stats],
    )


# ---------------------------------------------------------------------------
# Factorías de AgentCard
# ---------------------------------------------------------------------------

_CAPABILITIES = AgentCapabilities(streaming=True, push_notifications=False)


def get_results_agent_card(url: str) -> AgentCard:
    """Devuelve el AgentCard A2A para el agente de resultados."""
    return AgentCard(
        name="AgenteResultadosDeportivos",
        description="Proporciona marcadores en vivo, resultados recientes y clasificaciones de fútbol, F1, baloncesto y tenis.",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=_CAPABILITIES,
        supported_interfaces=[AgentInterface(url=url, protocol_binding="JSONRPC")],
        skills=[
            AgentSkill(
                id="marcadores_en_vivo",
                name="MarcadoresEnVivo",
                description="Devuelve marcadores en vivo y resultados recientes de un deporte o competición.",
                tags=["deportes", "marcadores", "resultados", "directo"],
                examples=["¿Cuáles son los marcadores de fútbol hoy?", "Resultados de la carrera de F1"],
            ),
            AgentSkill(
                id="clasificaciones",
                name="Clasificaciones",
                description="Devuelve la clasificación actual de una liga o campeonato.",
                tags=["deportes", "clasificación", "tabla", "ranking"],
                examples=["Muéstrame la tabla de La Liga", "Clasificación de pilotos de F1"],
            ),
        ],
    )


def get_stats_agent_card(url: str) -> AgentCard:
    """Devuelve el AgentCard A2A para el agente de estadísticas."""
    return AgentCard(
        name="AgenteEstadisticasDeportivas",
        description="Proporciona estadísticas detalladas de jugadores y equipos para los principales deportes.",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=_CAPABILITIES,
        supported_interfaces=[AgentInterface(url=url, protocol_binding="JSONRPC")],
        skills=[
            AgentSkill(
                id="estadisticas_jugador",
                name="EstadisticasJugador",
                description="Devuelve estadísticas detalladas de un jugador concreto.",
                tags=["deportes", "estadísticas", "jugador", "rendimiento"],
                examples=["Estadísticas de Vinicius Jr esta temporada", "Stats de Verstappen en 2025"],
            ),
            AgentSkill(
                id="estadisticas_equipo",
                name="EstadisticasEquipo",
                description="Devuelve métricas de rendimiento y estadísticas de un equipo.",
                tags=["deportes", "estadísticas", "equipo", "métricas"],
                examples=["Estadísticas del Real Madrid esta temporada", "Estadísticas de ataque del Barcelona"],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Diccionarios de búsqueda
# ---------------------------------------------------------------------------

AGENT_FACTORIES = {
    "results": create_results_agent,
    "stats": create_stats_agent,
}

AGENT_CARD_FACTORIES = {
    "results": get_results_agent_card,
    "stats": get_stats_agent_card,
}
