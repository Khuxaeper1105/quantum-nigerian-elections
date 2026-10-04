import matplotlib.pyplot as plt


def plot_region_support(region_data):
    labels = list(region_data.keys())
    values = list(region_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="steelblue")
    plt.title("Estimated Support by Region")
    plt.ylabel("Relative Support")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
