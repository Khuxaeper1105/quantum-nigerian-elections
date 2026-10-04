from src.election_model import NigerianElectionModel


def main():
    model = NigerianElectionModel()

    # Example simulation setup
    scenario = model.generate_scenario(
        turnout_bias=0.05,
        swing_factor=0.12,
        uncertainty=0.08
    )

    print("=== Nigerian Election Simulation ===")
    print(scenario)

    summary = model.simulate_election(scenario, trials=500)
    print("\n=== Summary ===")
    print(summary)


if __name__ == "__main__":
    main()
