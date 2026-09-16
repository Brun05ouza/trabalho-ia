"""Testes da modelagem do problema 03 e da validade das soluções."""

import pytest
from aima.search import breadth_first_graph_search

from src.buscas import (
    buscar_aprofundamento_iterativo,
    buscar_em_largura,
    buscar_em_profundidade,
    buscar_profundidade_limitada,
    caminho_respeita_regras,
)
from src.problema import (
    ENCHER_3,
    ENCHER_5,
    ESVAZIAR_3,
    ESVAZIAR_5,
    TRANSFERIR_3_PARA_5,
    TRANSFERIR_5_PARA_3,
    ProblemaRecipientes,
)


@pytest.fixture
def problema():
    return ProblemaRecipientes()


def test_estado_inicial(problema):
    assert problema.initial == (0, 0)


def test_objetivos_validos(problema):
    assert problema.goal_test((5, 2))
    assert problema.goal_test((4, 3))


def test_nao_objetivos(problema):
    for estado in ((0, 0), (5, 0), (3, 3), (5, 3)):
        assert problema.goal_test(estado) is False


def test_acoes_do_estado_inicial(problema):
    acoes = problema.actions((0, 0))
    assert ENCHER_5 in acoes
    assert ENCHER_3 in acoes
    assert ESVAZIAR_5 not in acoes
    assert ESVAZIAR_3 not in acoes
    assert TRANSFERIR_5_PARA_3 not in acoes
    assert TRANSFERIR_3_PARA_5 not in acoes


def test_transicoes(problema):
    assert problema.result((0, 0), ENCHER_5) == (5, 0)
    assert problema.result((0, 0), ENCHER_3) == (0, 3)
    assert problema.result((5, 1), TRANSFERIR_5_PARA_3) == (3, 3)
    assert problema.result((2, 3), TRANSFERIR_3_PARA_5) == (5, 0)
    assert problema.result((5, 3), ESVAZIAR_5) == (0, 3)
    assert problema.result((5, 3), ESVAZIAR_3) == (5, 0)


def test_acoes_invalidas_nao_aparecem(problema):
    assert ENCHER_5 not in problema.actions((5, 0))
    assert ENCHER_3 not in problema.actions((0, 3))
    assert ESVAZIAR_5 not in problema.actions((0, 2))
    assert ESVAZIAR_3 not in problema.actions((4, 0))
    assert TRANSFERIR_5_PARA_3 not in problema.actions((0, 1))
    assert TRANSFERIR_5_PARA_3 not in problema.actions((4, 3))
    assert TRANSFERIR_3_PARA_5 not in problema.actions((1, 0))
    assert TRANSFERIR_3_PARA_5 not in problema.actions((5, 2))


def test_todos_os_estados_respeitam_capacidade(problema):
    """As 24 combinações válidas não são, todas, alcançáveis a partir de (0, 0)."""
    assert 6 * 4 == 24
    for x in range(6):
        for y in range(4):
            estado = (x, y)
            for acao in problema.actions(estado):
                proximo = problema.result(estado, acao)
                nx, ny = proximo
                assert 0 <= nx <= 5
                assert 0 <= ny <= 3
                assert proximo != estado
                assert proximo not in ((6, 0), (2, 4), (-1, 3))


def test_dezesseis_estados_alcancaveis_a_partir_do_inicial(problema):
    """Percorre o grafo da modelagem com um conjunto.

    Não implementa busca em largura, profundidade nem outra estratégia do
    trabalho. Só confirma quais estados actions() e result() alcançam.
    """
    visitados = {(0, 0)}
    borda = {(0, 0)}

    while borda:
        estado = borda.pop()
        for acao in problema.actions(estado):
            sucessor = problema.result(estado, acao)
            if sucessor not in visitados:
                visitados.add(sucessor)
                borda.add(sucessor)

    assert len(visitados) == 16
    assert (0, 0) in visitados
    assert (5, 2) in visitados
    assert (4, 3) in visitados


def test_bfs_encontra_solucao_valida(problema):
    no = breadth_first_graph_search(problema)
    assert no is not None
    assert problema.goal_test(no.state)
    assert no.state[0] + no.state[1] == 7

    estados = no.path_states()
    acoes = no.solution()
    assert estados[0] == (0, 0)
    assert len(acoes) == no.depth
    assert no.path_cost == no.depth

    for indice, acao in enumerate(acoes):
        atual = estados[indice]
        proximo = estados[indice + 1]
        assert acao in problema.actions(atual)
        assert problema.result(atual, acao) == proximo
        px, py = proximo
        assert 0 <= px <= 5
        assert 0 <= py <= 3


@pytest.mark.parametrize(
    "executor",
    [
        pytest.param(buscar_em_largura, id="largura"),
        pytest.param(buscar_em_profundidade, id="profundidade"),
        pytest.param(
            lambda problema: buscar_profundidade_limitada(problema, 8),
            id="profundidade_limitada",
        ),
        pytest.param(buscar_aprofundamento_iterativo, id="aprofundamento_iterativo"),
    ],
)
def test_estrategias_devolvem_caminho_valido(problema, executor):
    resultado = executor(problema)
    assert resultado["status"] == "solucao"
    assert caminho_respeita_regras(problema, resultado)
    assert resultado["passos"] == resultado["profundidade"]
    assert resultado["custo"] == resultado["profundidade"]
