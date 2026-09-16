"""Executa as buscas não informadas já implementadas em aima.search.

Esta camada só chama o algoritmo, mede o tempo e lê o Node retornado.
Não reimplementa BFS, DFS nem as variações de profundidade.
"""

import time

from aima.search import (
    Node,
    breadth_first_graph_search,
    depth_first_graph_search,
    depth_limited_search,
    iterative_deepening_search,
)

# depth_limited_search do AIMA é busca em árvore (não descarta ciclos).
# O limite padrão da função é 50, impraticável neste problema sem alterar
# o AIMA. 8 cobre a solução de menor profundidade e ainda termina rápido.
LIMITE_PADRAO = 8


def buscar_em_largura(problema):
    return executar_busca("Busca em Largura", breadth_first_graph_search, problema)


def buscar_em_profundidade(problema):
    return executar_busca("Busca em Profundidade", depth_first_graph_search, problema)


def buscar_profundidade_limitada(problema, limite):
    nome = f"Busca em Profundidade Limitada (limite {limite})"
    return executar_busca(nome, depth_limited_search, problema, limite)


def buscar_aprofundamento_iterativo(problema):
    return executar_busca(
        "Aprofundamento Iterativo",
        iterative_deepening_search,
        problema,
    )


def comparar_estrategias(problema, limite=LIMITE_PADRAO):
    """Executa as quatro estratégias. Não ranqueia qual é melhor."""
    return [
        buscar_em_largura(problema),
        buscar_em_profundidade(problema),
        buscar_profundidade_limitada(problema, limite),
        buscar_aprofundamento_iterativo(problema),
    ]


def executar_busca(nome, funcao, problema, *args):
    inicio = time.perf_counter()
    bruto = funcao(problema, *args)
    tempo_ms = (time.perf_counter() - inicio) * 1000
    return montar_resultado(nome, problema, bruto, tempo_ms)


def montar_resultado(nome, problema, bruto, tempo_ms):
    """Lê apenas o que a API do AIMA devolve. Não inventa métricas."""
    base = {
        "nome": nome,
        "estado_inicial": problema.initial,
        "tempo_ms": tempo_ms,
        "no": None,
        "acoes": None,
        "estados": None,
        "profundidade": None,
        "custo": None,
        "passos": None,
    }

    if isinstance(bruto, Node):
        acoes = bruto.solution()
        estados = bruto.path_states()
        return {
            **base,
            "status": "solucao",
            "no": bruto,
            "acoes": acoes,
            "estados": estados,
            "profundidade": bruto.depth,
            "custo": bruto.path_cost,
            "passos": len(acoes),
        }

    if bruto == "cutoff":
        return {**base, "status": "cutoff"}

    if bruto is None:
        return {**base, "status": "sem_solucao"}

    return {**base, "status": "inesperado", "bruto": bruto}


def caminho_respeita_regras(problema, resultado):
    """Confere cada transição e o teste de objetivo, sem alterar o AIMA."""
    if resultado["status"] != "solucao":
        return False

    estados = resultado["estados"]
    acoes = resultado["acoes"]
    if not estados or estados[0] != problema.initial:
        return False
    if len(acoes) != len(estados) - 1:
        return False

    for indice, acao in enumerate(acoes):
        atual = estados[indice]
        proximo = estados[indice + 1]
        if acao not in problema.actions(atual):
            return False
        if problema.result(atual, acao) != proximo:
            return False
        if not _dentro_das_capacidades(problema, proximo):
            return False

    return problema.goal_test(estados[-1])


def _dentro_das_capacidades(problema, estado):
    x, y = estado
    return 0 <= x <= problema.CAPACIDADE_5 and 0 <= y <= problema.CAPACIDADE_3
