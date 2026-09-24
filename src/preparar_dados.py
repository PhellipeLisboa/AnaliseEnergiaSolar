# Preparar os dados para inserção no banco MySQL

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIRECTORY = PROJECT_ROOT / "datasets"
PROCESSED_DATA_DIRECTORY = DATASET_DIRECTORY / "processados"

PLANT_CODE_MAPPING = {
    4135001: "P01",
    4136001: "P02"
}


def load_generation_data():
    '''Carrega os arquivos originais de geração das duas usinas.'''
    plant_1_path = (DATASET_DIRECTORY / "Plant_1_Generation_Data.csv")
    plant_2_path = (DATASET_DIRECTORY / "Plant_2_Generation_Data.csv")

    plant_1_generation = pd.read_csv(plant_1_path)
    plant_2_generation = pd.read_csv(plant_2_path)

    return plant_1_generation, plant_2_generation


def prepare_generation_data(plant_1_generation, plant_2_generation):
    '''Padroniza e concatena os dados de geração.'''
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
    '''Valida a estrutura do conjunto consolidado de geração.'''
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
    '''Exporta os dados de geração preparados para um arquivo CSV.'''
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
    '''Carrega os arquivos meteorológicos originais das duas usinas.'''
    plant_1_path = (DATASET_DIRECTORY / 'Plant_1_Weather_Sensor_Data.csv')
    plant_2_path = (DATASET_DIRECTORY / 'Plant_2_Weather_Sensor_Data.csv')

    plant_1_weather = pd.read_csv(plant_1_path)
    plant_2_weather = pd.read_csv(plant_2_path)

    return plant_1_weather, plant_2_weather


def prepare_weather_data(plant_1_weather, plant_2_weather):
    '''Padroniza e concatena os dados meteorológicos.'''
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
    '''Valida o conjunto meteorológico consolidado.'''
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
    '''Exporta os dados meteorológicos preparados para CSV.'''
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


def add_friendly_codes(generation_data, weather_data):
    '''Adiciona códigos amigáveis para usinas, inversores e sensores.'''
    generation_data_copy = generation_data.copy()
    weather_data_copy = weather_data.copy()

    generation_data_copy['plant_code'] = (
        generation_data_copy['plant_id'].map(PLANT_CODE_MAPPING)
    )

    weather_data_copy['plant_code'] = (
        weather_data_copy['plant_id'].map(PLANT_CODE_MAPPING)
    )

    # Gerar código dos inversores
    inverter_mapping = {}

    for plant_id, plant_code in PLANT_CODE_MAPPING.items():
        inverter_source_keys = (
            generation_data_copy.loc[
                generation_data_copy['plant_id'] == plant_id,
                'source_key'
            ]
            .drop_duplicates()
            .sort_values()
        )

        for inverter_number, source_key in enumerate(inverter_source_keys, start=1):
            inverter_mapping[(plant_id, source_key)] = (
                f"INV-{plant_code}-{inverter_number:02d}"
            )

    generation_keys = zip(
        generation_data_copy['plant_id'],
        generation_data_copy['source_key']
    )

    generation_data_copy['inverter_code'] = [
        inverter_mapping[key] for key in generation_keys]

    # Gerar código dos sensores
    sensor_mapping = {}

    for plant_id, plant_code in PLANT_CODE_MAPPING.items():
        sensor_source_keys = (
            weather_data_copy.loc[
                weather_data_copy['plant_id'] == plant_id,
                'source_key'
            ]
            .drop_duplicates()
            .sort_values()
        )

        for sensor_number, source_key in enumerate(sensor_source_keys, start=1):
            sensor_mapping[(plant_id, source_key)] = (
                f"SEN-{plant_code}-{sensor_number:02d}"
            )

    weather_keys = zip(
        weather_data_copy['plant_id'],
        weather_data_copy['source_key']
    )

    weather_data_copy['sensor_code'] = [sensor_mapping[key]
                                        for key in weather_keys]

    generation_data_copy = generation_data_copy[
        [
            "date_time",
            "plant_id",
            "plant_code",
            "source_key",
            "inverter_code",
            "dc_power",
            "ac_power",
            "daily_yield",
            "total_yield",
        ]
    ]

    weather_data_copy = weather_data_copy[
        [
            "date_time",
            "plant_id",
            "plant_code",
            "source_key",
            "sensor_code",
            "ambient_temperature",
            "module_temperature",
            "irradiation",
        ]
    ]

    return generation_data_copy, weather_data_copy


def validate_friendly_codes(generation_data, weather_data):
    '''Valida os códigos amigáveis das usinas e equipamentos.'''
    expected_plant_codes = {'P01', 'P02'}

    generation_plant_codes = set(
        generation_data['plant_code'].unique()
    )

    weather_plant_codes = set(
        weather_data['plant_code'].unique()
    )

    inverters_per_plant = (
        generation_data
        .groupby('plant_code')['inverter_code']
        .nunique()
    )

    sensors_per_plant = (
        weather_data
        .groupby('plant_code')['sensor_code']
        .nunique()
    )

    inverter_codes_per_source = (
        generation_data
        .groupby(['plant_id', 'source_key'])['inverter_code']
        .nunique()
    )

    sensor_codes_per_source = (
        weather_data
        .groupby(['plant_id', 'source_key'])['sensor_code']
        .nunique()
    )

    assert generation_plant_codes == expected_plant_codes, (
        "Os códigos das usinas nos dados de geração não correspondem aos valores esperados.")
    assert weather_plant_codes == expected_plant_codes, (
        "Os códigos das usinas nos dados meteorológicos não correspondem aos valores esperados.")
    assert not generation_data[['plant_code', 'inverter_code']].isna().any(
    ).any(), ("Foram encontrados códigos ausentes nos dados de geração.")
    assert not weather_data[['plant_code', 'sensor_code']].isna().any().any(
    ), ("Foram encontrados códigos ausentes nos dados meteorológicos.")
    assert (inverters_per_plant == 22).all(
    ), ("Foi encontrada uma quantidade inesperada de inversores em alguma usina.")
    assert (sensors_per_plant == 1).all(
    ), ("Foi encontrada uma quantidade inesperada de sensores em alguma usina.")

    assert (inverter_codes_per_source == 1).all(
    ), ("Um mesmo inversor recebeu mais de um código.")
    assert (sensor_codes_per_source == 1).all(
    ), ("Um mesmo sensor recebeu mais de um código.")

    print("\nValidação dos códigos concluída com sucesso.")
    print("Inversores por usina:")
    print(inverters_per_plant)

    print("\nSensores por usina:")
    print(sensors_per_plant)


def main():
    plant_1_generation, plant_2_generation = load_generation_data()

    generation_data = prepare_generation_data(
        plant_1_generation=plant_1_generation, plant_2_generation=plant_2_generation)

    validate_generation_data(plant_1_generation=plant_1_generation,
                             plant_2_generation=plant_2_generation, generation_data=generation_data)

    plant_1_weather, plant_2_weather = load_weather_data()

    weather_data = prepare_weather_data(
        plant_1_weather=plant_1_weather, plant_2_weather=plant_2_weather)

    validate_weather_data(plant_1_weather=plant_1_weather,
                          plant_2_weather=plant_2_weather, weather_data=weather_data)

    generation_data, weather_data = add_friendly_codes(
        generation_data=generation_data, weather_data=weather_data)

    validate_friendly_codes(
        generation_data=generation_data, weather_data=weather_data)

    export_generation_data(generation_data)
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
