# Relatório de Machine Learning — SmartRoad Preditiva

**FIAP · Global Solution 2026.2 · CitizenTech · Inteligência Artificial & Machine Learning**
**Equipe:** Gustavo Viega Lopes Martins (RM555885), Gustavo Yuji Osugi (RM555034), Kaio Drago Lima Souza (RM556095), Otávio Santos de Lima Ferrão (RM556452) e Vitor Rivas Cardoso (RM556404)
**Notebook:** [`ml/smartroad_preditiva.ipynb`](ml/smartroad_preditiva.ipynb) · **Dados:** [`ml/dados/README.md`](ml/dados/README.md)

## 1. Problema e dados reais

O **SmartRoad** é o app em que o morador de São Paulo registra buracos, bueiros quebrados e calçadas danificadas e acompanha o andamento. Depois de registrar, a primeira dúvida de quem usa é *"isso vai demorar?"*, e o app não tem como responder. O indicador de impacto da nossa Ficha é justamente o tempo entre o registro e a conclusão.

**Pergunta de ML:** no momento em que uma ocorrência é registrada, dá para prever se ela vai **demorar mais de 30 dias para ser finalizada**? É uma classificação binária supervisionada.

**Dados:** solicitações reais do **SP156**, o canal oficial de pedidos de serviço da Prefeitura de São Paulo.

| | |
| --- | --- |
| Fonte | Portal de Dados Abertos da Prefeitura de São Paulo, conjunto "Dados do SP156 - Solicitações" |
| Link | https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156 |
| Período | pedidos abertos de 01/07/2025 a 30/06/2026 (4 arquivos trimestrais, republicados em 10/08/2026) |
| Volume | 2.023.061 solicitações nos arquivos originais; 189.467 nos 9 serviços que correspondem ao app |
| Licença | Creative Commons CC0 |

Ficamos com os serviços de tapa-buraco, bueiros e galerias, e calçadas e guias. O tipo "Iluminação" do app ficou de fora, porque o SP156 não traz serviço de iluminação pública nesse período.

## 2. Escolha do modelo

Escolhemos o **XGBoost** (`XGBClassifier`), entre as opções do enunciado, por quatro motivos:

- Os dados são uma **tabela** com variáveis categóricas e numéricas. Modelos de árvores costumam ser os melhores nesse formato e não exigem normalização.
- O efeito da região depende do serviço e da época. Árvores capturam essas **combinações** sozinhas.
- Temos a resposta de cada pedido, então o problema é supervisionado: KMeans + PCA não usa o rótulo. Uma LSTM precisa de sequências longas, e aqui cada pedido é uma linha independente. Uma MLP exigiria normalização e mais ajuste.
- Em relação ao Random Forest, o XGBoost tem controles diretos de complexidade, que usamos para estudar o overfitting, e devolve uma **probabilidade**, que é o que o app mostra ao cidadão.

## 3. Preparação e divisão treino/teste

**Limpeza** (188.136 linhas mantidas, 99,3% do recorte): removemos 1.225 pedidos cancelados pelo cidadão, 26 finalizados sem data, 20 de um canal que não consta no dicionário (RESOLUCAO) e 60 com coordenadas fora da cidade. Duas subprefeituras mudaram de nome no meio do período e foram unificadas.

**Alvo:** `demora = 1` quando o pedido não foi finalizado em até 30 dias, incluindo os que ainda estavam abertos. O limite de 30 dias foi escolhido porque todo pedido do recorte foi observado por mais de 30 dias antes da extração. Assim o alvo é conhecido para 100% das linhas, e não precisamos descartar os pedidos ainda abertos, que são os mais demorados. No total, 36,6% dos pedidos demoram.

**Entradas** (só o que o app sabe na hora do registro): serviço, canal, subprefeitura, latitude, longitude, mês e dia da semana. As categóricas passaram por *one-hot encoding* (50 colunas no total). Deixamos de fora o status, a data de finalização e o órgão responsável, que são informações de depois da abertura e causariam vazamento.

**Divisão por data, e não por sorteio:** treino com os pedidos de 01/07/2025 a 30/04/2026 (161.677; 85,9%) e teste com os de 01/05 a 30/06/2026 (26.459; 14,1%). A taxa de demora mudou muito ao longo do ano, e o modelo será usado para prever pedidos futuros. Por isso ele precisa ser testado em meses que não viu.

![Taxa de demora por mês de abertura](ml/figuras/03_demora_por_mes.png)

## 4. Treino com diferentes hiperparâmetros

