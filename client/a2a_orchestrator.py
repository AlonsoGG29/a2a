# Copyright (c) Microsoft. All rights reserved.
# Sports A2A Orchestrator — host agent that uses multiple sports agents as function tools

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
Sports A2A Orchestrator — wraps multiple A2A agents as tools for a host agent.

This is the more advanced client pattern: a local Foundry-backed agent receives
the user's sports questions and decides which remote A2A agent (results / stats)
to call, transparently composing the final answer.

Prerequisites:
  Terminal 1: uv run python server/a2a_server.py --agent-type results --port 5001
  Terminal 2: uv run python server/a2a_server.py --agent-type stats   --port 5002

Environment variables (in .env):
  FOUNDRY_PROJECT_ENDPOINT  — Azure AI Foundry project endpoint
  FOUNDRY_MODEL             — Model deployment name (e.g. gpt-4o-mini)
  A2A_RESULTS_HOST          — Results agent URL (default: http://localhost:5001/)
  A2A_STATS_HOST            — Stats agent URL   (default: http://localhost:5002/)

Usage:
  uv run python client/a2a_orchestrator.py
"""

ORCHESTRATOR_INSTRUCTIONS = """\
You are a sports information assistant. You have access to two specialized agents:
- A results agent: for live scores, match results, and league standings
- A stats agent: for detailed player and team statistics

Route user queries to the appropriate agent. For complex questions, call both.
Always provide clear, well-formatted answers with the most relevant data.
"""

# Demo queries that require different agents
DEMO_QUERIES = [
    "Who is leading the La Liga table and what are Vinicius Jr's stats this season?",
    "Give me the F1 standings and Max Verstappen's 2025 stats.",
]


async def resolve_agent(http_client: httpx.AsyncClient, host_url: str, label: str) -> tuple:
    """Resolves an A2A agent card and returns (agent_card, A2AAgent context)."""
    resolver = A2ACardResolver(httpx_client=http_client, base_url=host_url)
    card = await resolver.get_agent_card()
    print(f"  Resolved {label}: {card.name} ({len(card.skills)} skill(s))")
    return card


async def main() -> None:
    """Runs the orchestrator host agent against multiple sports A2A agents."""
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")
    results_host = os.getenv("A2A_RESULTS_HOST", "http://localhost:5001/")
    stats_host = os.getenv("A2A_STATS_HOST", "http://localhost:5002/")

    if not project_endpoint or not model:
        raise ValueError("FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL must be set in .env")

    print("Resolving remote A2A agents...")
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        results_card = await resolve_agent(http_client, results_host, "Results agent")
        stats_card = await resolve_agent(http_client, stats_host, "Stats agent")
    print()

    # Create the Foundry host agent with A2A skill tools
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
        # Convert each skill into a function tool
        def make_tools(a2a_agent, card):
            return [
                a2a_agent.as_tool(
                    name=re.sub(r"[^0-9A-Za-z]+", "_", skill.name),
                    description=skill.description or "",
                )
                for skill in card.skills
            ]

        all_tools = make_tools(results_agent, results_card) + make_tools(stats_agent, stats_card)

        host_agent = client.as_agent(
            name="SportsOrchestrator",
            instructions=ORCHESTRATOR_INSTRUCTIONS,
            tools=all_tools,
        )

        print(f"Host agent ready with {len(all_tools)} tools:")
        for tool in all_tools:
            print(f"  - {tool.name}")
        print()

        # Run the demo queries
        for query in DEMO_QUERIES:
            print("=" * 60)
            print(f"User  : {query}")
            response = await host_agent.run(query)
            print(f"Agent : {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
