# Copyright (c) Microsoft. All rights reserved.
# Sports A2A Client — connects to the sports server via A2A protocol

import asyncio
import os

import httpx
from a2a.client import A2ACardResolver
from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv

load_dotenv()

"""
Sports A2A Client — communicates with the SportsResultsAgent or SportsStatsAgent via A2A.

Demonstrates both non-streaming and streaming modes. The agent runs server-side;
this client only needs the A2A endpoint URL to discover capabilities and send queries.

Prerequisites:
  Start the server first:
    uv run python server/a2a_server.py --agent-type results --port 5001

Environment variables (in .env):
  A2A_AGENT_HOST  — URL of the running A2A server (default: http://localhost:5001/)

Usage:
  uv run python client/a2a_client.py
"""

# Sports queries to demonstrate the agent
DEMO_QUERIES = [
    "What are the live football scores right now?",
    "Show me the La Liga standings",
    "What are the F1 driver standings for 2025?",
]


async def main() -> None:
    """Connects to the Sports A2A agent and runs a set of demo queries."""
    a2a_agent_host = os.getenv("A2A_AGENT_HOST", "http://localhost:5001/")
    print(f"Connecting to Sports A2A agent at: {a2a_agent_host}\n")

    # 1. Resolve the agent card — discovers what the agent can do
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        resolver = A2ACardResolver(httpx_client=http_client, base_url=a2a_agent_host)
        agent_card = await resolver.get_agent_card()

    print(f"Agent found  : {agent_card.name}")
    print(f"Description  : {agent_card.description}")
    print(f"Skills ({len(agent_card.skills)})  :", ", ".join(s.name for s in agent_card.skills))
    print()

    # 2. Create the A2A agent wrapper and run queries
    async with A2AAgent(
        name=agent_card.name,
        description=agent_card.description,
        agent_card=agent_card,
        url=a2a_agent_host,
    ) as agent:

        # --- Non-streaming: single question/answer ---
        print("=" * 60)
        print("NON-STREAMING QUERY")
        print("=" * 60)
        query = DEMO_QUERIES[0]
        print(f"User  : {query}")
        response = await agent.run(query)
        print(f"Agent : {response.text}\n")

        # --- Streaming: receive response incrementally ---
        print("=" * 60)
        print("STREAMING QUERY")
        print("=" * 60)
        query = DEMO_QUERIES[1]
        print(f"User  : {query}")
        print("Agent : ", end="", flush=True)

        stream = agent.run(query, stream=True)
        async for update in stream:
            for content in update.contents:
                if content.text:
                    print(content.text, end="", flush=True)
        print()  # newline after streaming ends

        final = await stream.get_final_response()
        print(f"\n[Final response received — {len(final.text)} chars]\n")

        # --- Additional query ---
        print("=" * 60)
        print("ADDITIONAL QUERY")
        print("=" * 60)
        query = DEMO_QUERIES[2]
        print(f"User  : {query}")
        response = await agent.run(query)
        print(f"Agent : {response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