Testamos **18 combinações de 3 hiperparâmetros** com `GridSearchCV`: `max_depth` (3, 6, 9), `learning_rate` (0,03; 0,1; 0,3) e `n_estimators` (100, 300). A validação cruzada foi feita **só no treino**, com `TimeSeriesSplit` de 4 divisões, que sempre treina em datas anteriores e valida em datas posteriores. A métrica da busca foi a AUC-ROC.

A tabela e o gráfico das 18 combinações estão na Seção 5 do notebook. A melhor combinação foi `max_depth=9`, `learning_rate=0.1` e `n_estimators=100` (AUC de 0,800 na validação). As 9 primeiras ficaram entre 0,796 e 0,800, o que é um empate diante do desvio de 0,04 a 0,05 entre as divisões. A combinação mais complexa chegou a 0,992 no treino e ficou entre as piores na validação (0,786): decorou o treino. A mais simples teve a menor distância entre treino e validação, mas a pior validação (0,782): aprendeu de menos.

## 5. Resultados em treino e teste

| Métrica | Treino | Teste | Diferença |
| --- | ---: | ---: | ---: |
| AUC-ROC | 0,909 | 0,767 | 0,142 |
| Acurácia | 0,829 | 0,706 | 0,123 |
| Acurácia balanceada | 0,803 | 0,681 | 0,122 |
| Precisão (classe "demora") | 0,791 | 0,704 | 0,088 |
| Recall (classe "demora") | 0,710 | 0,521 | 0,189 |
| F1 (classe "demora") | 0,749 | 0,599 | 0,150 |
| *Linha de base: sempre "não demora" (acurácia)* | *0,642* | *0,579* | |

![Métricas de treino e teste lado a lado](ml/figuras/05_metricas_treino_teste.png)

**O modelo é útil fora do treino:** no teste, a acurácia fica 12,7 pontos acima da linha de base, e a acurácia balanceada sobe de 0,500 para 0,681.

**Há overfitting.** A AUC cai 0,14 do treino para o teste. Vemos duas causas: árvores profundas guardam detalhes do treino, e o ritmo da cidade mudou entre os períodos (35,8% de demora no treino, 42,1% no teste). A validação cruzada (0,800) antecipou o teste (0,767) muito melhor do que a nota do treino (0,909).

**A divisão por sorteio enfeitaria a nota.** Com os mesmos hiperparâmetros e divisão aleatória, a AUC de teste seria 0,878. O modelo "conheceria" o ritmo de cada época, o que o app nunca terá ao prever um pedido novo.

**Pontos fracos.** O recall é de 0,52: com corte em 50%, o modelo deixa passar quase metade das demoras. O mês responde por 21% do ganho, mas com 12 meses de dados ele separa principalmente o período rápido (2025) do lento (2026), e não uma sazonalidade aprendida. O serviço responde por 51% do ganho e a região por 26%.

**As probabilidades são confiáveis.** Em todas as faixas de chance, o previsto fica a menos de 5 pontos percentuais do que aconteceu no teste.

## 6. Conclusão: o que isso significa para o cidadão

**Sim, em parte, dá para prever.** Só com o que o SmartRoad sabe no registro, o modelo estima a chance de demora melhor do que o acaso e do que a linha de base. Ele não acerta caso a caso. É uma estimativa.

- **Expectativa honesta já no registro.** Hoje o cidadão só vê "Recebida". Com o modelo, o app pode dizer o que costuma acontecer com pedidos parecidos. No teste, a mensagem "costumam ser finalizados em até 30 dias" apareceria em 44% dos pedidos, e 77% deles foram finalizados no prazo. A mensagem "costumam passar de 30 dias" apareceria em 20%, e 81% deles de fato passaram. Nos 36% restantes a chance fica perto de meio a meio, e o app deve dizer isso com clareza.
- **O tipo de problema pesa mais que tudo.** No teste, 24% dos pedidos de bueiro, 36% dos de buraco e 69% dos de calçada passaram de 30 dias. Quem mais depende de calçada em bom estado (idosos, pessoas com deficiência, quem anda com carrinho de bebê) é quem mais espera.
- **O endereço também pesa.** No período analisado, a taxa de demora foi de 22% em Perus e Ermelino Matarazzo e de 50% na Sé. Mostrar isso ajuda moradores e associações de bairro a cobrar com dados (ODS 11 e ODS 10).

**Limites.** "Finalizada" no SP156 indica que o protocolo foi encerrado, e não que o reparo foi feito. O modelo aprendeu com 12 meses em que o ritmo mudou, então precisa ser retreinado com frequência e reavaliado sempre em meses futuros.

**Próximos passos.** Usar dois ou mais anos de dados, juntar a chuva diária do INMET e servir a previsão pelo backend para a tela de detalhe da ocorrência.
