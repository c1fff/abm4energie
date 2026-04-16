# ABM4energie

Agent-Based Modeling project for Salzburg heating behavior.

## Overview

This project loads survey data from `survey.json`, cleans and maps it to `Agent` objects, builds a neighbor graph with homophily and influence weights, and runs a step-by-step adoption simulation with personal susceptibility multipliers.

## Features

- Clean survey input data with awareness indicators
- Convert survey records into typed `Agent` objects with building attributes
- Build a weighted social graph between agents (spatial + homophily + influence)
- Run adoption simulation with configurable parameters and personal susceptibility
- Return simulation results via FastAPI endpoints with municipality filtering

## Project Structure

- `src/main.py` - FastAPI application entry point.
- `src/db/repository.py` - Loads raw JSON data.
- `src/db/services.py` - Cleans survey records.
- `src/agents/schemas.py` - Defines the `Agent` model with awareness and building fields.
- `src/agents/services.py` - Converts cleaned records into `Agent` instances.
- `src/agents/views.py` - Exposes `/agents` endpoint.
- `src/simulation/network.py` - Builds the graph and calculates edge weights.
- `src/simulation/services.py` - Loads agents and creates the graph.
- `src/simulation/core.py` - Runs the step-based adoption simulation with susceptibility.
- `src/simulation/views.py` - Exposes `/simulation` and `/simulation/steps` endpoints with parameters.

## Data Flow

1. Load raw survey JSON from `survey.json`.
2. Clean each record in `src/db/services.py`:
   - remove invalid values
   - set default `GROUP_BEH` to `6` if missing
3. Convert cleaned records to `Agent` objects in `src/agents/services.py`.
   - Includes awareness indicators (info_pas, info_s11) and building attributes
4. Build a graph in `src/simulation/network.py`:
   - agents are neighbors if they share the same municipality
   - edge weight = `alpha*spatial + beta*homophily + gamma*influence` (configurable)
   - homophily includes income, age, building_type, and build_age (4 measures)
5. Run adoption simulation in `src/simulation/core.py`:
   - personal susceptibility calculated from awareness indicators [0.5, 1.5]
   - for each step, non-adopted agents check adopted neighbors
   - adoption probability = `susceptibility * (1 - Π(1 - weight * base_p))`
   - state transitions: `UNAWARE → AWARE → ADOPTED`
   - configurable base probabilities and weight parameters
6. Return results through the API with municipality filtering.

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
- `record_to_agent(record)` - creates an `Agent` from a survey record with all fields
- `load_agents()` - returns a list of `Agent` objects

### `src/simulation/network.py`

- `same_municipality(agent, other)` - checks if agents share a municipality
- `spatial_weight(agent, other)` - 1.0 when same municipality
- `numeric_similarity(value_a, value_b, max_diff)` - returns similarity score [0,1]
- `homophily_weight(agent, other)` - computes similarity on income, age, building_type, build_age (4 measures)
- `influence_weight(agent, other)` - averages group influence values
- `edge_weight(agent, other)` - final edge weight = alpha*spatial + beta*homophily + gamma*influence
- `build_agent_graph(agents)` - creates a weighted `networkx.Graph`

### `src/simulation/core.py`

- `susceptibility(agent)` - calculates personal multiplier [0.5, 1.5] from info_pas and info_s11
- `SimulationState` - tracks agent states and graph connections with configurable parameters
- `calculate_adoption_probability(agent_id)` - computes P(adopt) with susceptibility multiplier
- `update_agent_state(agent_id, adopt)` - updates agent state
- `run_simulation_steps(agents, graph, num_steps, p_unaware, p_aware, alpha, beta, gamma)` - executes the step loop with parameters

### `src/simulation/services.py`

- `run_simulation()` - loads agents and builds the graph

## API Endpoints

- `GET /agents` - returns the list of loaded agents
- `GET /simulation?municipality=X` - returns full graph or filtered by municipality
- `GET /simulation/steps?num_steps=N&municipality=X&p_unaware=0.01&p_aware=0.15&alpha=0.4&beta=0.3&gamma=0.3` - runs simulation with parameters

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
- Personal susceptibility is calculated from awareness indicators.
- Homophily includes 4 similarity measures (income, age, building_type, build_age).
- All simulation parameters are configurable via API query parameters.
- Municipality filtering available for both graph and simulation endpoints.
