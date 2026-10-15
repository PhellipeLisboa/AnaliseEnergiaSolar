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


def identify_outliers_iqr(data: pd.Series) -> dict:
    """Identifica outliers utilizando o IQR"""

    clean_data = data.dropna()

    q1 = np.percentile(clean_data, 25)
    q3 = np.percentile(clean_data, 75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    lower_outliers = clean_data[clean_data < lower_limit]
    upper_outliers = clean_data[clean_data > upper_limit]

    return {
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "lower_limit": lower_limit,
        "upper_limit": upper_limit,
        "lower_outliers": lower_outliers,
        "upper_outliers": upper_outliers
    }


def calculate_dispersion_measures(data: pd.Series) -> dict[str, float]:
    """Calcula medidas de dispersão de uma variável quantitativa."""

    clean_data = data.dropna()

    mean = np.mean(clean_data)
    variance = np.var(clean_data)
    standard_devation = np.std(clean_data)
    coefficient_of_variation = (standard_devation / mean) * 100

    variance_mean_distance = variance / (mean ** 2)

    if variance_mean_distance <= 0.10:
        dispersion_classification = (
            "Baixa dispersão dos dados em relação à média."
        )
    elif variance_mean_distance < 0.25:
        dispersion_classification = (
            "Dispersão moderada dos dados em relação à média."
        )
    else:
        dispersion_classification = (
            "Alta dispersão dos dados em relação à média."
        )

    return {
        "variance": variance,
        "standard_deviation": standard_devation,
        "coefficient_of_variation": coefficient_of_variation,
        "variance_mean_distance": variance_mean_distance,
        "dispersion_classification": dispersion_classification
    }


def calculate_distribution_shape(data: pd.Series) -> dict[str, float | str]:
    """Calcula e classifica a assimetria e a curtose."""

    clean_data = data.dropna()

    skewness = clean_data.skew()

    if -0.5 <= skewness <= 0.5:
        skewness_classification = (
            "Simétrica ou quase simétrica. "
            "Média e mediana são próximas."
        )
    elif skewness > 0.5:
        skewness_classification = (
            "Assimetria positiva. A cauda se estende para a direita."
        )
    else:
        skewness_classification = (
            "Assimetria negativa. A cauda se estende para a esquerda."
        )

    excess_kurtosis = clean_data.kurtosis()
    real_kurtosis = excess_kurtosis + 3

    if 2.5 <= real_kurtosis <= 3.5:
        kurtosis_classification = (
            "Mesocúrtica. Distribuição próxima da normal."
        )
    elif real_kurtosis < 2.5:
        kurtosis_classification = (
            "Platicúrtica. Dados mais dispersos em relação à média."
        )
    else:
        kurtosis_classification = (
            "Leptocúrtica. Dados concentrados no centro e com caudas pesadas."
        )

    return {
        "skewness": skewness,
        "skewness_classification": skewness_classification,
        "excess_kurtosis": excess_kurtosis,
        "real_kurtosis": real_kurtosis,
        "kurtosis_classification": kurtosis_classification
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


def visualize_boxplot(data: pd.Series, title: str = "Boxplot dos dados", x_label: str = "Valores") -> None:
    """Gera um boxplot de uma variável quantitativa."""

    clean_data = data.dropna()

    plt.figure(figsize=(10, 4))

    sns.boxplot(
        x=clean_data,
    )

    plt.title(title)
    plt.xlabel(x_label)
    plt.tight_layout()
    plt.show()
