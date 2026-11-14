# Dados usados no modelo

Todos os dados são **reais e públicos**. Nada foi simulado.

## Fonte, link e período

| | |
| --- | --- |
| **Fonte** | Prefeitura de São Paulo, Secretaria Municipal de Inovação e Tecnologia — conjunto "Dados do SP156 - Solicitações" |
| **Link** | https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156 |
| **Período** | solicitações abertas de **01/07/2025 a 30/06/2026** |
| **Arquivos originais** | `arquivo-final-3-trim-25.csv`, `arquivo-final-4-trim-25.csv`, `arquivo-final-1-trim-26.csv` e `arquivo-final-2-trim-26.csv` |
| **Versão dos arquivos** | republicados pela Prefeitura em 10/08/2026. O status e a data de finalização mostram a situação de cada pedido até essa extração (a finalização mais recente é de 07/08/2026) |
| **Baixados em** | 14/11/2026 |
| **Licença** | Creative Commons CC0 (domínio público) |
| **Dicionário oficial** | "Dicionário dados abertos - SP156 2020 em diante", na mesma página do conjunto |

O SP156 é o canal oficial de pedidos de serviço da Prefeitura (central telefônica, portal, aplicativo e chatbot). Segundo a página do conjunto, as bases passam por tratamento para retirar informações pessoais dos solicitantes antes da publicação.

## O que está nesta pasta

| Arquivo | O que é |
| --- | --- |
| `sp156_zeladoria_jul2025_jun2026.csv.gz` | recorte usado pelo notebook: 189.467 solicitações, 11 colunas, 3 MB |
| `preparar_dados.py` | script que baixa os 4 arquivos originais e gera o recorte |
| `brutos/` | os arquivos originais (cerca de 430 MB). Ficam fora do Git; o script baixa de novo quando precisar |

## Como o recorte foi feito

Os 4 arquivos originais têm 2.023.061 solicitações de todos os assuntos da Prefeitura. O script `preparar_dados.py` faz só duas coisas, sem alterar nenhum valor:

1. **Filtra as linhas** dos 9 serviços que correspondem aos tipos de ocorrência do app SmartRoad.
2. **Mantém 10 colunas** e acrescenta `tipo_smartroad`. Logradouro, número e CEP ficam de fora, porque o modelo não usa o endereço.

| Tipo no SmartRoad | Serviço no SP156 | Solicitações |
| --- | --- | ---: |
| Buraco | Tapa-buraco | 100.268 |
| Buraco | Tapa-buraco em faixa exclusiva ou corredor de ônibus | 3.662 |
| Bueiro | Solicitar limpeza de bueiros, boca de lobo e poços de visita | 24.463 |
| Bueiro | Reformar galerias de águas de chuvas (pluviais) | 12.450 |
| Bueiro | Drenagem de água da chuva - Bueiros e bocas de lobo | 2.025 |
| Calçada | Guias, sarjetas e sarjetões - solicitar manutenção | 30.286 |
| Calçada | Calçada pública - solicitar manutenção | 6.612 |
| Calçada | Acessibilidade - solicitar avaliação de obstáculo na calçada | 5.261 |
| Calçada | Calçada particular - denunciar calçada danificada ou inexistente | 4.440 |
| | **Total** | **189.467** |

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

O script baixa os 4 arquivos para `ml/dados/brutos/` (se ainda não estiverem lá) e regrava `sp156_zeladoria_jul2025_jun2026.csv.gz`.
