"""
FinOps Check - Identificador de recursos ociosos/orfaos na Magalu Cloud
=========================================================================

Objetivo:
    Identificar recursos reais da sua conta Magalu Cloud que estao gerando
    custo mas aparentam nao estar em uso (volumes de Block Storage sem
    instancia anexada, Load Balancers sem backend configurado, etc).

Como obtem os dados:
    Este script usa o `mgc` CLI (que voce ja tem instalado e autenticado
    com sua API Key) para listar seus recursos reais, via subprocess.
    Isso evita ter que descobrir/adivinhar endpoints REST nao documentados
    publicamente - o mgc CLI ja sabe os caminhos corretos.

    Caso o `mgc` CLI nao esteja instalado, nao esteja autenticado, ou a
    chamada falhe por qualquer motivo, o script cai automaticamente para
    um arquivo CSV de exemplo (fallback), sem travar a execucao.

Uso:
    python3 finops_check.py [caminho_do_csv_fallback]

Saida:
    - Relatorio formatado no terminal
    - Arquivo 'relatorio_desperdicio.csv' com os recursos identificados

Nota sobre os custos:
    A Magalu Cloud nao expoe publicamente uma API de billing/consumo
    detalhado por recurso (a tela de Faturamento do Console usa uma API
    interna que exige login de sessao, nao API Key). Por isso, os custos
    aqui sao ESTIMATIVAS aproximadas baseadas na tabela de precos publica,
    nao valores exatos de fatura.
"""

import csv
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Estimativas de custo por hora (R$), baseadas na tabela publica de precos.
# Ajuste esses valores conforme os planos/flavors reais que voce usa.
CUSTO_HORA_ESTIMADO = {
    "virtual_machine": 0.05,   # ex: BV-Instancia 1 vCPU / 1GB RAM
    "block_storage": 0.01,     # por GB/mes, aproximado e convertido em estimativa/hora
    "load_balancer": 0.05,
}


# ---------------------------------------------------------------------
# Chamadas ao mgc CLI
# ---------------------------------------------------------------------

