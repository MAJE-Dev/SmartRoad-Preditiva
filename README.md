🛠️ Modelo Preditivo baseado no nosso app SmartRoad: https://github.com/MAJE-Dev/SmartRoad

## Integrantes

| Nome | RM |
| --- | --- |
| Gustavo Viega Lopes Martins | RM555885 |
| Gustavo Yuji Osugi | RM555034 |
| Kaio Drago Lima Souza | RM556095 |
| Otávio Santos de Lima Ferrão | RM556452 |
| Vitor Rivas Cardoso | RM556404 |

# SmartRoad Preditiva

O modelo responde a uma pergunta que o app ainda não consegue responder ao morador: **"a ocorrência que acabei de registrar vai demorar mais de 30 dias para ser finalizada?"**

## Ficha da CitizenTech

| Campo | Descrição |
| --- | --- |
| **Nome da CitizenTech** | SmartRoad |
| **Cidade e bairro** | São Paulo (SP). O modelo cobre as 32 subprefeituras da cidade. |
| **Cidadão beneficiado** | Moradores que andam, dirigem ou pedalam pelas ruas, em especial quem mais depende de calçada e rua em bom estado: idosos, pessoas com deficiência e quem anda com carrinho de bebê. |
| **Problema, em uma frase** | Buracos, bueiros quebrados e calçadas danificadas demoram a ser resolvidos, e o morador não tem um jeito simples de avisar nem de saber quanto tempo o reparo deve levar. |
| **Como funciona** | O cidadão registra o problema no app em menos de 1 minuto e acompanha o andamento. Com este modelo, o app passa a informar, já no registro, a chance de o pedido demorar mais de 30 dias. |
| **O que cada parte faz** | **App mobile** ([MAJE-Dev/SmartRoad](https://github.com/MAJE-Dev/SmartRoad)): consultar, registrar e acompanhar ocorrências. **Machine Learning (este repositório):** prever a chance de demora a partir dos dados reais do SP156. |
| **Link do repositório** | https://github.com/MAJE-Dev/SmartRoad-Preditiva (ML) · https://github.com/MAJE-Dev/SmartRoad (app) |
| **Indicador de impacto** | Tempo entre o registro e a conclusão do reparo. Aqui ele é medido como a porcentagem de pedidos finalizados em até 30 dias, por tipo de serviço e por subprefeitura. |
| **ODS conectados** | ODS 11 (cidades e comunidades sustentáveis), ODS 9 (infraestrutura) e ODS 10 (redução das desigualdades: o tempo de espera muda conforme a região). |

## ODS e metas

| ODS | Meta | Como o projeto contribui |
| --- | --- | --- |
| **ODS 9** (indústria, inovação e infraestrutura) | 9.1: infraestrutura de qualidade, confiável e resiliente | O modelo prevê quais pedidos de reparo de buraco, bueiro e calçada tendem a passar de 30 dias. Isso mostra onde a manutenção da infraestrutura viária está atrasando e ajuda a Prefeitura a priorizar esses casos. |
| **ODS 11** (cidades e comunidades sustentáveis) | 11.2: sistemas de transporte seguros e acessíveis. 11.3: urbanização inclusiva e gestão participativa | Ruas e calçadas em bom estado dão mais segurança a quem anda, dirige ou pedala, em especial idosos e pessoas com deficiência. Ao avisar o cidadão, já no registro, a chance de demora, o app torna o acompanhamento do reparo mais transparente e incentiva a participação. |
| **ODS 10** (redução das desigualdades) | 10.2: inclusão social, econômica e política de todos | Nos dois anos de dados analisados, a taxa de demora foi de 19% no Jabaquara e de 48% na Sé. Tornar essa diferença visível permite que moradores e associações de bairro cobrem um atendimento igual entre as regiões. |

O indicador de impacto (porcentagem de pedidos finalizados em até 30 dias, por tipo de serviço e por subprefeitura) é o que acompanha essas contribuições ao longo do tempo.

## Resumo do trabalho

| | |
| --- | --- |
| **Pergunta de ML** | Classificação binária: a solicitação vai demorar mais de 30 dias para ser finalizada? |
| **Dados** | 384.139 solicitações reais do [SP156](https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156) (Prefeitura de São Paulo), abertas de 01/07/2024 a 30/06/2026 (2 anos corridos), dos serviços de tapa-buraco, bueiros e calçadas |
| **Série temporal** | A demora é uma série que muda de regime (de ~25% para ~50% em jan/2026). O modelo recebe, a cada pedido, séries diárias do serviço e da subprefeitura: fila em aberto, fila atrasada, volume dos últimos 7/30 dias, ritmo de finalização e taxa de demora recente (14 indicadores, só com o que já havia acontecido antes do registro; há teste anti-vazamento no notebook) |
| **Modelo** | XGBoost (`XGBClassifier`) |
| **Divisão** | por data, com intervalo de 30 dias: treino de 01/07/2024 a 31/03/2026 (342.311 pedidos), teste de 01/05 a 30/06/2026 (26.459 pedidos) |
| **Validação** | `TimeSeriesSplit` com intervalo de 30 dias no treino e **walk-forward de 12 meses** (retreino a cada mês, jul/2025 a jun/2026) |
| **Hiperparâmetros** | 18 combinações de `max_depth`, `learning_rate` e `n_estimators`, com validação cruzada temporal só no treino (melhor: profundidade 6, passo 0,03, 300 árvores) |
| **Resultado no teste** | AUC-ROC 0,72 · acurácia 0,68 (linha de base: 0,58) · F1 da classe "demora" 0,56 |
| **Resultado no treino** | AUC-ROC 0,87 · acurácia 0,80 · F1 0,68 (há overfitting, discutido no relatório) |
| **A série temporal ajuda?** | Walk-forward de 12 meses: AUC média 0,794 com série temporal, 0,782 sem ela e 0,777 com a previsão ingênua (persistência). Brier 0,169 contra 0,177, e o erro de nível da chance prevista cai de 10,9 para 6,6 pontos percentuais. O ganho é modesto e some logo após o salto de regime de jan/2026 |

## Entregas

| Entrega | Onde está |
| --- | --- |
| Notebook executado | [`ml/smartroad_preditiva.ipynb`](ml/smartroad_preditiva.ipynb) |
| Documentação dos dados (fonte, link e período) | [`ml/dados/README.md`](ml/dados/README.md) |
| Dependências | [`ml/requirements.txt`](ml/requirements.txt) |
| Relatório | [`RELATORIO_ML.md`](RELATORIO_ML.md) |
| Registro dos prompts de IA | [`prompts.md`](prompts.md) |
| Vídeo (até 5 min, YouTube não listado) | **PREENCHER com o link** |

## Estrutura

```
README.md              esta página, com a Ficha da CitizenTech
RELATORIO_ML.md        relatório, do problema à conclusão
prompts.md             prompts de IA usados no trabalho
ml/
  smartroad_preditiva.ipynb   notebook executado (dados, preparação, treino, resultados, conclusão)
  requirements.txt            bibliotecas
  dados/
    README.md                 fonte, link, período, colunas e cuidados
    preparar_dados.py         baixa os arquivos do SP156 e gera o recorte
    sp156_zeladoria_jul2024_jun2026.csv.gz   recorte usado no notebook (6 MB)
  figuras/                    gráficos gerados pelo notebook
```

## Como rodar

Precisa de Python 3.10 ou mais novo.

```bash
git clone https://github.com/MAJE-Dev/SmartRoad-Preditiva.git
```

```bash
cd SmartRoad-Preditiva/ml
```

```bash
pip install -r requirements.txt
```

```bash
jupyter notebook smartroad_preditiva.ipynb
```

O notebook lê o recorte que já está em `ml/dados/` e roda inteiro em cerca de 1 a 2 minutos. No Google Colab, basta abrir o arquivo `.ipynb`: sem a pasta `dados/`, ele busca o mesmo recorte no GitHub (isso exige o repositório público e o arquivo na branch `main`).

Para refazer o recorte a partir dos arquivos originais da Prefeitura (cerca de 430 MB), veja [`ml/dados/README.md`](ml/dados/README.md).
