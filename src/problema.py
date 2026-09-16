"""Problema 03 — Recipientes com Água (5, 3), versão 1.

Modelagem para a classe Problem do aima-python. Os algoritmos de busca
não são implementados aqui.
"""

from aima.search import Problem

ENCHER_5 = "ENCHER_5"
ENCHER_3 = "ENCHER_3"
ESVAZIAR_5 = "ESVAZIAR_5"
ESVAZIAR_3 = "ESVAZIAR_3"
TRANSFERIR_5_PARA_3 = "TRANSFERIR_5_PARA_3"
TRANSFERIR_3_PARA_5 = "TRANSFERIR_3_PARA_5"

ACOES = (
    ENCHER_5,
    ENCHER_3,
    ESVAZIAR_5,
    ESVAZIAR_3,
    TRANSFERIR_5_PARA_3,
    TRANSFERIR_3_PARA_5,
)


class ProblemaRecipientes(Problem):
    """Dois recipientes (5 L e 3 L) e uma torneira.

    Estado: (x, y), com x no recipiente de 5 L e y no de 3 L.
    Objetivo: obter 7 litros no total, isto é, x + y == 7.
    O enunciado não exige que os 7 litros estejam em um recipiente só.
    Os únicos estados válidos que satisfazem isso são (5, 2) e (4, 3).
    """

    CAPACIDADE_5 = 5
    CAPACIDADE_3 = 3
    OBJETIVO_LITROS = 7

    def __init__(self, inicial=(0, 0)):
        super().__init__(inicial)

    def actions(self, state):
        """Ações que alteram o estado e respeitam as capacidades."""
        x, y = state
        acoes = []

        if x < self.CAPACIDADE_5:
            acoes.append(ENCHER_5)
        if y < self.CAPACIDADE_3:
            acoes.append(ENCHER_3)
        if x > 0:
            acoes.append(ESVAZIAR_5)
        if y > 0:
            acoes.append(ESVAZIAR_3)
        if x > 0 and y < self.CAPACIDADE_3:
            acoes.append(TRANSFERIR_5_PARA_3)
        if y > 0 and x < self.CAPACIDADE_5:
            acoes.append(TRANSFERIR_3_PARA_5)

        return acoes

    def result(self, state, action):
        """Estado sucessor. A transferência para no vazio ou no cheio."""
        x, y = state

        if action == ENCHER_5:
            return (self.CAPACIDADE_5, y)
        if action == ENCHER_3:
            return (x, self.CAPACIDADE_3)
        if action == ESVAZIAR_5:
            return (0, y)
        if action == ESVAZIAR_3:
            return (x, 0)
        if action == TRANSFERIR_5_PARA_3:
            espaco = self.CAPACIDADE_3 - y
            transferido = min(x, espaco)
            return (x - transferido, y + transferido)
        if action == TRANSFERIR_3_PARA_5:
            espaco = self.CAPACIDADE_5 - x
            transferido = min(y, espaco)
            return (x + transferido, y - transferido)

        raise ValueError(f"Ação desconhecida: {action}")

    def goal_test(self, state):
        """True se os dois recipientes somam exatamente 7 litros."""
        x, y = state
        return x + y == self.OBJETIVO_LITROS
