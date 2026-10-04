import json
from pathlib import Path

from src.election_model import NigerianElectionModel
from src.quantum_election import QuantumElectionEngine
from src.visualization import plot_party_support


def main():
    model = NigerianElectionModel()
    scenario = model.generate_scenario(
        turnout_bias=0.03,
        swing_factor=0.12,
        uncertainty=0.05,
    )

    print("=== Nigerian Election Simulation ===")
    print(json.dumps(scenario, indent=2, sort_keys=True))

    summary = model.simulate_election(
        scenario=scenario,
        trials=2000,
        turnout_bias=0.04,
        swing_factor=0.10,
        uncertainty=0.04,
    )

    print("\n=== National Summary ===")
    print(json.dumps(summary["national"], indent=2, sort_keys=True))

    quantum_engine = QuantumElectionEngine(summary["national"])
    quantum_distribution = quantum_engine.probability_distribution()
    print("\n=== Quantum-Inspired Probability Distribution ===")
    print(json.dumps(quantum_distribution, indent=2, sort_keys=True))

    plot_party_support(summary["national"])


if __name__ == "__main__":
    main()
