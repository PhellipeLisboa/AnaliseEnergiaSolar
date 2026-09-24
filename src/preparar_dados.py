# Preparar os dados para inserção no banco MySQL

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIRECTORY = PROJECT_ROOT / "datasets"
PROCESSED_DATA_DIRECTORY = DATASET_DIRECTORY / "processados"


def load_generation_data():
    """Carrega os arquivos originais de geração das duas usinas."""
    plant_1_path = (DATASET_DIRECTORY / "Plant_1_Generation_Data.csv")
    plant_2_path = (DATASET_DIRECTORY / "Plant_2_Generation_Data.csv")

    plant_1_generation = pd.read_csv(plant_1_path)
    plant_2_generation = pd.read_csv(plant_2_path)

    return plant_1_generation, plant_2_generation


def prepare_generation_data(plant_1_generation, plant_2_generation):
    """Padroniza e concatena os dados de geração."""
    plant_1_generation_copy = plant_1_generation.copy()
    plant_2_generation_copy = plant_2_generation.copy()

    generation_columns = {
        "DATE_TIME": "date_time",
        "PLANT_ID": "plant_id",
        "SOURCE_KEY": "source_key",
        "DC_POWER": "dc_power",
        "AC_POWER": "ac_power",
        "DAILY_YIELD": "daily_yield",
        "TOTAL_YIELD": "total_yield",
    }

    plant_1_generation_copy = plant_1_generation_copy.rename(
        columns=generation_columns
    )

    plant_2_generation_copy = plant_2_generation_copy.rename(
        columns=generation_columns
    )

    plant_1_generation_copy['date_time'] = pd.to_datetime(
        plant_1_generation_copy['date_time'],
        format="%d-%m-%Y %H:%M"
    )

    plant_2_generation_copy['date_time'] = pd.to_datetime(
        plant_2_generation_copy['date_time'],
        format="%Y-%m-%d %H:%M:%S"
    )

    generation_data = pd.concat(
        [
            plant_1_generation_copy,
            plant_2_generation_copy
        ], ignore_index=True
    )

    return generation_data


def validate_generation_data(plant_1_generation, plant_2_generation, generation_data):
    """Valida a estrutura do conjunto consolidado de geração."""
    expected_rows = (len(plant_1_generation) + len(plant_2_generation))
    actual_rows = len(generation_data)

    plants_count = generation_data["plant_id"].nunique()

    duplicated_measurements = generation_data.duplicated(
        subset=["plant_id", "source_key", "date_time"]
    ).sum()

    missing_key_values = generation_data[
        ["plant_id", "source_key", "date_time"]
    ].isna().sum()

    expected_columns = [
        "date_time",
        "plant_id",
        "source_key",
        "dc_power",
        "ac_power",
        "daily_yield",
        "total_yield"
    ]

    assert actual_rows == expected_rows, (
        "A quantidade de registros após a concatenação não corresponde à soma dos arquivos originais.")
    assert plants_count == 2, ("O conjunto preparado deveria possuir duas usinas.")
    assert duplicated_measurements == 0, (
        "Foram encontradas medições duplicadas na chave candidata.")
    assert missing_key_values.sum(
    ) == 0, ("Foram encontrados valores ausentes nas colunas da chave.")
    assert generation_data.columns.tolist() == expected_columns, (
        "As colunas do conjunto preparado não correspondem à estrutura esperada.")

    print("Validação dos dados de geração concluída com sucesso.")
    print(f"Registros esperados: {expected_rows}")
    print(f"Registros encontrados: {actual_rows}")
    print(f"Usinas encontradas: {plants_count}")


def export_generation_data(generation_data):
    """Exporta os dados de geração preparados para um arquivo CSV."""
    PROCESSED_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        PROCESSED_DATA_DIRECTORY / "generation_data.csv"
    )

    generation_data.to_csv(
        output_path,
        index=False,
        date_format="%Y-%m-%d %H:%M:%S"
    )

    assert output_path.exists(), ("O arquivo processado não foi criado.")

    print("\nDados de geração exportados com sucesso.")
    print(f"Arquivo gerado: {output_path}\n")


def load_weather_data():
    """Carrega os arquivos meteorológicos originais das duas usinas."""
    plant_1_path = (DATASET_DIRECTORY / 'Plant_1_Weather_Sensor_Data.csv')
    plant_2_path = (DATASET_DIRECTORY / 'Plant_2_Weather_Sensor_Data.csv')

    plant_1_weather = pd.read_csv(plant_1_path)
    plant_2_weather = pd.read_csv(plant_2_path)

    return plant_1_weather, plant_2_weather


