import networkx as nx
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import Counter

from src.agents.schemas import Agent

BASE_ADOPTION_PROBABILITY = {
    "UNAWARE": 0.01,
    "AWARE": 0.15,
    "ADOPTED": 1.0,  # Already adopted, no change
}

STATE_TRANSITION = {
    "UNAWARE": "AWARE",
    "AWARE": "ADOPTED",
    "ADOPTED": "ADOPTED",
}


@dataclass
class StepResult:
    step: int
    adopted_count: int
    total_agents: int
    adopted_rate: float
    state_distribution: Dict[str, int]
    group_distribution: Dict[int, int]


@dataclass
class SimulationState:
    agents: Dict[int, Agent] = field(default_factory=dict)
    agent_states: Dict[int, str] = field(default_factory=dict)
    graph: Optional[nx.Graph] = None

    def init_agents(self, agents: List, graph: nx.Graph) -> None:
        self.graph = graph
        for agent in agents:
            if isinstance(agent, dict):
                agent_id = agent.get("id")
                state = agent.get("state", "UNAWARE")
                self.agents[agent_id] = agent
            else:
                agent_id = agent.id
                state = agent.state or "UNAWARE"
                self.agents[agent_id] = agent
            self.agent_states[agent_id] = state

    def get_neighbors(self, agent_id: int) -> List[int]:
        if not self.graph:
            return []
        return list(self.graph.neighbors(agent_id))

    def get_edge_weight(self, agent_id: int, neighbor_id: int) -> float:
        if not self.graph or not self.graph.has_edge(agent_id, neighbor_id):
            return 0.0
        return self.graph[agent_id][neighbor_id].get("weight", 0.0)

    def calculate_adoption_probability(self, agent_id: int) -> float:
        current_state = self.agent_states.get(agent_id, "UNAWARE")
        if current_state == "ADOPTED":
            return 0.0

        neighbors = self.get_neighbors(agent_id)
        if not neighbors:
            base_p = BASE_ADOPTION_PROBABILITY.get(current_state, 0.0)
            return base_p

        product = 1.0
        for neighbor_id in neighbors:
            neighbor_state = self.agent_states.get(neighbor_id, "UNAWARE")
            if neighbor_state == "ADOPTED":
                edge_weight = self.get_edge_weight(agent_id, neighbor_id)
                base_p = BASE_ADOPTION_PROBABILITY.get(current_state, 0.0)
                product *= (1.0 - edge_weight * base_p)

        probability = 1.0 - product
        return min(probability, 1.0)

    def update_agent_state(self, agent_id: int, adopt: bool) -> None:
        current_state = self.agent_states.get(agent_id, "UNAWARE")
        if adopt and current_state != "ADOPTED":
            self.agent_states[agent_id] = STATE_TRANSITION.get(current_state, current_state)

    def get_state_distribution(self) -> Dict[str, int]:
        return dict(Counter(self.agent_states.values()))

    def get_group_distribution(self) -> Dict[int, int]:
        distribution = {}
        for agent_id, agent in self.agents.items():
            if isinstance(agent, dict):
                group = agent.get("group")
            else:
                group = agent.group
            if group is not None:
                distribution[group] = distribution.get(group, 0) + 1
        return distribution

    def count_adopted(self) -> int:
        return sum(1 for state in self.agent_states.values() if state == "ADOPTED")


def run_simulation_steps(
    agents: List[Agent], graph: nx.Graph, num_steps: int = 10
) -> List[StepResult]:
    state = SimulationState()
    state.init_agents(agents, graph)
    results = []

    for step in range(num_steps):
        agent_ids = list(state.agents.keys())
        for agent_id in agent_ids:
            current_state = state.agent_states.get(agent_id, "UNAWARE")
            if current_state == "ADOPTED":
                continue

            probability = state.calculate_adoption_probability(agent_id)
            import random
            if random.random() < probability:
                state.update_agent_state(agent_id, True)

        adopted_count = state.count_adopted()
        adopted_rate = adopted_count / len(agents) if agents else 0.0
        state_dist = state.get_state_distribution()

        result = StepResult(
            step=step,
            adopted_count=adopted_count,
            total_agents=len(agents),
            adopted_rate=adopted_rate,
            state_distribution=state_dist,
            group_distribution=state.get_group_distribution(),
        )
        results.append(result)

    return results
