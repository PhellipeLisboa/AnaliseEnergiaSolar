# Integração entre Python e o banco MySQL do projeto.

# Integração entre Python e o banco MySQL do projeto.

import mysql.connector
from typing import Any

TAMANHO_RELATORIO = 162


def obter_dados_do_banco(query: str) -> tuple[tuple[str, ...], list[tuple[Any, ...]]] | None:
    '''
    Executa uma consulta no banco MySQL e retorna suas colunas e resultados.

    Args:
        query: Instrução SQL que será executada no banco de dados.

    Returns:
        Tupla contendo os nomes das colunas e a lista de registros retornados pela consulta. Retorna None se ocorrer um erro ao acessar o banco de dados.
    '''
    conexao = None
    cursor = None

    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database="solar_power"
        )
        cursor = conexao.cursor()
        cursor.execute(query)
        colunas = cursor.column_names
        resultados = cursor.fetchall()
        return colunas, resultados
    except mysql.connector.Error as erro:
        print(f"Erro ao acessar o MySQL: {erro}")
        return None
    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def exibir_resultados(consulta: dict[str, str], resultado_consulta: tuple[tuple[str, ...], list[tuple[Any, ...]]] | None) -> None:
    '''
    Formata e exibe no terminal os resultados de uma consulta estratégica.

    Args:
        consulta: Dicionário contendo a pergunta estratégica e a instrução SQL associada.
        resultado_consulta: Tupla contendo os nomes das colunas e a lista de registros retornados pela consulta. Pode ser None quando ocorrer um erro no acesso ao banco de dados.

    Returns:
        None.

    Raises:
        KeyError: Se a chave pergunta não estiver presente no dicionário da consulta.
    '''
    print("=" * TAMANHO_RELATORIO)
    print(consulta["pergunta"].center(TAMANHO_RELATORIO))
    print("=" * TAMANHO_RELATORIO)

    if resultado_consulta is None:
        return

    colunas, dados = resultado_consulta

    tamanho_colunas = []
    # O numero de divisórias é sempre o número de colunas - 1. O resultado é multiplicado por 3 porque a divisória usada é composta por 3 caracteres " | "
    tamanho_linha = (len(colunas) - 1) * 3
    for coluna in colunas:
        tamanho_colunas.append(len(coluna))
        tamanho_linha += len(coluna)

    if not dados:
        print("Nenhum resultado encontrado.")
        return

    print(((tamanho_linha) * "_").center(TAMANHO_RELATORIO))
    print(("|" + " | ".join(colunas) + "|").center(TAMANHO_RELATORIO))
    print(("|" + "-" * tamanho_linha + "|").center(TAMANHO_RELATORIO))

    for linha in dados:
        valores = [str(valor) for valor in linha]
        for posicao, valor in enumerate(valores):
            valores[posicao] = valor.ljust(tamanho_colunas[posicao])
        print(("|" + " | ".join(valores) + "|").center(TAMANHO_RELATORIO))
    print(((tamanho_linha) * "-").center(TAMANHO_RELATORIO))


def mostrar_relatorio_completo(lista_de_consultas: list[dict[str, str]]) -> None:
    '''
    Executa e exibe todas as consultas estratégicas definidas.

    Args:
        lista_de_consultas: Lista de dicionários contendo as perguntas estratégicas e as instruções SQL associadas.

    Returns:
        None.

    Raises:
        KeyError: Se as chaves pergunta ou query não estiverem presentes em algum dos dicionários da lista.
    '''
    for consulta in lista_de_consultas:

        if not consulta["query"].strip():
            continue

        resultado_consulta = obter_dados_do_banco(consulta['query'])

        exibir_resultados(consulta=consulta,
                          resultado_consulta=resultado_consulta)


def mostrar_consulta_individual(lista_de_consultas: list[dict[str, str]], numero_da_consulta: int) -> None:
    '''
    Executa e exibe uma consulta estratégica selecionada pelo número.

    Args:
        lista_de_consultas: Lista de dicionários contendo as perguntas estratégicas e as instruções SQL associadas.
        numero_da_consulta: Número da consulta que será executada, considerando a numeração iniciada em 1.

    Returns:
        None.

    Raises:
        KeyError: Se as chaves pergunta ou query não estiverem presentes no dicionário da consulta selecionada.
    '''

    if numero_da_consulta < 1 or numero_da_consulta > len(lista_de_consultas):
        print(
            f"Entrada inválida: Escolha um numero entre 1 e {len(lista_de_consultas)}.")
        return

    consulta = lista_de_consultas[numero_da_consulta - 1]

    if not consulta['query'].strip():
        print("Esta consulta ainda não foi definida")
        return

    resultado_consulta = obter_dados_do_banco(consulta['query'])

    exibir_resultados(consulta=consulta, resultado_consulta=resultado_consulta)


consultas_estrategicas = []

# Consulta estratégica 1
primeira_pergunta = "Qual usina apresentou a maior geração total estimada a partir dos registros diários durante o período analisado?"
primeira_query = """
    WITH geracao_diaria_por_inversor AS (
        SELECT
            plant_code,
            inverter_code,
            DATE(date_time) AS data_medicao,
            MAX(daily_yield) AS geracao_diaria
        FROM generation_measurements
        GROUP BY
            plant_code,
            inverter_code,
            DATE(date_time)
    )
    SELECT
        plant_code,
        ROUND(SUM(geracao_diaria), 2) AS energia_total_gerada
    FROM geracao_diaria_por_inversor
    GROUP BY
        plant_code
    ORDER BY
        energia_total_gerada DESC;
"""
consultas_estrategicas.append(
    {
        'pergunta': primeira_pergunta,
        'query': primeira_query
    }
)

