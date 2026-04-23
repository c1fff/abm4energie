# ABM4energie

Agent-Based Modeling project for heating adoption behavior in Salzburg.

## Overview

ABM4energie loads survey data from `survey.json`, converts each record into an `Agent`, builds a weighted social network, and simulates adoption dynamics over multiple steps.

The simulation uses:
- municipality-based spatial connectivity
- homophily on income, age, building type, and building age
- influence weighting based on adoption group
- personal susceptibility from awareness indicators (`INFO_PAS`, `INFO_S11`)

## Project Structure

- `src/main.py` - FastAPI application entry point.
- `src/db/repository.py` - loads raw survey JSON from `survey.json`.
- `src/db/services.py` - cleans survey records and fills defaults.
- `src/agents/schemas.py` - defines the `Agent` data model.
- `src/agents/services.py` - converts cleaned records into `Agent` objects.
- `src/agents/views.py` - exposes agent endpoints.
- `src/simulation/network.py` - builds a weighted agent graph.
- `src/simulation/services.py` - loads agents and builds the graph.
- `src/simulation/core.py` - runs the step-based adoption simulation.
- `src/simulation/views.py` - exposes simulation endpoints.

## Data Flow

1. `src/db/services.py` loads raw survey records and normalizes values.
2. Invalid or missing fields are cleaned; missing `GROUP_BEH` defaults to `6`.
3. `src/agents/services.py` converts each record into an `Agent`.
4. `src/simulation/network.py` builds a graph connecting agents in the same municipality.
   - edge weight is composed of spatial, homophily, and influence components.
5. `src/simulation/core.py` runs `run_simulation_steps()` to simulate adoption.
   - adoption probability is influenced by adopted neighbors and agent susceptibility.

## Key Functions

### `src/db/services.py`

- `normalize_value(value)` - cleans raw values and normalizes empty or invalid strings.
- `fill_defaults(record)` - normalizes each field and defaults missing `GROUP_BEH` to `6`.
- `clean_survey_data(records)` - filters and cleans survey records.
- `load_survey_data()` - returns cleaned survey data.

### `src/agents/services.py`

- `parse_int(value)` - safely converts strings or numbers to integers.
- `parse_float(value)` - safely converts strings or numbers to floats.
- `get_state_by_group(group)` - maps `GROUP_BEH` values to state labels:
  - `1, 2, 3` → `ADOPTED`
  - `4, 5` → `AWARE`
  - `6` → `UNAWARE`
- `record_to_agent(record)` - builds an `Agent` object from a cleaned survey record.
- `load_agents()` - returns a list of `Agent` instances.

### `src/simulation/network.py`

- `same_municipality(agent, other)` - checks whether two agents share the same municipality.
- `spatial_weight(agent, other)` - returns `1.0` when agents share a municipality, otherwise `0.0`.
- `numeric_similarity(value_a, value_b, max_diff)` - computes similarity for numeric values.
- `homophily_weight(agent, other)` - averages similarity for income, age, building type, and build age.
- `influence_weight(agent, other)` - averages influence values derived from agent groups.
- `edge_weight(agent, other)` - returns the weighted edge score for same-municipality agents.
- `build_agent_graph(agents)` - creates a `networkx.Graph` with nodes and weighted edges.

### `src/simulation/core.py`

- `susceptibility(agent)` - computes a personal multiplier in `[0.5, 1.5]` from awareness indicators.
- `SimulationState` - holds agent states, graph, and adoption probabilities.
- `calculate_adoption_probability(agent_id)` - computes adoption probability from adopted neighbors.
- `update_agent_state(agent_id, adopt)` - applies state transitions when adoption occurs.
- `run_simulation_steps(...)` - runs the stepwise adoption simulation and returns summarized results.

### `src/simulation/services.py`

- `run_simulation()` - loads agents and returns the built agent graph.

## API Endpoints

- `GET /agents` - returns all loaded agents.
- `GET /agents/municipalities` - returns agents grouped by municipality.
- `GET /agents/income` - returns counts by income group.
- `GET /simulation/steps` - runs the adoption simulation.

### Simulation query parameters

- `num_steps` - number of simulation steps (default `10`).
- `municipality` - optional municipality filter.
- `p_unaware` - base probability for `UNAWARE` agents (default `0.01`).
- `p_aware` - base probability for `AWARE` agents (default `0.15`).
- `alpha` - spatial component weight (default `0.4`).
- `beta` - homophily component weight (default `0.3`).
- `gamma` - influence component weight (default `0.3`).

## Run Locally

```powershell
cd C:\Users\rauan\Desktop\Projects\abm4energie
venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```
### For analysis
```
source venv/bin/activate
cd analysis
pip3 install requirements.txt
python3 main.py
```


Open the API docs at `http://127.0.0.1:8000/docs`.

## Notes

- Agents are connected only when they share the same municipality.
- Homophily is computed from income, age, building type, and building age.
- The simulation uses a fixed graph and random adoption outcomes per step.
- Susceptibility is derived from the agent's awareness indicators.
