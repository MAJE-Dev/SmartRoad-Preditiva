# Dados usados no modelo

Todos os dados são **reais e públicos**. Nada foi simulado.

## Fonte, link e período

| | |
| --- | --- |
| **Fonte** | Prefeitura de São Paulo, Secretaria Municipal de Inovação e Tecnologia — conjunto "Dados do SP156 - Solicitações" |
| **Link** | https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156 |
| **Período** | solicitações abertas de **01/07/2024 a 30/06/2026** (2 anos corridos) |
| **Arquivos originais** | 8 arquivos trimestrais, do 3º trimestre de 2024 ao 2º trimestre de 2026 (`arquivo-final-3-trim.-2024.csv` até `arquivo-final-2-trim-26.csv`; os links exatos estão em `preparar_dados.py`) |
| **Versão dos arquivos** | os arquivos de 2025 e 2026 foram republicados pela Prefeitura em 10/08/2026. O status e a data de finalização mostram a situação de cada pedido até essa extração (a finalização mais recente é de 10/08/2026) |
| **Baixados em** | 14/11/2026 |
| **Licença** | Creative Commons CC0 (domínio público) |
| **Dicionário oficial** | "Dicionário dados abertos - SP156 2020 em diante", na mesma página do conjunto |

O SP156 é o canal oficial de pedidos de serviço da Prefeitura (central telefônica, portal, aplicativo e chatbot). Segundo a página do conjunto, as bases passam por tratamento para retirar informações pessoais dos solicitantes antes da publicação.

## O que está nesta pasta

| Arquivo | O que é |
| --- | --- |
| `sp156_zeladoria_jul2024_jun2026.csv.gz` | recorte usado pelo notebook: 387.605 solicitações, 11 colunas, 6 MB |
| `preparar_dados.py` | script que baixa os 8 arquivos originais e gera o recorte |
| `brutos/` | os arquivos originais (cerca de 930 MB). Ficam fora do Git; o script baixa de novo quando precisar |

## Como o recorte foi feito

Os 8 arquivos originais têm 4.704.953 solicitações de todos os assuntos da Prefeitura. O script `preparar_dados.py` faz só duas coisas, sem alterar nenhum valor:

1. **Filtra as linhas** dos 9 serviços que correspondem aos tipos de ocorrência do app SmartRoad.
2. **Mantém 10 colunas** e acrescenta `tipo_smartroad`. Logradouro, número e CEP ficam de fora, porque o modelo não usa o endereço.

| Tipo no SmartRoad | Serviço no SP156 | Solicitações |
| --- | --- | ---: |
| Buraco | Tapa-buraco | 208.350 |
| Buraco | Tapa-buraco em faixa exclusiva ou corredor de ônibus | 6.168 |
| Bueiro | Solicitar limpeza de bueiros, boca de lobo e poços de visita | 51.511 |
| Bueiro | Reformar galerias de águas de chuvas (pluviais) | 23.120 |
| Bueiro | Drenagem de água da chuva - Bueiros e bocas de lobo | 6.173 |
| Calçada | Guias, sarjetas e sarjetões - solicitar manutenção | 62.293 |
| Calçada | Calçada pública - solicitar manutenção | 12.243 |
| Calçada | Acessibilidade - solicitar avaliação de obstáculo na calçada | 9.359 |
| Calçada | Calçada particular - denunciar calçada danificada ou inexistente | 8.388 |
| | **Total** | **387.605** |

O tipo "Iluminação" do app não aparece: não há serviço de iluminação pública nos arquivos do SP156 deste período.

## Colunas do recorte

| Coluna | Nome original no SP156 | Descrição |
| --- | --- | --- |
| `tipo_smartroad` | (criada por nós) | tipo de ocorrência do app: Buraco, Bueiro ou Calçada |
| `data_abertura` | Data de Abertura | dia em que o cidadão abriu o pedido (dd/mm/aaaa) |
| `data_finalizacao` | Data de Finalização | dia em que o protocolo foi encerrado; vazio se ainda estava aberto na extração |
| `canal` | Meio de Comunicação | por onde o pedido chegou: MOBILE, PORTAL, CRM, CHATBOT ou RESOLUCAO |
| `servico` | Serviço | serviço pedido, conforme a Carta de Serviços da Prefeitura |
| `status` | Status | situação na extração: Finalizada, Aberto, Em Andamento ou Cancelada |
| `orgao` | Órgão | órgão responsável **na data da extração** (pode mudar depois da abertura) |
| `latitude`, `longitude` | Latitude, Longitude | coordenadas do local do pedido |
| `subprefeitura` | Prefeitura Operacional | subprefeitura do local |
| `distrito` | Distrito | distrito do local |

## Cuidados ao usar

- **Por que 2 anos, e por que começa em 01/07/2024.** O modelo usa séries temporais diárias (fila, ritmo de finalização e taxa de demora recentes), e a série precisa ser contínua. O arquivo do 2º trimestre de 2024 não traz a coluna "Serviço", então não dá para separar os nossos 9 serviços nele; começar no 3º trimestre de 2024 evita um buraco no meio da série.
- **O 1º trimestre de 2025 pode estar incompleto.** O arquivo tem 1.048.575 linhas, exatamente o limite de linhas de uma planilha Excel (2^20 menos o cabeçalho). Os dias do fim do trimestre aparecem normalmente, mas não temos como garantir que nenhuma linha foi perdida.

- **"Finalizada" não quer dizer "consertado".** O status indica que o órgão encerrou o protocolo. Os dados não dizem se o serviço foi executado.
- **Solicitação não é problema.** O dicionário oficial avisa que várias pessoas podem pedir o mesmo serviço, e que a Prefeitura pode executar um serviço sem ter recebido pedido.
- **`orgao`, `status` e `data_finalizacao` não são entradas do modelo.** São informações de depois da abertura. O notebook usa as duas últimas só para construir o alvo.
- **Significado dos canais.** O dicionário descreve portal, central telefônica, aplicativo e chatbot, mas os arquivos usam os códigos MOBILE, PORTAL, CRM e CHATBOT. Entendemos que MOBILE é o aplicativo e CRM é o atendimento registrado pela central; o dicionário não confirma essa correspondência.
- A limpeza (canceladas, coordenadas fora da cidade, nomes de subprefeitura) é feita e explicada no notebook, Seção 3.1.

## Como gerar o recorte de novo

```bash
pip install -r ml/requirements.txt
```

```bash
python ml/dados/preparar_dados.py
```

O script baixa os 8 arquivos para `ml/dados/brutos/` (se ainda não estiverem lá) e regrava `sp156_zeladoria_jul2024_jun2026.csv.gz`.
