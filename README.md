# ABM4energie

Agent-Based Modeling project for Salzburg heating behavior.

## Overview

This project loads survey data from `survey.json`, cleans and maps it to `Agent` objects, builds a neighbor graph, and runs a step-by-step adoption simulation.

## Features

- Clean survey input data
- Convert survey records into typed `Agent` objects
- Build a weighted social graph between agents
- Run adoption simulation over multiple steps
- Return simulation results via FastAPI endpoints

## Project Structure

- `src/main.py` - FastAPI application entry point.
- `src/db/repository.py` - Loads raw JSON data.
- `src/db/services.py` - Cleans survey records.
- `src/agents/schemas.py` - Defines the `Agent` model.
- `src/agents/services.py` - Converts cleaned records into `Agent` instances.
- `src/agents/views.py` - Exposes `/agents` endpoint.
- `src/simulation/network.py` - Builds the graph and calculates edge weights.
- `src/simulation/services.py` - Loads agents and creates the graph.
- `src/simulation/core.py` - Runs the step-based adoption simulation.
- `src/simulation/views.py` - Exposes `/simulation` and `/simulation/steps` endpoints.

## Data Flow

1. Load raw survey JSON from `survey.json`.
2. Clean each record in `src/db/services.py`:
   - remove invalid values
   - set default `GROUP_BEH` to `6` if missing
3. Convert cleaned records to `Agent` objects in `src/agents/services.py`.
4. Build a graph in `src/simulation/network.py`:
   - agents are neighbors if they share the same municipality
   - edge weight = `0.4*spatial + 0.3*homophily + 0.3*influence`
5. Run adoption simulation in `src/simulation/core.py`:
   - for each step, non-adopted agents check adopted neighbors
   - adoption probability = `1 - Π(1 - weight * base_p)`
   - state transitions: `UNAWARE → AWARE → ADOPTED`
6. Return results through the API.

## Key Functions

### `src/db/services.py`

- `normalize_value(value)` - cleans individual values
- `fill_defaults(record)` - normalizes fields and fills defaults
- `clean_survey_data(records)` - filters and cleans survey records
- `load_survey_data()` - returns a list of cleaned survey records

### `src/agents/services.py`

- `parse_int(value)` - safely parses integers
- `parse_float(value)` - safely parses floats
- `get_state_by_group(group)` - maps `GROUP_BEH` to state:
  - `1,2,3` → `ADOPTED`
  - `4,5` → `AWARE`
  - `6` → `UNAWARE`
- `record_to_agent(record)` - creates an `Agent` from a survey record
- `load_agents()` - returns a list of `Agent` objects

### `src/simulation/network.py`

- `same_municipality(agent, other)` - checks if agents share a municipality
- `spatial_weight(agent, other)` - 1.0 when same municipality
- `numeric_similarity(value_a, value_b, max_diff)` - returns similarity score [0,1]
- `homophily_weight(agent, other)` - computes similarity on income, age, building type
- `influence_weight(agent, other)` - averages group influence values
- `edge_weight(agent, other)` - final edge weight formula
- `build_agent_graph(agents)` - creates a weighted `networkx.Graph`

### `src/simulation/core.py`

- `SimulationState` - tracks agent states and graph connections
- `calculate_adoption_probability(agent_id)` - computes adoption probability from adopted neighbors
- `update_agent_state(agent_id, adopt)` - updates agent state
- `run_simulation_steps(agents, graph, num_steps)` - executes the step loop and returns results

### `src/simulation/services.py`

- `run_simulation()` - loads agents and builds the graph

## API Endpoints

- `GET /agents` - returns the list of loaded agents
- `GET /simulation` - returns the first 10 graph nodes and edges
- `GET /simulation/steps?num_steps=N` - runs the adoption simulation for `N` steps and returns step summaries

## Run Locally

```bash
cd /project_destination/
venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

Then open Swagger UI at `http://127.0.0.1:8000/docs`.

## Notes

- The project is currently synchronous.
- The simulation uses a static graph built once from agent attributes.
- Async functions are not required unless you add external I/O or database integration.
