# Automação inteligente sem usar AI

Projeto de Bi cujo objetivo é tratar (ETL) os arquivos exportados do Salesforce de forma rápida e eficiente
fazendo depois cruzamentos e análises onde os resultados são disponibilizados de forma executiva por meio de htmls compartilháveis e editáveis.

* Todos os dados são 100% fictícios, gerados por código sem relação com empresa real mas foi criado e inspirado a partir do Projeto de Automação inteligente com Python em uma empresa que atuo.

O que o projeto mostra

**Dashboard Executivo**: KPIs, matriz de situação (só em Pedidos, em ambos,
só em Faturas) e quebras por unidade, categoria e status.

**Dados Cruzados**: tabela com filtros, edição de células e exportação para CSV/Excel.

### Demo online:

https://byvanessapagano.github.io/dashboard-executivo-bi/saida/dados_cruzados.html
https://byvanessapagano.github.io/dashboard-executivo-bi/saida/dashboard_executivo.html

## Como Desenvolvi

- **Python** (somente biblioteca padrão) para gerar os dados fictícios
- **HTML, CSS e JavaScript** para a interface interativa
- Semente fixa (`seed=2026`): o resultado é sempre reproduzível
- Conferência automática para garantir que nenhum termo do projeto original permaneceu nos arquivos


## Habilidades demonstradas

Análise de dados / Cruzamento de bases (reconciliação) / Indicadores (KPIs) 
Visualização / Automação com Python / Anonimização de dados


## Sobre o código

O script é incluído para mostrar a lógica de geração dos dados.

## Sobre o código

O script `codigo/gerar_exemplo_ficticio.py` gera as duas bases fictícias
(Pedidos e Faturas), calcula a reconciliação entre elas e os indicadores que alimentam o dashboard. Roda só com a biblioteca padrão do Python:

    python codigo/gerar_exemplo_ficticio.py

Os HTMLs prontos, já com esses dados, estão na pasta `saida/`.

## Autora

Vanessa Pagano · [LinkedIn](https://www.linkedin.com/in/vanessa-pagano/)
