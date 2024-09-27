# Câmara dos Deputados - Aplicação Web

Este projeto consiste na construção de uma aplicação web interativa utilizando o framework [Streamlit](https://streamlit.io), com dados extraídos da [API Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/). O principal objetivo da aplicação é permitir o acompanhamento detalhado dos gastos de cada partido e parlamentar, com a flexibilidade de aplicar filtros por ano, partido e deputado.

## Funcionalidades

- **Visualização Dinâmica de Gastos**: Acompanhe os gastos por partido e/ou parlamentar com gráficos interativos.
- **Filtros Inteligentes**: Ao selecionar um partido, o filtro de deputados exibe automaticamente apenas os parlamentares pertencentes ao partido escolhido, proporcionando uma experiência de navegação mais ágil e precisa.
- **Gráficos Interativos**: Os gráficos foram criados utilizando a biblioteca [Plotly Express](https://plotly.com/python/plotly-express/), garantindo máxima interatividade e visualização rica em detalhes.
- **Personalização de Estilo**: Incluímos um arquivo CSS para permitir a customização da paleta de cores, adaptando o design da aplicação às preferências do usuário.

## Análise de Dados

Todo o processo de extração, análise, formatação e exploração dos dados (EDA - Análise Exploratória de Dados) foi realizado no notebook `Analise_cdf.ipynb`, que está disponível neste repositório. Nele, você pode acompanhar cada etapa do tratamento dos dados e entender as principais decisões que guiaram o desenvolvimento da aplicação.

## Estrutura do Projeto

- `app.py`: Código principal da aplicação Streamlit.
- `Analise_cdf.ipynb`: Notebook com a análise de dados, limpeza, transformação e criação de insights.
- `style.css`: Arquivo CSS que permite a personalização da paleta de cores da aplicação.
- `requirements.txt`: Lista das dependências necessárias para a execução do projeto.

## Fonte de Dados

- `API Dados Abertos da Câmara dos Deputados`: Todos os dados utilizados nesta aplicação foram obtidos através da API oficial da Câmara dos Deputados. Para mais informações, consulte a documentação oficial em https://dadosabertos.camara.leg.br/.