# Orquestador A2A de deportes — host agent que usa múltiples agentes A2A como herramientas

import asyncio
import os
import re

import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

"""
Orquestador A2A de deportes — convierte múltiples agentes A2A en herramientas de un host agent.

Este es el patrón de cliente avanzado: un agente local respaldado por Foundry recibe las
preguntas deportivas del usuario y decide qué agente remoto A2A (results / stats) invocar,
componiendo automáticamente la respuesta final.

Requisitos previos:
  Terminal 1: python server/a2a_server.py --agent-type results --port 5001
  Terminal 2: python server/a2a_server.py --agent-type stats   --port 5002

Variables de entorno (en .env):
  FOUNDRY_PROJECT_ENDPOINT  — Endpoint del proyecto Azure AI Foundry
  FOUNDRY_MODEL             — Nombre del modelo desplegado (p.ej. gpt-4o-mini)
  A2A_RESULTS_HOST          — URL del agente de resultados (por defecto: http://localhost:5001/)
  A2A_STATS_HOST            — URL del agente de estadísticas (por defecto: http://localhost:5002/)

Uso:
  python client/a2a_orchestrator.py
"""

INSTRUCCIONES_ORQUESTADOR = """\
Eres un asistente de información deportiva. Tienes acceso a dos agentes especializados:
- Agente de resultados: para marcadores en vivo, resultados de partidos y clasificaciones de ligas.
- Agente de estadísticas: para estadísticas detalladas de jugadores y equipos.

Dirige las consultas del usuario al agente apropiado. Para preguntas complejas, llama a ambos.
Proporciona siempre respuestas claras y bien formateadas con los datos más relevantes.
Responde siempre en español.
"""

# Consultas de demo que requieren agentes distintos
CONSULTAS_DEMO = [
    "¿Quién lidera La Liga y cuáles son las estadísticas de Vinicius Jr esta temporada?",
    "Dame la clasificación de F1 y las estadísticas de Max Verstappen.",
]


async def resolver_agente(http_client: httpx.AsyncClient, host_url: str, etiqueta: str):
    """Resuelve el agent card de un agente A2A y devuelve el AgentCard."""
    resolver = A2ACardResolver(httpx_client=http_client, base_url=host_url)
    card = await resolver.get_agent_card()
    print(f"  Resuelto {etiqueta}: {card.name} ({len(card.skills)} skill(s))")
    return card


async def main() -> None:
    """Ejecuta el host agent orquestador contra múltiples agentes A2A de deportes."""
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")
    results_host = os.getenv("A2A_RESULTS_HOST", "http://localhost:5001/")
    stats_host = os.getenv("A2A_STATS_HOST", "http://localhost:5002/")

    if not project_endpoint or not model:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT y FOUNDRY_MODEL deben estar configurados en .env")

    print("Resolviendo agentes A2A remotos...")
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        results_card = await resolver_agente(http_client, results_host, "Agente de resultados")
        stats_card = await resolver_agente(http_client, stats_host, "Agente de estadísticas")
    print()

    # Crear el host agent de Foundry con las skills A2A como herramientas
    credential = AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=credential,
    )

    async with (
        A2AAgent(
            name=results_card.name,
            description=results_card.description,
            agent_card=results_card,
            url=results_host,
        ) as results_agent,
        A2AAgent(
            name=stats_card.name,
            description=stats_card.description,
            agent_card=stats_card,
            url=stats_host,
        ) as stats_agent,
    ):
        # Convertir cada skill en una function tool
        def crear_tools(a2a_agent, card):
            return [
                a2a_agent.as_tool(
                    name=re.sub(r"[^0-9A-Za-z]+", "_", skill.name),
                    description=skill.description or "",
                )
                for skill in card.skills
            ]

        todas_las_tools = crear_tools(results_agent, results_card) + crear_tools(stats_agent, stats_card)

        host_agent = client.as_agent(
            name="OrquestadorDeportivo",
            instructions=INSTRUCCIONES_ORQUESTADOR,
            tools=todas_las_tools,
        )

        print(f"Host agent listo con {len(todas_las_tools)} herramientas:")
        for tool in todas_las_tools:
            print(f"  - {tool.name}")
        print()

        # Ejecutar las consultas de demo
        for consulta in CONSULTAS_DEMO:
            print("=" * 60)
            print(f"Usuario : {consulta}")
            respuesta = await host_agent.run(consulta)
            print(f"Agente  : {respuesta}\n")


if __name__ == "__main__":
    asyncio.run(main())
