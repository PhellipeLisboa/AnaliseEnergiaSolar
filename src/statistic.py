import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# FUNÇÕES ESTATÍSTICAS


def calculate_descriptive_measures(data: pd.Series) -> dict[str, float]:
    """Calcula medidas descritivas de uma variável quantitativa."""

    clean_data = data.dropna()

    mean = np.mean(clean_data)
    median = np.median(clean_data)

    q1 = np.percentile(clean_data, 25)
    q2 = np.percentile(clean_data, 50)
    q3 = np.percentile(clean_data, 75)

    iqr = q3 - q1

    minimum = np.min(clean_data)
    maximum = np.max(clean_data)
    total_range = maximum - minimum

    return {
        "count": len(clean_data),
        "mean": mean,
        "median": median,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "IQR": iqr,
        "minimum": minimum,
        "maximum": maximum,
        "total_range": total_range,
    }


def calculate_mean_median_distance(data: pd.Series) -> dict[str, float]:
    """Calcula a distância relativa entre a média e a mediana."""

    clean_data = data.dropna()

    mean = np.mean(clean_data)
    median = np.median(clean_data)

    relative_distance = (mean - median) / median
    percentage_distance = relative_distance * 100

    return {
        "mean": mean,
        "median": median,
        "relative_distance": relative_distance,
        "percentage_distance": percentage_distance,
    }

# FUNÇÕES GRÁFICAS


def visualize_distribution(data: pd.Series, title: str = "Distribuição dos dados", x_label: str = "Valores") -> None:
    """Gera um histograma com KDE, média e mediana."""

    clean_data = data.dropna()

    mean = np.mean(clean_data)
    median = np.median(clean_data)

    plt.figure(figsize=(10, 6))

    sns.histplot(
        clean_data,
        kde=True,
        bins="auto",
        edgecolor="black"
    )

    plt.axvline(
        mean,
        color="red",
        linestyle="--",
        label=f"Média: {mean:.2f}"
    )

    plt.axvline(
        median,
        color="green",
        linestyle=":",
        label=f"Mediana: {median:.2f}"
    )

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Frequência")
    plt.legend()
    plt.tight_layout()
    plt.show()