# Consulta estratégica 2
segunda_pergunta = "Quais inversores apresentaram a maior geração acumulada a partir dos registros diários durante o período analisado?"
segunda_query = """
    WITH geracao_diaria_por_inversor AS (
        SELECT
            plant_code,
            inverter_code,
            DATE(date_time) AS data_medicao,
            MAX(daily_yield) AS geracao_diaria
        FROM generation_measurements
        GROUP BY
            plant_code,
            inverter_code,
            DATE(date_time)
    )
    SELECT
        plant_code,
        inverter_code,
        ROUND(SUM(geracao_diaria), 2) AS energia_gerada
    FROM geracao_diaria_por_inversor
    GROUP BY
        plant_code,
        inverter_code
    ORDER BY
        plant_code,
        energia_gerada DESC;
"""
consultas_estrategicas.append(
    {
        'pergunta': segunda_pergunta,
        'query': segunda_query
    }
)

# Consulta estratégica 3
terceira_pergunta = "Em qual dia cada usina apresentou sua maior geração de energia?"
terceira_query = """
    WITH geracao_diaria_por_inversor AS (
        SELECT
            plant_code,
            inverter_code,
            DATE(date_time) AS data_medicao,
            MAX(daily_yield) AS geracao_diaria
        FROM generation_measurements
        GROUP BY
            plant_code,
            inverter_code,
            DATE(date_time)
    ),
    geracao_diaria_por_usina AS (
        SELECT
            plant_code,
            data_medicao,
            SUM(geracao_diaria) AS geracao_total_diaria
        FROM geracao_diaria_por_inversor
        GROUP BY 
            plant_code,
            data_medicao
    ),
    classificacao_diaria AS (
        SELECT
            plant_code,
            data_medicao,
            geracao_total_diaria,
            ROW_NUMBER() OVER (
                PARTITION BY plant_code
                ORDER BY geracao_total_diaria DESC
            ) AS posicao
        FROM geracao_diaria_por_usina
    )
    SELECT 
        plant_code,
        data_medicao,
        ROUND(geracao_total_diaria, 2) AS geracao_total_diaria
    FROM classificacao_diaria
    WHERE posicao = 1
    ORDER BY plant_code;
"""
consultas_estrategicas.append(
    {
        'pergunta': terceira_pergunta,
        'query': terceira_query
    }
)

# Consulta estratégica 4
quarta_pergunta = "Quais foram as condições climáticas médias registradas em cada usina?"
quarta_query = """
    SELECT
        plant_code,
        ROUND(AVG(ambient_temperature), 2) AS temperatura_ambiente_media,
        ROUND(AVG(module_temperature), 2) AS temperatura_modulo_media,
        ROUND(AVG(irradiation), 4) AS irradiacao_media,
        ROUND(MAX(ambient_temperature), 2) AS maior_temperatura_ambiente,
        ROUND(MAX(module_temperature), 2) AS maior_temperatura_modulo,
        ROUND(MAX(irradiation), 4) AS maior_irradiacao
    FROM weather_measurements
    GROUP BY plant_code
    ORDER BY plant_code;
"""
consultas_estrategicas.append(
    {
        'pergunta': quarta_pergunta,
        'query': quarta_query
    }
)

# Consulta estratégica 5
quinta_pergunta = "Como a geração diária de cada usina se relacionou com a temperatura e a irradiação médias?"
quinta_query = """
    WITH geracao_diaria_por_inversor AS (
        SELECT
            plant_code,
            plant_id,
            inverter_code,
            DATE(date_time) AS data_medicao,
            MAX(daily_yield) AS geracao_diaria
    FROM generation_measurements
    GROUP BY
        plant_code,
        plant_id,
        inverter_code,
        DATE(date_time)
    ),
    geracao_diaria_por_usina AS (
        SELECT
            plant_code,
            plant_id,
            data_medicao,
            SUM(geracao_diaria) AS geracao_total_diaria
    FROM geracao_diaria_por_inversor
    GROUP BY
        plant_code,
        plant_id,
        data_medicao
    ),
    clima_diario_por_usina AS (
        SELECT
        plant_code,
        plant_id,
        DATE(date_time) AS data_medicao,
        AVG(ambient_temperature) AS temperatura_ambiente_media,
        AVG(module_temperature) AS temperatura_modulo_media,
        AVG(irradiation) AS irradiacao_media
    FROM weather_measurements
    GROUP BY
        plant_code,
        plant_id,
        DATE(date_time)
    )
    SELECT
        g.plant_code,
        g.data_medicao,
        ROUND(g.geracao_total_diaria, 2) AS geracao_total_diaria,
        ROUND(c.temperatura_ambiente_media, 2) AS temperatura_ambiente_media,
        ROUND(c.temperatura_modulo_media, 2) AS temperatura_modulo_media,
        ROUND(c.irradiacao_media, 4) AS irradiacao_media
    FROM geracao_diaria_por_usina AS g
    INNER JOIN clima_diario_por_usina AS c
        ON c.plant_code = g.plant_code
        AND c.plant_id = g.plant_id
        AND c.data_medicao = g.data_medicao
    ORDER BY g.plant_code, g.data_medicao;
"""
consultas_estrategicas.append(
    {
        'pergunta': quinta_pergunta,
        'query': quinta_query
    }
)


def main() -> None:
    '''Executa a exibição das consultas individualmente ou do relatório completo com todas as as consultas estratégicas.'''

    mostrar_relatorio_completo(lista_de_consultas=consultas_estrategicas)
    # mostrar_consulta_individual(
    #     lista_de_consultas=consultas_estrategicas, numero_da_consulta=2)


if __name__ == "__main__":
    main()