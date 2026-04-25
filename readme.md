DOCUMENTAÇÃO DO PROJETO INTEGRADOR – DESENVOLVIMENTO LOW CODE EM CIÊNCIA DE DADOS

Tema do Projeto: Dashboard Estratégico de Vendas para Marketing

Integrantes:

•	Alison Moretto Dias 

•	Caetano Araujo Mina 

•	Felipe Santos de Alencar 

•	Iago Faria dos Santos 

•	Ivan Silva de Arruda Campos 

•	Leandro Morais dos Santos 

•	Marcio Ricardo Hatzlhoffer Correia Filho 


-------------------------------------------------------------------------

Estrutura inicial do Projeto:

O repositório foi criado para centralizar o desenvolvimento do projeto. Todos os integrantes foram adicionados como colaboradores e a estrutura inicial será organizada em pastas para dados, análise exploratória, código do dashboard e documentação.
Este projeto segue uma abordagem de análise orientada a negócio, onde os indicadores foram definidos com base nas necessidades da equipe de marketing.

-------------------------------------------------------------------------

Contexto do Projeto

O crescimento do comércio eletrônico tem gerado grandes volumes de dados relacionados a vendas, comportamento de clientes e desempenho de produtos. Nesse cenário, a análise desses dados se torna essencial para que empresas possam compreender melhor seu público, identificar padrões de consumo e tomar decisões mais estratégicas.
Além disso, equipes de marketing utilizam essas informações para planejar campanhas, definir estratégias de precificação e direcionar esforços para maximizar resultados. Dessa forma, a utilização de ferramentas de análise de dados e visualização se torna fundamental para transformar dados brutos em informações úteis para o negócio.

-------------------------------------------------------------------------

Problema de Negócio (Business Understanding)

Diante do grande volume de dados gerados no contexto de e-commerce, muitas empresas enfrentam dificuldades em transformar esses dados em informações úteis para a tomada de decisão.

A ausência de uma visualização clara e organizada dos dados pode dificultar a identificação de padrões de consumo, desempenho de produtos e oportunidades de melhoria nas vendas.

Nesse sentido, surge o desafio de analisar esses dados de forma estruturada e apresentá-los de maneira acessível, pois sem essa análise, decisões de marketing podem ser tomadas sem base analítica, reduzindo eficiência operacional e possivelmente acarretando gastos desnecessários.

Portanto, chegamos à seguinte pergunta problema: Como transformar dados de vendas de um e-commerce em informações úteis e acessíveis para apoiar a tomada de decisão da equipe de marketing?

-------------------------------------------------------------------------

Objetivo do Projeto:

O objetivo deste projeto é desenvolver um dashboard interativo que permita analisar dados de vendas e gerar insights estratégicos, apoiando a tomada de decisão da equipe de marketing.

-------------------------------------------------------------------------

Base de Dados:

1.	Base de dados escolhida:	 https://www.kaggle.com/datasets/aliiihussain/amazon-sales-dataset

2.	Descrição da base de dados:
Para o desenvolvimento deste projeto, foi utilizada uma base de dados de vendas de e-commerce disponibilizada na plataforma Kaggle – plataforma amplamente utilizada para projetos de análise de dados.
O dataset contém registros de transações de vendas da Amazon no período de 2022 - 2023, incluindo informações sobre id do pedido, data da venda, categorias de produto, valor unitário, quantidade, região da compra, método de pagamento e avaliação do produto.
A partir da análise desses dados será desenvolvido um dashboard interativo em Python permitindo identificar padrões de vendas, comportamento de compra e oportunidades de otimização para maior assertividade das estratégias de marketing

3.	Motivo da escolha:
A base foi escolhida por conter informações sólidas e relevantes para análise de comportamento de consumo e desempenho de vendas, permitindo a geração de insights estratégicos para equipes de marketing e gestão comercial.

-------------------------------------------------------------------------

Planejamento do Projeto

O projeto está sendo desenvolvido seguindo um fluxo estruturado de etapas, conforme descrito abaixo:

•	Definição do tema

•	Entendimento de negócio

•	Definição dos objetivos do projeto

•	Escolha da base de dados

•	Limpeza e tratamento dos dados

•	Análise exploratória dos dados

•	Definição das métricas e indicadores

•	Transformação dos dados

•	Desenvolvimento das visualizações

•	Construção do dashboard final

-------------------------------------------------------------------------

Cronograma
O cronograma do projeto foi definido de acordo com o prazo estabelecido pela disciplina, distribuindo as atividades ao longo das semanas de desenvolvimento e com foco no objeto de entrega dessa primeira etapa:

•	Semana 1: Definição do tema do projeto e do problema de negócio

•	Semana 2: Criação do repositório no Github e escolha da base de dados

•	Semana 3: Definição dos tratamentos, métricas e visualizações pretendidas

•	Semana 4: Entrega da documentação da primeira etapa

-------------------------------------------------------------------------

Divisão de tarefas

Integrante	          Responsabilidade

Felipe :	      Criação e organização do repositório Github

Iago :	         Organização da documentação e tarefas

Leandro	:         Exploração e tratamentos iniciais da base de dados

Demais membros :  Definição das métricas, visualizações e tratamentos

-------------------------------------------------------------------------

Transformações que pretendemos realizar

As transformações foram definidas com base nas necessidades das métricas e visualizações propostas para o dashboard. Entre as principais transformações previstas estão:

•	Tratamento de valores nulos

•	Padronização de colunas e textos 

•	Conversão de tipos de dados

•	Remoção de duplicatas

•	Agrupamento de dados

•	Criação de novas colunas (feature engineering)

•	Cálculo de métricas derivadas (ex: ticket médio) 

-------------------------------------------------------------------------

Métricas e Indicadores pretendidos
 

1.	Receita total 
2.	Número total de pedidos 
3.	Ticket médio 
4.	Avaliação média dos produtos 
5.	Vendas por categoria 
6.	Vendas por região 
7.	Evolução das vendas ao longo do tempo
8.	Top produtos mais vendidos

-------------------------------------------------------------------------

Visualizações pretendidas

Os indicadores principais serão apresentados em formato de KPIs, enquanto as análises comparativas serão exibidas por meio de gráficos interativos.

Métrica ------------------- Tipo de gráfico

Receita total ------------- KPI (número grande)

Número de pedidos	----- KPI

Ticket médio ------------- KPI

Avaliação média	--------- KPI

Vendas por categoria ---- Gráfico de barras

Vendas por região	------- Gráfico de pizza

Evolução das vendas	----- Gráfico de linha

Top produtos ------------- Ranking (barra horizontal)

-------------------------------------------------------------------------

Ideia inicial do dashboard

O dashboard será dividido em painéis interativos que permitirão, através de filtros, gráficos e relatórios, visualizar indicadores gerais de vendas, desempenho por categoria de produto, distribuição geográfica das vendas e tendências ao longo do tempo. O objetivo é fornecer uma visão clara e rápida dos principais indicadores para apoiar decisões da equipe de marketing.


Painel 1 — Visão Geral

•	Receita total 
•	Número de pedidos 
•	Ticket médio 
•	Avaliação média 

Painel 2 — Desempenho de vendas

•	Vendas por categoria 
•	Top produtos 

Painel 3 — Análise geográfica

•	Vendas por região 

Painel 4 — Tendência temporal

•	Evolução das vendas ao longo do tempo