def prepare_weather_data(plant_1_weather, plant_2_weather):
    """Padroniza e concatena os dados meteorológicos."""
    plant_1_weather_copy = plant_1_weather.copy()
    plant_2_weather_copy = plant_2_weather.copy()

    weather_columns = {
        "DATE_TIME": "date_time",
        "PLANT_ID": "plant_id",
        "SOURCE_KEY": "source_key",
        "AMBIENT_TEMPERATURE": "ambient_temperature",
        "MODULE_TEMPERATURE": "module_temperature",
        "IRRADIATION": "irradiation"
    }

    plant_1_weather_copy = plant_1_weather_copy.rename(columns=weather_columns)
    plant_2_weather_copy = plant_2_weather_copy.rename(columns=weather_columns)

    plant_1_weather_copy['date_time'] = pd.to_datetime(
        plant_1_weather_copy['date_time'],
        format="%Y-%m-%d %H:%M:%S"
    )

    plant_2_weather_copy['date_time'] = pd.to_datetime(
        plant_2_weather_copy['date_time'],
        format="%Y-%m-%d %H:%M:%S"
    )

    weather_data = pd.concat(
        [
            plant_1_weather_copy,
            plant_2_weather_copy
        ],
        ignore_index=True
    )

    return weather_data


def validate_weather_data(plant_1_weather, plant_2_weather, weather_data):
    """Valida o conjunto meteorológico consolidado."""
    expected_rows = (len(plant_1_weather) + len(plant_2_weather))
    actual_rows = len(weather_data)

    plants_count = weather_data['plant_id'].nunique()

    duplicated_measurements = weather_data.duplicated(
        subset=['plant_id', 'source_key', 'date_time']
    ).sum()

    missing_key_values = weather_data[
        ['plant_id', 'source_key', 'date_time']
    ].isna().sum()

    expected_columns = [
        "date_time",
        "plant_id",
        "source_key",
        "ambient_temperature",
        "module_temperature",
        "irradiation"
    ]

    sensors_by_plant = (
        weather_data
        .groupby('plant_id')['source_key']
        .nunique()
    )

    assert actual_rows == expected_rows, (
        "A quantidade de registros climáticos não corrresponde à soma dos arquivos originais.")
    assert plants_count == 2, ("O cojunto climático deveria possuir duas usinas.")
    assert duplicated_measurements == 0, (
        "Foram encontradas medições climáticas duplicadas.")
    assert missing_key_values.sum(
    ) == 0, ("Foram encontrados valores ausentes nas colunas da chave candidate.")
    assert weather_data.columns.tolist() == expected_columns, (
        "As colunas meteorológicas não correspondem à estrutura esperada.")
    assert (sensors_by_plant == 1).all(
    ), ("Foi encontrada uma quantidade inesperada de sensores em alguma usina.")

    print("\nValidação dos dados meteorológicos concluída com sucesso.")
    print(f"Registros esperados: {expected_rows}")
    print(f"Registros encontrados: {actual_rows}")
    print(f"Usinas encontradas: {plants_count}")
    print("Sensores encontrados por usina:")
    print(sensors_by_plant)


def export_weather_data(weather_data):
    """Exporta os dados meteorológicos preparados para CSV."""
    PROCESSED_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (PROCESSED_DATA_DIRECTORY / 'weather_data.csv')

    weather_data.to_csv(
        output_path,
        index=False,
        date_format="%Y-%m-%d %H:%M:%S"
    )

    assert output_path.exists(), ("O arquivo climático processado não foi criado.")

    print("\nDados climáticos exportados com sucesso.")
    print(f"Arquivo gerado: {output_path}\n")


def main():
    plant_1_generation, plant_2_generation = load_generation_data()

    generation_data = prepare_generation_data(
        plant_1_generation, plant_2_generation)

    validate_generation_data(
        plant_1_generation, plant_2_generation, generation_data)

    export_generation_data(generation_data)

    plant_1_weather, plant_2_weather = load_weather_data()

    weather_data = prepare_weather_data(plant_1_weather, plant_2_weather)

    validate_weather_data(plant_1_weather, plant_2_weather, weather_data)

    export_weather_data(weather_data)

    print("\nResumo dos dados preparados:")
    print(f"Geração: {generation_data.shape}")
    print(f"Dados meteorológicos: {weather_data.shape}")
    print("-"*100)
    print(generation_data)
    print("-"*100)
    print(weather_data)
    print("-"*100)


if __name__ == "__main__":
    main()
