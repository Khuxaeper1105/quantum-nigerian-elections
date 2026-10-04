from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np


class NigerianElectionModel:
    """A probabilistic and quantum-inspired model for Nigerian election analysis."""

    def __init__(self, data_path: str | None = None):
        self.parties = ["APC", "PDP", "LP", "NNPP", "Others"]
        self.zones = {
            "North West": {"weight": 0.20, "turnout": 0.48, "swing": 0.08, "base_support": {"APC": 0.38, "PDP": 0.27, "LP": 0.12, "NNPP": 0.15, "Others": 0.08}},
            "North East": {"weight": 0.14, "turnout": 0.46, "swing": 0.07, "base_support": {"APC": 0.34, "PDP": 0.31, "LP": 0.15, "NNPP": 0.12, "Others": 0.08}},
            "North Central": {"weight": 0.16, "turnout": 0.50, "swing": 0.10, "base_support": {"APC": 0.29, "PDP": 0.34, "LP": 0.18, "NNPP": 0.11, "Others": 0.08}},
            "South West": {"weight": 0.18, "turnout": 0.55, "swing": 0.12, "base_support": {"APC": 0.42, "PDP": 0.26, "LP": 0.16, "NNPP": 0.08, "Others": 0.08}},
            "South South": {"weight": 0.16, "turnout": 0.52, "swing": 0.11, "base_support": {"APC": 0.22, "PDP": 0.42, "LP": 0.18, "NNPP": 0.09, "Others": 0.09}},
            "South East": {"weight": 0.16, "turnout": 0.50, "swing": 0.09, "base_support": {"APC": 0.18, "PDP": 0.41, "LP": 0.25, "NNPP": 0.08, "Others": 0.08}},
        }

        if data_path is None:
            data_path = Path(__file__).resolve().parents[1] / "data" / "sample_nigeria_regions.json"
        self.data_path = Path(data_path)
        self._load_region_data()

    def _load_region_data(self):
        if not self.data_path.exists():
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "regions" in data:
            for region in data["regions"]:
                if region not in self.zones:
                    self.zones[region] = {"weight": 0.10, "turnout": 0.50, "swing": 0.10, "base_support": {p: 1 / len(self.parties) for p in self.parties}}

    def create_zone_support(self, zone: str, turnout_bias: float = 0.0, swing_factor: float = 0.0, uncertainty: float = 0.02) -> Dict[str, float]:
        if zone not in self.zones:
            raise ValueError(f"Unknown zone: {zone}")

        zone_data = self.zones[zone]
        support = {}

        for party in self.parties:
            base = zone_data["base_support"].get(party, 1 / len(self.parties))
            random_shift = np.random.normal(0.0, uncertainty)
            zone_swing = zone_data["swing"] * swing_factor
            adjusted = base + random_shift + zone_swing
            support[party] = max(0.02, adjusted)

        total = sum(support.values())
        support = {party: value / total for party, value in support.items()}
        return support

    def generate_scenario(self, turnout_bias: float = 0.0, swing_factor: float = 0.0, uncertainty: float = 0.02) -> Dict[str, Dict[str, float]]:
        scenario: Dict[str, Dict[str, float]] = {}

        for zone in self.zones:
            support = self.create_zone_support(zone, turnout_bias, swing_factor, uncertainty)
            turnout = self.zones[zone]["turnout"] + turnout_bias + np.random.normal(0.0, uncertainty)
            turnout = max(0.25, min(0.80, turnout))
            scenario[zone] = {"turnout": float(turnout), "support": support}

        return scenario

    def simulate_election(
        self,
        scenario: Dict[str, Dict[str, float]],
        trials: int = 1000,
        turnout_bias: float = 0.0,
        swing_factor: float = 0.0,
        uncertainty: float = 0.02,
    ) -> Dict[str, Dict[str, float] | Dict[str, Dict[str, float]]]:
        national_support = {party: 0.0 for party in self.parties}
        zone_results: Dict[str, Dict[str, float]] = {}

        for zone, zone_data in scenario.items():
            turnout = zone_data["turnout"]
            support = zone_data["support"]
            zone_votes = {party: 0.0 for party in self.parties}

            for _ in range(trials):
                noise = np.random.normal(0.0, uncertainty)
                effective_turnout = max(0.2, min(0.9, turnout + noise + turnout_bias))

                for party in self.parties:
                    swing_noise = np.random.normal(0.0, uncertainty)
                    adjusted = max(0.01, support.get(party, 0.0) + swing_factor + swing_noise)
                    zone_votes[party] += effective_turnout * adjusted

            normalized_zone = {party: value / max(sum(zone_votes.values()), 1e-9) for party, value in zone_votes.items()}
            zone_results[zone] = normalized_zone

            weight = self.zones[zone].get("weight", 1 / len(self.zones))
            for party, value in normalized_zone.items():
                national_support[party] += value * weight

        total = sum(national_support.values())
        national_distribution = {party: value / total for party, value in national_support.items()}

        return {"national": national_distribution, "zones": zone_results}
