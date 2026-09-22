<h1 align="center"> ☀ Análise de Geração de Energia Solar ☀</h1>

<h2 align="center"> Objetivo </h2>

> Analisar os dados de geração de duas usinas solares, investigando seu comportamento ao longo do tempo, a relação entre fatores ambientas, como temperatura e irradiação solar, e a produção de energia e possíveis diferenças de desempenho entre usinas e inversores.

---

<h2 align="center"> Pergunta central </h2>

> Como a geração de energia das duas usinas variou durante o período analisado e como ela se relacionou com as condições ambientais e o desempenho dos inversores?

---

---

<h2 align="center"> Parte 1 </h2>

> A primeira etapa contém:
> - banco de dados MySQL
> - integração entre Python e MySQL
> - cinco consultas estratégicas
> - análise estatística com Pandas

---


<h2 align="center"> Obtenção dos dados </h2>

Os dados estão disponíveis no kaggle: [Solar Power Generation Data](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data)

Consulte o arquivo `fontes.txt` para mais detalhes.

---

<h2 align="center"> Estrutura </h2>

``` 
analiseEnergiaSolar/
├─── README.md datasets
├─── fontes.txt
├─── requirements.txt
├─── .gitignore
│
├─── notebooks/
│    └── 01-inspecao-inicial.ipynb
│
├─── src/
│    └── integracao_mysql.py
│    └── analise-estatistica.py
│
└─── sql/
     └── criacao_banco.sql

```

- <b>README.md</b>: informações gerais e documentação do projeto.
- <b>fontes.txt</b>: informações específicas sobre a fonte dos dados e como utilizá-la.
- <b>requirements.txt</b>: Arquivo que armazena as dependências do projeto.
- <b>src/</b>: diretório para armazenar os scripts desenvolvidos em Python para integração com o banco de dados e para analise estatística.
- <b>src/</b>: diretório para armazenar os arquivos contendo os comandos SQL para a criação da estrutura do banco de dados.
- <b>notebooks</b>: diretório parar armazenar os notebooks desenvolvidos para inspecionar os dados.


---

<h2 align="center"> Tecnologias e ferramentas </h2>

    - Python
    - Pandas
    - Numpy
    - Matplotlib
    - Jupyter Notebook
    - MYSQL/SQL


---

<h2 align="center"> Grupo </h2>

<div align="center">
    <h3>Phellipe Lisbôa | <a href="https://www.linkedin.com/in/phellipe-lisboa/">Linkedin</a></h3>
    <h3>Jorge | <a href="https://www.linkedin.com/in/jorge-alberto-santos-da-silva-b8547457/">Linkedin</a></h3>
    <h3>Elisângela | <a href="https://www.linkedin.com/in/elisangela/">Linkedin</a></h3>
</div>

---