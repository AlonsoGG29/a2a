# Sports A2A — Comunicación cliente-servidor con el protocolo A2A

Proyecto de demostración de comunicación **Agent-to-Agent (A2A)** usando
**Microsoft Agent Framework** con **Azure AI Foundry** como proveedor LLM.

El tema es **deportes**: fútbol, Fórmula 1, baloncesto y tenis.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENTE                            │
│                                                         │
│  a2a_client.py          a2a_orchestrator.py             │
│  (cliente simple)       (host agent + 2 agentes A2A)   │
└────────────────┬──────────────────┬─────────────────────┘
                 │ A2A / JSON-RPC   │ A2A / JSON-RPC
      ┌──────────▼──────┐  ┌────────▼──────────┐
      │  SERVIDOR :5001  │  │  SERVIDOR :5002   │
      │                  │  │                   │
      │ SportsResults    │  │  SportsStats      │
      │ Agent            │  │  Agent            │
      │  - LiveScores    │  │   - PlayerStats   │
      │  - Standings     │  │   - TeamStats     │
      └──────────────────┘  └───────────────────┘
               │                      │
               └──────────┬───────────┘
                    Azure AI Foundry
                    (gpt-4o-mini)
```

---

## Estructura de ficheros

```
sports-a2a/
├── server/
│   ├── a2a_server.py        # Servidor A2A (Starlette + uvicorn)
│   ├── agent_definitions.py # Definiciones de agentes y AgentCards
│   └── sports_data.py       # Datos mock + herramientas (tools)
├── client/
│   ├── a2a_client.py        # Cliente simple (non-streaming + streaming)
│   └── a2a_orchestrator.py  # Host agent con múltiples agentes A2A como tools
├── .env                     # Variables de entorno (credenciales Foundry)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales

Edita `.env` con tu endpoint de Azure AI Foundry:

```env
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
FOUNDRY_MODEL=gpt-4o-mini
```

Autentícate con Azure CLI:

```bash
az login
```

---

## Ejecución

### Opción A — Cliente simple (un servidor)

**Terminal 1 — Iniciar el servidor de resultados:**
```bash
python server/a2a_server.py --agent-type results --port 5001
```

**Terminal 2 — Ejecutar el cliente:**
```bash
python client/a2a_client.py
```

El cliente:
1. Descubre el agente en `/.well-known/agent.json`
2. Hace una consulta sin streaming
3. Hace una consulta con streaming (SSE)
4. Hace una consulta adicional

---

### Opción B — Orquestador (dos servidores)

**Terminal 1:**
```bash
python server/a2a_server.py --agent-type results --port 5001
```

**Terminal 2:**
```bash
python server/a2a_server.py --agent-type stats --port 5002
```

**Terminal 3:**
```bash
python client/a2a_orchestrator.py
```

El orquestador crea un host agent local (Foundry) que convierte las skills
de cada agente remoto en tools, y decide automáticamente a cuál llamar.

---

## Agentes disponibles

| Tipo       | Puerto | Skills                            |
|------------|--------|-----------------------------------|
| `results`  | 5001   | LiveScores, Standings             |
| `stats`    | 5002   | PlayerStats, TeamStats            |

---

## Consultas de ejemplo

```
# Resultados / Standings
"¿Cuáles son los marcadores en vivo del fútbol?"
"Muéstrame la clasificación de La Liga"
"Clasificación de pilotos de F1 2025"

# Estadísticas
"Estadísticas de Vinicius Jr esta temporada"
"Stats de Max Verstappen en 2025"
"Estadísticas del equipo Real Madrid"

# Consultas mixtas (orquestador)
"¿Quién lidera La Liga y cuáles son los stats de Vinicius Jr?"
"Dame los standings de F1 y las stats de Verstappen"
```

---

## Notas

- Los datos de `sports_data.py` son **mock**. En producción, reemplázalos
  con llamadas reales a APIs como API-Football, Ergast (F1), NBA API, etc.
- El servidor usa `AzureCliCredential` — asegúrate de tener sesión activa (`az login`).
- Para producción, usa `ManagedIdentityCredential` en lugar de `AzureCliCredential`.
