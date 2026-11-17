# Prompts de IA usados neste trabalho

O briefing da Global Solution permite usar IA como copiloto e pede o registro dos prompts. Este arquivo lista o que foi pedido, o que a IA fez e o que a equipe precisa conferir.

**Ferramenta:** Claude Code (Anthropic), em sessão na nuvem com acesso a este repositório.
**Datas:** 14/11/2026 (Prompt 1) e 17/11/2026 (Prompts 2 e 3).

## Prompt 1 — construção da entrega de IA & Machine Learning

Arquivos anexados ao prompt: o briefing `2nd GS 2026.pdf` e o notebook `GS - Nemeczao.ipynb` (nosso trabalho do primeiro semestre, usado como referência de estilo).

> Leia `2nd GS 2026.pdf` e encontre a materia "Inteligência Artificial & Machine Learning" la perto da pagina 31 do pdf, eh esta materia a que vamos fazer!!
>
> Como modelo do tipo de trabalho que eu estava acostumado a fazer na metade do ano tenho esse `GS - Nemeczao.ipynb`, caso seja util
>
> Objetivo: Realizar a tarefa em "Inteligência Artificial & Machine Learning" no pdf anexado, como envolve um repositorio github ja te entreguei um chamado SmartRoad-Preditiva, ja que pensei em usar de base nosso app que construimos em https://github.com/MAJE-Dev/SmartRoad para montar esse modelo preditivo!

### O que a IA fez a partir desse prompt

1. Leu as páginas 31 a 33 do briefing (entregáveis e critérios) e o README do app SmartRoad.
2. Propôs a pergunta de ML ("a ocorrência vai demorar mais de 30 dias?") a partir do indicador de impacto da Ficha.
3. Baixou os dados reais do SP156 no Portal de Dados Abertos da Prefeitura de São Paulo e escreveu `ml/dados/preparar_dados.py`.
4. Explorou os dados e tomou as decisões de preparação: alvo de 30 dias, entradas sem vazamento e divisão treino/teste por data.
5. Escreveu e executou o notebook `ml/smartroad_preditiva.ipynb` (XGBoost, 18 combinações de hiperparâmetros, validação cruzada só no treino, métricas de treino e teste).
6. Escreveu `RELATORIO_ML.md`, `README.md`, `ml/dados/README.md` e este arquivo.

### Decisões que vieram da IA e que a equipe precisa saber explicar

- **Por que classificação com limite de 30 dias**, e não regressão do número de dias (Seção 3.2 do notebook).
- **Por que a divisão é por data**, e não por sorteio, e por que a validação cruzada usa `TimeSeriesSplit` (Seções 3.6, 5 e 6.1).
- **Por que `orgao`, `status` e `data_finalizacao` não são entradas** (Seção 2 do notebook).
- **Por que o XGBoost** entre os modelos permitidos (Seção 4).
- **O cuidado com a variável mês** e a discussão de overfitting (Seção 6.5).

## Prompt 2 — devolutiva do professor sobre o README

> Resposta do professor sobre o projeto: "pelo readme.md, me parece OK. Mas cuidado com essa modelagem porque ela exige série temporal. SE vc não fizer uma série temporal ela está essencialmente errada."
>
> Vamos ver em prática o que fazer, me recomende também qual modelo (Sonnet ou Opus) usar e qual esforço.

A IA propôs um plano (manter a pergunta, mas dar ao modelo o histórico recente e validar mês a mês), a equipe aprovou a abordagem "features temporais + walk-forward" e pediu para ampliar os dados para 2 anos.

## Prompt 3 — execução do plano de série temporal

### O que a IA fez a partir desses prompts

1. Ampliou os dados de 12 para 24 meses (01/07/2024 a 30/06/2026) em `ml/dados/preparar_dados.py` e descobriu que o arquivo do 2º trimestre de 2024 não tem a coluna "Serviço" (por isso a série começa no 3º trimestre de 2024) e que o do 1º trimestre de 2025 tem exatamente o limite de linhas do Excel.
2. Criou 14 indicadores de série temporal por serviço e por subprefeitura (fila, fila atrasada, volume, ritmo de finalização, taxa de demora madura e tendência), com um teste que confere que nenhum deles usa informação do dia ou do futuro.
3. Passou a deixar um intervalo de 30 dias entre treino e teste e entre treino e validação, porque o desfecho de um pedido só é conhecido 30 dias depois.
4. Adicionou a comparação com a previsão ingênua (persistência), com o modelo sem série temporal e o walk-forward de 12 meses, e removeu o mês do calendário das entradas depois de medir que ele piorava a previsão.
5. Reexecutou o notebook do início ao fim e atualizou `RELATORIO_ML.md`, `README.md` e `ml/dados/README.md` com os números novos.

### Decisões que vieram da IA e que a equipe precisa saber explicar

- **O que é a `taxa_madura` e por que ela só olha pedidos de 90 a 31 dias atrás** (Seção 3.4 do notebook).
- **Por que existe um intervalo de 30 dias entre treino e teste** (Seção 3.6).
- **Por que o ganho da série temporal é modesto e por que isso é um resultado válido**, e não um erro (Seção 6.4).
- **Por que o mês do calendário foi retirado das entradas** (Seção 6.4).
- **Por que o recorte começa em 01/07/2024**, e não em 2023 (`ml/dados/README.md`).

### O que a equipe conferiu ou ainda precisa conferir

- [ ] Rodar o notebook do início ao fim e conferir se os números batem com o relatório (a execução leva cerca de 7 minutos).
- [ ] Ler cada célula e conseguir explicar cada linha.
- [ ] Conferir a Ficha da CitizenTech no `README.md` com o restante da equipe.
- [ ] Gravar o vídeo de até 5 minutos e colocar o link no `README.md`.
