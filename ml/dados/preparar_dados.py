"""Baixa os dados abertos do SP156 e gera o recorte usado no notebook.

Fonte: Portal de Dados Abertos da Prefeitura de São Paulo - "Dados do SP156 - Solicitações"
       https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156
Período: solicitações abertas de 01/07/2025 a 30/06/2026 (4 arquivos trimestrais).

O que o script faz:
  1. baixa os 4 arquivos trimestrais (cerca de 430 MB) para ml/dados/brutos/ (pasta fora do Git);
  2. mantém só os 9 serviços que correspondem aos tipos de ocorrência do app SmartRoad;
  3. mantém só as colunas usadas e grava ml/dados/sp156_zeladoria_jul2025_jun2026.csv.gz.

Nenhuma linha é alterada ou inventada: é só filtro de linhas e de colunas.
A limpeza de verdade (datas, categorias, alvo) fica no notebook.

Uso:  python ml/dados/preparar_dados.py
"""

import time
import urllib.request
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parent
BRUTOS = PASTA / "brutos"
SAIDA = PASTA / "sp156_zeladoria_jul2025_jun2026.csv.gz"

BASE = "https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/"
ARQUIVOS = {
    "arquivo-final-3-trim-25.csv": "3b1d2648-d586-40c8-819c-24fbb8005343/download/arquivo-final-3-trim-25.csv",
    "arquivo-final-4-trim-25.csv": "d3a98097-8128-45d4-b8fe-21874b81c971/download/arquivo-final-4-trim-25.csv",
    "arquivo-final-1-trim-26.csv": "75105148-4efd-48f3-8ae0-fc6c2adf7060/download/arquivo-final-1-trim-26.csv",
    "arquivo-final-2-trim-26.csv": "368eb32d-ef25-4441-be8f-fce0146575a1/download/arquivo-final-2-trim-26.csv",
}

# Serviços do SP156 que correspondem aos tipos de ocorrência do app SmartRoad.
# (O SP156 não tem serviço de iluminação pública nesses arquivos, então o tipo "Iluminação" fica de fora.)
SERVICOS = {
    "Tapa-buraco": "Buraco",
    "Tapa-buraco em faixa exclusiva ou corredor de ônibus": "Buraco",
    "Solicitar limpeza de bueiros, boca de lobo e poços de visita": "Bueiro",
    "Drenagem de água da chuva - Bueiros e bocas de lobo": "Bueiro",
    "Reformar galerias de águas de chuvas (pluviais)": "Bueiro",
    "Calçada pública - solicitar manutenção": "Calçada",
    "Calçada particular - denunciar calçada danificada ou inexistente": "Calçada",
    "Acessibilidade - solicitar avaliação de obstáculo na calçada": "Calçada",
    "Guias, sarjetas e sarjetões - solicitar manutenção": "Calçada",
}

# Nome original no SP156 -> nome da coluna no nosso arquivo.
# Endereço (logradouro, número e CEP) fica de fora: o modelo não usa.
COLUNAS = {
    "Data de Abertura": "data_abertura",
    "Data de Finalização": "data_finalizacao",
    "Meio de Comunicação": "canal",
    "Serviço": "servico",
    "Status": "status",
    "Órgão": "orgao",
    "Prefeitura Operacional": "subprefeitura",
    "Distrito": "distrito",
    "Latitude": "latitude",
    "Longitude": "longitude",
}


def baixar(nome: str, caminho_url: str) -> Path:
    """Baixa um arquivo trimestral, tentando de novo se a conexão cair."""
    destino = BRUTOS / nome
    if destino.exists():
        return destino
    BRUTOS.mkdir(exist_ok=True)
    for tentativa in range(1, 6):
        try:
            print(f"Baixando {nome} (tentativa {tentativa})...")
            parcial = destino.with_suffix(".parcial")
            urllib.request.urlretrieve(BASE + caminho_url, parcial)
            parcial.rename(destino)
            return destino
        except Exception as erro:  # conexão caiu no meio: espera e tenta de novo
            print(f"  falhou: {erro}")
            time.sleep(5 * tentativa)
    raise RuntimeError(f"Não foi possível baixar {nome}")


def main() -> None:
    partes = []
    for nome, caminho_url in ARQUIVOS.items():
        arquivo = baixar(nome, caminho_url)
        # Os arquivos do portal usam ";" como separador e codificação Latin-1.
        bruto = pd.read_csv(arquivo, sep=";", encoding="latin1", dtype=str, usecols=list(COLUNAS))
        recorte = bruto[bruto["Serviço"].isin(SERVICOS.keys())].rename(columns=COLUNAS)
        print(f"{nome}: {len(bruto):,} solicitações no total, {len(recorte):,} no recorte")
        partes.append(recorte)

    dados = pd.concat(partes, ignore_index=True)
    dados.insert(0, "tipo_smartroad", dados["servico"].map(SERVICOS))

    # Ordena por data de abertura (o arquivo original vem em dd/mm/aaaa).
    ordem = pd.to_datetime(dados["data_abertura"], format="%d/%m/%Y").argsort(kind="stable")
    dados = dados.iloc[ordem].reset_index(drop=True)

    # mtime=0 deixa o .gz idêntico a cada execução (sem carimbo de hora dentro do arquivo).
    dados.to_csv(SAIDA, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"\nGravado {SAIDA.name}: {len(dados):,} linhas, {SAIDA.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
