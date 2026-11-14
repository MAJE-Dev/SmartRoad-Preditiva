# Prompts de IA usados neste trabalho

O briefing da Global Solution permite usar IA como copiloto e pede o registro dos prompts. Este arquivo lista o que foi pedido, o que a IA fez e o que a equipe precisa conferir.

**Ferramenta:** Claude Code (Anthropic), em sessão na nuvem com acesso a este repositório.
**Data:** 14/11/2026.

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
- **Por que a divisão é por data**, e não por sorteio, e por que a validação cruzada usa `TimeSeriesSplit` (Seções 3.5, 5 e 6.1).
- **Por que `orgao`, `status` e `data_finalizacao` não são entradas** (Seção 2 do notebook).
- **Por que o XGBoost** entre os modelos permitidos (Seção 4).
- **O cuidado com a variável mês** e a discussão de overfitting (Seção 6.4).

### O que a equipe conferiu ou ainda precisa conferir

- [ ] Rodar o notebook do início ao fim e conferir se os números batem com o relatório.
- [ ] Ler cada célula e conseguir explicar cada linha.
- [ ] Conferir a Ficha da CitizenTech no `README.md` com o restante da equipe.
- [ ] Gravar o vídeo de até 5 minutos e colocar o link no `README.md`.
