from src.election_model import NigerianElectionModel


class QuantumElectionCore:
    """Quantum-inspired modeling layer using probability amplitudes."""

    def __init__(self):
        self.model = NigerianElectionModel()

    def build_probability_vector(self, support_dict):
        # Convert support distribution to a normalized amplitude vector
        values = np.array(list(support_dict.values()), dtype=float)
        total = values.sum()
        if total == 0:
            return np.ones(len(values)) / len(values)
        return values / total

    def estimate_quantum_outcome(self, support_dict):
        vector = self.build_probability_vector(support_dict)
        # Quantum-inspired interference effect using magnitude squared
        probabilities = np.square(vector)
        return dict(zip(support_dict.keys(), probabilities.tolist()))


try:
    import numpy as np
except Exception:
    np = None
