# Servidor A2A de deportes — expone agentes deportivos como endpoints A2A

import argparse
import os
import sys

import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from agent_definitions import AGENT_CARD_FACTORIES, AGENT_FACTORIES
from agent_framework.a2a import A2AExecutor
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from starlette.applications import Starlette

load_dotenv()

"""
Servidor A2A de deportes — expone agentes deportivos como endpoints A2A usando Azure AI Foundry.

Tipos de agente disponibles:
  - results   — Responde preguntas sobre resultados y clasificaciones.
  - stats     — Proporciona estadísticas detalladas de jugadores y equipos.

Uso:
  python a2a_server.py --agent-type results --port 5001
  python a2a_server.py --agent-type stats   --port 5002

Variables de entorno (en .env):
  FOUNDRY_PROJECT_ENDPOINT  — Endpoint del proyecto Azure AI Foundry
  FOUNDRY_MODEL             — Nombre del modelo desplegado (p.ej. gpt-4o-mini)
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor A2A de deportes")
    parser.add_argument(
        "--agent-type",
        choices=list(AGENT_FACTORIES.keys()),
        default="results",
        help="Tipo de agente deportivo a exponer (por defecto: results)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host donde escucha el servidor (por defecto: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5001,
        help="Puerto donde escucha el servidor (por defecto: 5001)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Validar variables de entorno obligatorias
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")

    if not project_endpoint:
        print("Error: la variable de entorno FOUNDRY_PROJECT_ENDPOINT no está configurada.")
        sys.exit(1)
    if not model:
        print("Error: la variable de entorno FOUNDRY_MODEL no está configurada.")
        sys.exit(1)

    # Crear el cliente Foundry con credenciales de Azure CLI
    credential = AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=credential,
    )

    # Instanciar el agente deportivo solicitado
    agent_factory = AGENT_FACTORIES[args.agent_type]
    agent = agent_factory(client)

    # Construir los componentes del servidor A2A
    url = f"http://{args.host}:{args.port}/"
    agent_card = AGENT_CARD_FACTORIES[args.agent_type](url)
    executor = A2AExecutor(agent, stream=True)
    task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=agent_card,
    )

    app = Starlette(
        routes=[
            *create_agent_card_routes(agent_card),
            *create_jsonrpc_routes(request_handler, "/"),
        ]
    )

    print(f"Iniciando servidor A2A de deportes: {agent_card.name}")
    print(f"  Tipo de agente : {args.agent_type}")
    print(f"  Escuchando en  : {url}")
    print(f"  Agent card     : {url}.well-known/agent.json")
    print()

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