def rodar_mgc(comando):
    """
    Executa um comando do mgc CLI pedindo saida em JSON.
    Retorna a lista de itens (ja parseada) ou None se algo falhar.
    """
    try:
        resultado = subprocess.run(
            ["mgc", *comando, "-o", "json", "-r"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if resultado.returncode != 0:
            return None

        dados = json.loads(resultado.stdout)

        if isinstance(dados, list):
            return dados
        if isinstance(dados, dict):
            for chave in ("instances", "volumes", "results", "load_balancers"):
                if chave in dados and isinstance(dados[chave], list):
                    return dados[chave]
        return None

    except FileNotFoundError:
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def obter_dados_reais():
    """
    Coleta VMs, volumes de Block Storage e Load Balancers reais da conta,
    e monta uma lista normalizada no mesmo formato usado no restante do script.
    """
    instances = rodar_mgc(["virtual-machine", "instances", "list"])
    volumes = rodar_mgc(["block-storage", "volumes", "list"])
    load_balancers = rodar_mgc(["load-balancer", "network-loadbalancers", "list"])

    if instances is None and volumes is None and load_balancers is None:
        return None

    instances = instances or []
    volumes = volumes or []
    load_balancers = load_balancers or []

    registros = []

    for i in instances:
        registros.append({
            "resource_id": str(i.get("id", "")),
            "resource_name": str(i.get("name", "")),
            "resource_type": "virtual_machine",
            "linked_instance_id": str(i.get("id", "")),
            "billed_cost": CUSTO_HORA_ESTIMADO["virtual_machine"],
            "usage_amount": 1 if i.get("state", "").lower() == "running" else 0,
            "billing_period": datetime.now().strftime("%Y-%m"),
        })

    for v in volumes:
        anexado = v.get("attachment") or v.get("instance_id") or v.get("attached_to")
        registros.append({
            "resource_id": str(v.get("id", "")),
            "resource_name": str(v.get("name", "")),
            "resource_type": "block_storage",
            "linked_instance_id": str(anexado or ""),
            "billed_cost": CUSTO_HORA_ESTIMADO["block_storage"] * float(v.get("size", 1)),
            "usage_amount": 1 if anexado else 0,
            "billing_period": datetime.now().strftime("%Y-%m"),
        })

    for lb in load_balancers:
        backends = lb.get("backends") or []
        total_targets = sum(len(b.get("targets", [])) for b in backends)
        registros.append({
            "resource_id": str(lb.get("id", "")),
            "resource_name": str(lb.get("name", "")),
            "resource_type": "load_balancer",
            "linked_instance_id": str(total_targets) if total_targets else "",
            "billed_cost": CUSTO_HORA_ESTIMADO["load_balancer"],
            "usage_amount": total_targets,
            "billing_period": datetime.now().strftime("%Y-%m"),
        })

    return registros


# ---------------------------------------------------------------------
# Fallback: CSV de exemplo
# ---------------------------------------------------------------------

def carregar_dados_do_csv(caminho_csv):
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def carregar_dados(caminho_csv_fallback):
    dados_reais = obter_dados_reais()
    if dados_reais:
        return dados_reais, "mgc_cli"

    print("Aviso: nao foi possivel obter recursos reais via mgc CLI. Usando dados de exemplo.\n")

    if not caminho_csv_fallback.exists():
        print(f"Erro: nem dados reais nem arquivo de exemplo encontrado -> {caminho_csv_fallback}")
        sys.exit(1)

    return carregar_dados_do_csv(caminho_csv_fallback), "csv_exemplo"


# ---------------------------------------------------------------------
# Regras de analise
# ---------------------------------------------------------------------

def eh_recurso_ocioso(linha):
    custo = float(linha["billed_cost"] or 0)
    uso = float(linha["usage_amount"] or 0)
    tipo = linha["resource_type"]
    vinculo = (linha.get("linked_instance_id") or "").strip()

    if custo <= 0:
        return False, ""

    if tipo == "load_balancer" and not vinculo:
        return True, "Load balancer com backend configurado mas sem nenhuma instancia (target) recebendo trafego"

    if tipo == "block_storage" and not vinculo:
        return True, "Volume de block storage sem instancia anexada"

    if tipo == "virtual_machine" and uso == 0:
        return True, "Maquina virtual existente mas nao esta em execucao (status inativo)"

    return False, ""


def analisar(dados):
    achados = []
    for linha in dados:
        ocioso, motivo = eh_recurso_ocioso(linha)
        if ocioso:
            achados.append({
                "resource_id": linha["resource_id"],
                "resource_name": linha["resource_name"],
                "resource_type": linha["resource_type"],
                "billed_cost": linha["billed_cost"],
                "billing_period": linha["billing_period"],
                "motivo": motivo,
            })
    return achados


# ---------------------------------------------------------------------
# Saida (terminal + CSV)
# ---------------------------------------------------------------------

def imprimir_relatorio(achados, total_recursos, origem):
    print("=" * 70)
    print(" RELATORIO FINOPS - POSSIVEL DESPERDICIO DE RECURSOS")
    print(" Gerado em:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    fonte = "recursos reais da conta (via mgc CLI)" if origem == "mgc_cli" else "dados de exemplo (CSV)"
    print(" Fonte dos dados:", fonte)
    if origem == "mgc_cli":
        print(" Atencao: custos sao ESTIMATIVAS aproximadas, nao valores exatos de fatura.")
    print("=" * 70)

    if not achados:
        print("\nNenhum recurso ocioso identificado. Tudo certo por aqui!\n")
        return

    custo_total = sum(float(a["billed_cost"]) for a in achados)

    print(f"\nRecursos analisados: {total_recursos}")
    print(f"Recursos com possivel desperdicio: {len(achados)}")
    print(f"Custo estimado em desperdicio: R$ {custo_total:.2f}\n")

    for a in achados:
        print(f"- [{a['resource_type']}] {a['resource_name']} ({a['resource_id']})")
        print(f"    Motivo: {a['motivo']}")
        print(f"    Custo estimado: R$ {float(a['billed_cost']):.2f} | Periodo: {a['billing_period']}\n")

    print("=" * 70)


def salvar_csv(achados, caminho_saida):
    if not achados:
        return
    with open(caminho_saida, "w", newline="", encoding="utf-8") as f:
        campos = ["resource_id", "resource_name", "resource_type",
                  "billed_cost", "billing_period", "motivo"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(achados)
    print(f"Relatorio salvo em: {caminho_saida}\n")


def main():
    diretorio_script = Path(__file__).parent
    caminho_csv_fallback = Path(sys.argv[1]) if len(sys.argv) > 1 else diretorio_script / "consumo_focus_magalu.csv"

    dados, origem = carregar_dados(caminho_csv_fallback)
    achados = analisar(dados)

    imprimir_relatorio(achados, total_recursos=len(dados), origem=origem)
    salvar_csv(achados, diretorio_script / "relatorio_desperdicio.csv")


if __name__ == "__main__":
    main()