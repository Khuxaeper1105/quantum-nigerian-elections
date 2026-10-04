from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def plot_party_support(support_distribution: dict[str, float], title: str = "National Party Support") -> None:
    labels = list(support_distribution.keys())
    values = list(support_distribution.values())

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(labels, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])
    ax.set_title(title)
    ax.set_ylabel("Support share")
    ax.set_ylim(0, max(1.0, max(values) * 1.5))
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "party_support.png"), dpi=200)
    plt.close(fig)


def plot_zone_support(zone_support: dict[str, dict[str, float]]) -> None:
    fig, axes = plt.subplots(len(zone_support), 1, figsize=(10, 12), squeeze=False)
    for idx, (zone, support) in enumerate(zone_support.items()):
        parties = list(support.keys())
        values = list(support.values())
        axes[idx, 0].bar(parties, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"])
        axes[idx, 0].set_title(f"{zone} support")
        axes[idx, 0].set_ylim(0, 1.0)
    plt.tight_layout()
    plt.savefig(str(OUTPUT_DIR / "zone_support.png"), dpi=200)
    plt.close(fig)
