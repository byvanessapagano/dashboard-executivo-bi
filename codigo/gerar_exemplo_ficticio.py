#!/usr/bin/env python3
"""
Gerador de dados 100% FICTICIOS para demonstracao de BI.

Simula duas bases (Pedidos e Faturas) ligadas por "Nº do documento" e faz a
reconciliacao entre elas:
  - Só em Pedidos (sem Fatura)
  - Em Pedidos e Faturas
  - Só em Faturas (sem Pedido)

Uso: python gerar_exemplo_ficticio.py [PASTA_SAIDA]
Gera dados_ficticios.json (KPIs, matriz, dimensoes) e dados_cruzados.csv.
Usa so a biblioteca padrao. Semente fixa: o resultado e sempre o mesmo.
"""
import csv, json, random, sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

A, B = "Pedidos", "Faturas"
SIT_A, SIT_AB, SIT_B = "Só em Pedidos (sem Fatura)", "Em Pedidos e Faturas", "Só em Faturas (sem Pedido)"
COLS_A = ["Cliente", "Nº do documento", "Categoria", "Código do item", "Local de entrega", "Unidade", "Status do pedido"]
COLS_B = ["Nº do documento", "Fatura", "Seq.", "Fatura de origem", "Data de emissão", "Descrição da fatura",
          "Filial", "Tipo de fatura", "Quantidade"]
COLS = ["Situação"] + COLS_A + COLS_B[1:]

N_SO_A, N_SO_B, N_AMBOS = 1150, 640, 11400


def escolha(rng, itens, pesos):
    return rng.choices(itens, weights=pesos, k=1)[0]


def gerar(seed=2026):
    rng = random.Random(seed)
    cats = ["Hardware", "Software", "Serviços", "Insumos", "Manutenção", "Logística"]
    pc = [30, 18, 22, 14, 10, 6]
    unid = [f"Unidade {i:02d}" for i in range(1, 13)]
    pu = [14, 12, 11, 10, 9, 9, 8, 7, 6, 5, 5, 4]
    stat = ["Aberto", "Em análise", "Aprovado", "Pendente", "Cancelado", "Bloqueado", "Aguardando cliente"]
    ps = [26, 20, 18, 14, 9, 7, 6]
    desc = ["Serviço mensal", "Venda de produto", "Assinatura anual", "Taxa de entrega", "Ajuste comercial"]
    pd_ = [34, 30, 18, 12, 6]
    filial = [f"Filial {i:02d}" for i in range(1, 9)]
    pf = [20, 17, 15, 13, 11, 10, 8, 6]
    tipos = ["Venda", "Serviço", "Devolução", "Ajuste"]
    pt = [55, 30, 9, 6]
    qtds = ["1", "2", "0", "3"]
    pq = [70, 15, 10, 5]
    base = datetime(2024, 1, 1)

    ids = rng.sample(range(100000, 999999), N_SO_A + N_SO_B)

    def doc(i):
        return f"DOC-{i}"

    linhas_a = []
    for n in range(N_SO_A + 15):  # ~1% de documentos repetidos
        i = ids[n] if n < N_SO_A else ids[rng.randrange(N_SO_A)]
        linhas_a.append([f"C-{rng.randint(1000, 9999)}" if rng.random() < .65 else "", doc(i),
                         escolha(rng, cats, pc), f"ITM-{rng.randint(10000, 99999)}",
                         f"Zona {rng.randint(1, 14):02d}" if rng.random() < .5 else "",
                         escolha(rng, unid, pu), escolha(rng, stat, ps)])
    linhas_b = []
    for n in range(N_SO_B + 5):
        i = ids[N_SO_A + n] if n < N_SO_B else ids[N_SO_A + rng.randrange(N_SO_B)]
        d = base + timedelta(days=rng.randint(0, 1050))
        linhas_b.append([doc(i), f"FAT-{rng.randint(100000, 999999)}", escolha(rng, ["0", "1"], [92, 8]),
                         f"PED-{rng.randint(10000, 99999)}", d.strftime("%Y-%m-%d 00:00:00"),
                         escolha(rng, desc, pd_), escolha(rng, filial, pf),
                         escolha(rng, tipos, pt), escolha(rng, qtds, pq)])
    return rng, linhas_a, linhas_b


def dims(rng, linhas, cols, nomes, n_ambos_linhas):
    out = {}
    for nome in nomes:
        j = cols.index(nome)
        cont = Counter(r[j] for r in linhas)
        tot = sum(cont.values())
        itens = sorted(cont.items(), key=lambda x: (-x[1], x[0]))[:300]
        out[nome] = [[v, n, max(1, round(n_ambos_linhas * n / tot * rng.uniform(.8, 1.25)))] for v, n in itens]
    return out


def montar():
    rng, la, lb = gerar()
    l_ambos_a, l_ambos_b = 11420, 11410
    kpi = {"linhas_pedidos": len(la) + l_ambos_a, "linhas_faturas": len(lb) + l_ambos_b,
           "pedidos": N_SO_A + N_AMBOS, "faturas": N_SO_B + N_AMBOS, "ambos": N_AMBOS,
           "so_pedidos": N_SO_A, "so_faturas": N_SO_B}
    pct = lambda a, b: f"{100 * a / b:.1f}%"
    matriz = [[SIT_A, A, len(la), N_SO_A, pct(len(la), kpi["linhas_pedidos"])],
              [SIT_AB, A, l_ambos_a, N_AMBOS, pct(l_ambos_a, kpi["linhas_pedidos"])],
              [SIT_B, B, len(lb), N_SO_B, pct(len(lb), kpi["linhas_faturas"])]]
    lados = {
        "pedidos": {"rotulo": SIT_A, "cols": COLS_A, "rows": la,
                    "dims": dims(rng, la, COLS_A, ["Unidade", "Categoria", "Status do pedido"], l_ambos_a)},
        "faturas": {"rotulo": SIT_B, "cols": COLS_B, "rows": lb,
                    "dims": dims(rng, lb, COLS_B, ["Filial", "Descrição da fatura", "Tipo de fatura"], l_ambos_b)},
    }
    D = {"kpi": kpi, "matriz": matriz, "lados": lados, "chave": "Nº do documento",
         "fonte": "Dados fictícios gerados para demonstração",
         "gerado": datetime.now().strftime("%d/%m/%Y %H:%M")}
    # tabela unica: Pedidos e Faturas lado a lado
    rows = [[SIT_A] + r + [""] * (len(COLS_B) - 1) for r in la]
    rows += [[SIT_B, "", r[0]] + [""] * (len(COLS_A) - 2) + r[1:] for r in lb]
    return D, rows


def main(saida="dados"):
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    D, rows = montar()
    (saida / "dados_ficticios.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(saida / "dados_cruzados.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLS)
        w.writerows(rows)
    print("KPIs:", D["kpi"])
    print("Linhas na tabela cruzada:", len(rows), "| Arquivos em:", saida.resolve())


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dados")