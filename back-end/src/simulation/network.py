import networkx as nx
from typing import List, Optional

from src.agents.schemas import Agent

GROUP_INFLUENCE = {
    1: 1.0,
    2: 1.0,
    3: 0.8,
    4: 0.5,
    5: 0.4,
    6: 0.0,
}


def same_municipality(agent: Agent, other: Agent) -> bool:
    return bool(agent.municipality and other.municipality and agent.municipality == other.municipality)


def spatial_weight(agent: Agent, other: Agent) -> float:
    return 1.0 if same_municipality(agent, other) else 0.0


def numeric_similarity(value_a: Optional[float], value_b: Optional[float], max_diff: float) -> float:
    if value_a is None or value_b is None:
        return 0.5
    diff = abs(value_a - value_b)
    return max(0.0, 1.0 - min(diff, max_diff) / max_diff)


def homophily_weight(agent: Agent, other: Agent) -> float:
    """
    Computes homophily weight based on:
    - income (continuous): max_diff 100,000
    - age (continuous): max_diff 50
    - building_type (categorical): exact match
    - build_age (categorical 1-10): exact match
    Returns average of 4 similarities.
    """
    income_similarity = numeric_similarity(agent.income, other.income, max_diff=100_000)
    age_similarity = numeric_similarity(agent.age, other.age, max_diff=50)
    building_similarity = 1.0 if agent.building_type and other.building_type and agent.building_type == other.building_type else 0.0
    build_age_similarity = 1.0 if agent.build_age and other.build_age and agent.build_age == other.build_age else 0.0
    return (income_similarity + age_similarity + building_similarity + build_age_similarity) / 4.0


def influence_weight(agent: Agent, other: Agent) -> float:
    agent_influence = GROUP_INFLUENCE.get(agent.group, 0.0)
    other_influence = GROUP_INFLUENCE.get(other.group, 0.0)
    return (agent_influence + other_influence) / 2.0


def edge_weight(agent: Agent, other: Agent) -> float:
    spatial = spatial_weight(agent, other)
    if spatial == 0.0:
        return 0.0
    homophily = homophily_weight(agent, other)
    influence = influence_weight(agent, other)
    return 0.4 * spatial + 0.3 * homophily + 0.3 * influence


def build_agent_graph(agents: List[Agent]) -> nx.Graph:
    graph = nx.Graph()
    for agent in agents:
        graph.add_node(agent.id, **agent.dict(exclude_none=True))

    for i, agent in enumerate(agents):
        for other in agents[i + 1 :]:
            if not same_municipality(agent, other):
                continue
            weight = edge_weight(agent, other)
            graph.add_edge(
                agent.id,
                other.id,
                weight=weight,
                spatial=1.0,
                homophily=homophily_weight(agent, other),
                influence=influence_weight(agent, other),
            )

    return graph
