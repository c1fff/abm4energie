from src.agents.services import load_agents
from src.simulation.network import build_agent_graph
from src.simulation.core import run_simulation_steps


def run_scenario(name, p_unaware, p_aware, alpha, beta, gamma):
    print(f"\n=== {name} ===")

    agents = load_agents()
    graph = build_agent_graph(agents)

    results = run_simulation_steps(
        agents=agents,
        graph=graph,
        num_steps=10,
        p_unaware=p_unaware,
        p_aware=p_aware,
        alpha=alpha,
        beta=beta,
        gamma=gamma
    )

    final_step = results[-1]

    print(f"Final adoption rate: {final_step.adopted_rate:.2f}")
    print(f"Adopted: {final_step.adopted_count}/{final_step.total_agents}")

    return final_step.adopted_rate


def main():
    scenarios = [
        {
            "name": "Low Awareness",
            "params": dict(p_unaware=0.01, p_aware=0.05, alpha=0.4, beta=0.3, gamma=0.3)
        },
        {
            "name": "High Awareness Campaign",
            "params": dict(p_unaware=0.1, p_aware=0.2, alpha=0.4, beta=0.3, gamma=0.3)
        },
        {
            "name": "Strong Social Influence",
            "params": dict(p_unaware=0.05, p_aware=0.1, alpha=0.2, beta=0.2, gamma=0.6)
        }
    ]

    results = {}

    for scenario in scenarios:
        rate = run_scenario(scenario["name"], **scenario["params"])
        results[scenario["name"]] = rate

    print("\n=== COMPARISON ===")
    for name, rate in results.items():
        print(f"{name}: {rate:.2f}")


if __name__ == "__main__":
    main()