# Cliente A2A de deportes — conecta con el servidor de deportes mediante el protocolo A2A

import asyncio
import os

import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv

load_dotenv()

"""
Cliente A2A de deportes — se comunica con el AgenteResultadosDeportivos o
AgenteEstadisticasDeportivas mediante el protocolo A2A.

Demuestra los modos sin streaming y con streaming. El agente se ejecuta en el servidor;
este cliente solo necesita la URL del endpoint A2A para descubrir capacidades y enviar consultas.

Requisitos previos:
  Arrancar primero el servidor:
    python server/a2a_server.py --agent-type results --port 5001

Variables de entorno (en .env):
  A2A_AGENT_HOST  — URL del servidor A2A en ejecución (por defecto: http://localhost:5001/)

Uso:
  python client/a2a_client.py
"""

# Consultas de demostración
CONSULTAS_DEMO = [
    "¿Cuáles son los marcadores de fútbol en vivo ahora mismo?",
    "Muéstrame la clasificación de La Liga",
    "¿Cuál es la clasificación de pilotos de F1?",
]


async def main() -> None:
    """Conecta con el agente A2A de deportes y ejecuta un conjunto de consultas de demo."""
    a2a_agent_host = os.getenv("A2A_AGENT_HOST", "http://localhost:5001/")
    print(f"Conectando con el agente A2A de deportes en: {a2a_agent_host}\n")

    # 1. Resolver el agent card — descubre qué puede hacer el agente
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        resolver = A2ACardResolver(httpx_client=http_client, base_url=a2a_agent_host)
        agent_card = await resolver.get_agent_card()

    print(f"Agente encontrado : {agent_card.name}")
    print(f"Descripción       : {agent_card.description}")
    print(f"Skills ({len(agent_card.skills)})        :", ", ".join(s.name for s in agent_card.skills))
    print()

    # 2. Crear el wrapper A2A y ejecutar las consultas
    async with A2AAgent(
        name=agent_card.name,
        description=agent_card.description,
        agent_card=agent_card,
        url=a2a_agent_host,
    ) as agent:

        # --- Sin streaming: pregunta/respuesta simple ---
        print("=" * 60)
        print("CONSULTA SIN STREAMING")
        print("=" * 60)
        consulta = CONSULTAS_DEMO[0]
        print(f"Usuario : {consulta}")
        respuesta = await agent.run(consulta)
        print(f"Agente  : {respuesta.text}\n")

        # --- Con streaming: recibe la respuesta de forma incremental ---
        print("=" * 60)
        print("CONSULTA CON STREAMING")
        print("=" * 60)
        consulta = CONSULTAS_DEMO[1]
        print(f"Usuario : {consulta}")
        print("Agente  : ", end="", flush=True)

        stream = agent.run(consulta, stream=True)
        async for update in stream:
            for content in update.contents:
                if content.text:
                    print(content.text, end="", flush=True)
        print()  # salto de línea al terminar el streaming

        final = await stream.get_final_response()
        print(f"\n[Respuesta final recibida — {len(final.text)} caracteres]\n")

        # --- Consulta adicional ---
        print("=" * 60)
        print("CONSULTA ADICIONAL")
        print("=" * 60)
        consulta = CONSULTAS_DEMO[2]
        print(f"Usuario : {consulta}")
        respuesta = await agent.run(consulta)
        print(f"Agente  : {respuesta.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
