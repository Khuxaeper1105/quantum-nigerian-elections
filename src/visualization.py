from __future__ import annotations

from typing import Dict

import numpy as np

try:
    from qiskit import QuantumCircuit
except ImportError:  # pragma: no cover
    QuantumCircuit = None


class QuantumElectionEngine:
    """Quantum-inspired election engine using amplitudes and probability amplitudes."""

    def __init__(self, support_distribution: Dict[str, float]):
        self.support_distribution = self._normalize(support_distribution)

    @staticmethod
    def _normalize(distribution: Dict[str, float]) -> Dict[str, float]:
        values = np.array(list(distribution.values()), dtype=float)
        total = values.sum()
        if total <= 0:
            uniform = 1.0 / len(distribution)
            return {party: uniform for party in distribution}
        return {party: float(value / total) for party, value in distribution.items()}

    def amplitude_vector(self) -> np.ndarray:
        values = np.array(list(self.support_distribution.values()), dtype=float)
        values = np.sqrt(values)
        norm = np.linalg.norm(values)
        if norm == 0:
            return np.ones(len(values), dtype=float) / np.sqrt(len(values))
        return values / norm

    def probability_distribution(self) -> Dict[str, float]:
        amplitudes = self.amplitude_vector()
        probabilities = np.abs(amplitudes) ** 2
        total = probabilities.sum()
        if total == 0:
            return {party: 1 / len(self.support_distribution) for party in self.support_distribution}
        probability_map = {party: float(p / total) for party, p in zip(self.support_distribution.keys(), probabilities)}
        return probability_map

    def interfere(self, phase_shift: float = 0.5) -> Dict[str, float]:
        amplitudes = self.amplitude_vector()
        phases = np.exp(1j * np.linspace(0.0, phase_shift, len(amplitudes)))
        interfered = amplitudes * phases
        probabilities = np.abs(interfered) ** 2
        total = probabilities.sum()
        if total == 0:
            return {party: 1 / len(self.support_distribution) for party in self.support_distribution}
        return {party: float(p / total) for party, p in zip(self.support_distribution.keys(), probabilities)}

    def build_qiskit_circuit(self):
        if QuantumCircuit is None:
            return None

        num_qubits = max(1, int(np.ceil(np.log2(len(self.support_distribution)))))
        qc = QuantumCircuit(num_qubits)
        qc.h(range(num_qubits))
        return qc
