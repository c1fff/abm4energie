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


def susceptibility(agent: Any) -> float:
    """
    Calculate personal susceptibility multiplier based on awareness indicators.
    Uses INFO_PAS and INFO_S11 to quantify agent's awareness of sustainable solutions.
    
    Returns a multiplier in range [0.5, 1.5] where:
    - 0.5: low awareness (baseline reduction)
    - 1.0: neutral/average awareness
    - 1.5: high awareness (baseline boost)
    """
    if isinstance(agent, dict):
        info_pas = agent.get("info_pas")
        info_s11 = agent.get("info_s11")
    else:
        info_pas = agent.info_pas
        info_s11 = agent.info_s11
    
    # If no awareness data, use neutral multiplier
    if info_pas is None and info_s11 is None:
        return 1.0
    
    # Normalize values (assume 0-100 scale)
    pas_norm = (info_pas / 100.0) if info_pas is not None else 0.5
    s11_norm = (info_s11 / 100.0) if info_s11 is not None else 0.5
    
    # Average awareness, scale to [0.5, 1.5]
    avg_awareness = (pas_norm + s11_norm) / 2.0
    # Map [0, 1] to [0.5, 1.5]
    multiplier = 0.5 + (avg_awareness * 1.0)
    
    return min(max(multiplier, 0.5), 1.5)  # Clamp to [0.5, 1.5]


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
    base_adoption_probs: Dict[str, float] = field(default_factory=lambda: {
        "UNAWARE": 0.01,
        "AWARE": 0.15,
        "ADOPTED": 1.0,
    })
    # Weighting parameters for influence decomposition
    alpha: float = 0.4  # spatial weight
    beta: float = 0.3   # homophily weight
    gamma: float = 0.3  # influence weight

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
        """
        Calculate adoption probability with susceptibility multiplier.
        
        Formula: P(adopt) = susceptibility(agent) * (1 - ∏(1 - edge_weight * base_p))
                 for all ADOPTED neighbors
        """
        current_state = self.agent_states.get(agent_id, "UNAWARE")
        if current_state == "ADOPTED":
            return 0.0

        # Get personal susceptibility
        agent = self.agents.get(agent_id)
        personal_susceptibility = susceptibility(agent) if agent else 1.0

        neighbors = self.get_neighbors(agent_id)
        if not neighbors:
            base_p = self.base_adoption_probs.get(current_state, 0.0)
            return personal_susceptibility * base_p

        product = 1.0
        for neighbor_id in neighbors:
            neighbor_state = self.agent_states.get(neighbor_id, "UNAWARE")
            if neighbor_state == "ADOPTED":
                edge_weight = self.get_edge_weight(agent_id, neighbor_id)
                base_p = self.base_adoption_probs.get(current_state, 0.0)
                product *= (1.0 - edge_weight * base_p)

        probability = 1.0 - product
        # Apply personal susceptibility multiplier
        return min(personal_susceptibility * probability, 1.0)

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
    agents: List[Agent],
    graph: nx.Graph,
    num_steps: int,
    p_unaware: float = 0.01,
    p_aware: float = 0.15,
    alpha: float = 0.4,
    beta: float = 0.3,
    gamma: float = 0.3,
) -> tuple[List[StepResult], Dict[int, Any]]:
    """
    Run adoption simulation for specified number of steps.
    
    Parameters:
    - agents: List of Agent objects or dicts
    - graph: NetworkX graph with agent network
    - num_steps: Number of simulation steps
    - p_unaware: Base adoption probability for UNAWARE agents (default 0.01)
    - p_aware: Base adoption probability for AWARE agents (default 0.15)
    - alpha: Weight for spatial component (default 0.4)
    - beta: Weight for homophily component (default 0.3)
    - gamma: Weight for influence component (default 0.3)
    
    Returns:
    - tuple: (step_results, agent_history)
      - step_results: List of StepResult for each step
      - agent_history: Dict mapping agent_id to list of historical records
    """
    state = SimulationState()
    state.base_adoption_probs = {
        "UNAWARE": p_unaware,
        "AWARE": p_aware,
        "ADOPTED": 1.0,
    }
    state.alpha = alpha
    state.beta = beta
    state.gamma = gamma
    
    state.init_agents(agents, graph)
    results = []
    agent_history = {}
    
    # Initialize agent history dictionary
    for agent_id in state.agents.keys():
        agent_history[agent_id] = []

    for step in range(num_steps):
        agent_ids = list(state.agents.keys())
        for agent_id in agent_ids:
            current_state = state.agent_states.get(agent_id, "UNAWARE")
            
            # Collect neighbor information for history (only for non-adopted agents)
            neighbors_info = []
            probability = 0.0
            changed = False
            
            if current_state != "ADOPTED":
                probability = state.calculate_adoption_probability(agent_id)
                
                # Collect neighbor information for history
                for neighbor_id in state.get_neighbors(agent_id):
                    neighbor_state = state.agent_states.get(neighbor_id, "UNAWARE")
                    if neighbor_state == "ADOPTED":
                        edge_weight = state.get_edge_weight(agent_id, neighbor_id)
                        base_p = state.base_adoption_probs.get(current_state, 0.0)
                        contribution = edge_weight * base_p
                        neighbors_info.append({
                            "id": neighbor_id,
                            "state": neighbor_state,
                            "weight": edge_weight,
                            "contribution": contribution
                        })
                
                import random
                if random.random() < probability:
                    state.update_agent_state(agent_id, True)
                    changed = True
            
            # Record agent history
            agent_history[agent_id].append({
                "step": step,
                "state": state.agent_states.get(agent_id, current_state),
                "adoption_probability": probability,
                "changed": changed,
                "neighbors": neighbors_info
            })

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

    return results, agent_history
