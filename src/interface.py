"""Interface de linha de comando para exibir os resultados da busca."""

from src.buscas import (
    LIMITE_PADRAO,
    buscar_aprofundamento_iterativo,
    buscar_em_largura,
    buscar_em_profundidade,
    buscar_profundidade_limitada,
    comparar_estrategias,
)
from src.problema import ProblemaRecipientes

NOMES_ACOES = {
    "ENCHER_5": "Encher recipiente de 5L",
    "ENCHER_3": "Encher recipiente de 3L",
    "ESVAZIAR_5": "Esvaziar recipiente de 5L",
    "ESVAZIAR_3": "Esvaziar recipiente de 3L",
    "TRANSFERIR_5_PARA_3": "Transferir água de 5L para 3L",
    "TRANSFERIR_3_PARA_5": "Transferir água de 3L para 5L",
}

SEPARADOR = "=" * 50
LINHA = "-" * 50


def executar_interface(problema=None):
    if problema is None:
        problema = ProblemaRecipientes()

    while True:
        _mostrar_menu(problema)
        try:
            opcao = input("Opção: ").strip()
        except EOFError:
            print()
            break

        print()
        if opcao == "0":
            print("Encerrando.")
            break
        if opcao == "1":
            exibir_resultado(buscar_em_largura(problema))
        elif opcao == "2":
            exibir_resultado(buscar_em_profundidade(problema))
        elif opcao == "3":
            limite = _ler_limite()
            if limite is None:
                continue
            exibir_resultado(buscar_profundidade_limitada(problema, limite))
        elif opcao == "4":
            exibir_resultado(buscar_aprofundamento_iterativo(problema))
        elif opcao == "5":
            exibir_comparacao(comparar_estrategias(problema), LIMITE_PADRAO)
        else:
            print("Opção inválida.")


def exibir_resultado(resultado):
    print()
    print(SEPARADOR)
    print(f" {resultado['nome'].upper()}")
    print(SEPARADOR)
    print()

    if resultado["status"] != "solucao":
        print("Estado inicial:")
        print(_formatar_recipientes(resultado["estado_inicial"]))
        print()
        if resultado["status"] == "cutoff":
            print("A busca atingiu o limite de profundidade sem solução (cutoff).")
            print("Nenhum caminho foi retornado pelo AIMA.")
        elif resultado["status"] == "sem_solucao":
            print("Nenhuma solução foi encontrada.")
        else:
            print("A busca devolveu um resultado inesperado. Nada foi interpretado como solução.")
        _mostrar_tempo(resultado)
        return

    estados = resultado["estados"]
    acoes = resultado["acoes"]

    print(_formatar_passo(0, estados[0]))
    print()
    for indice, acao in enumerate(acoes, start=1):
        print(_formatar_passo(indice, estados[indice], acao))
        print()

    print("OBJETIVO ATINGIDO")
    print()
    print("Estado objetivo:")
    print(_formatar_recipientes(estados[-1]))
    print()
    print(f"Quantidade de passos: {resultado['passos']}")
    print(f"Profundidade: {resultado['profundidade']}")
    print(f"Custo: {resultado['custo']}")
    _mostrar_tempo(resultado)


def exibir_comparacao(resultados, limite):
    print()
    print(SEPARADOR)
    print(" COMPARAÇÃO DAS ESTRATÉGIAS")
    print(SEPARADOR)
    print()
    print(
        "A busca em profundidade limitada usou limite "
        f"{limite}. A tabela só registra o que cada execução devolveu."
    )
    print("Caminhos diferentes não significam, por si sós, que uma estratégia é melhor.")
    print()
    cabecalho = (
        f"{'Algoritmo':<42} {'Passos':>8} {'Profundidade':>14} "
        f"{'Custo':>8} {'Tempo':>12}"
    )
    print(cabecalho)
    print("-" * len(cabecalho))
    for resultado in resultados:
        print(
            f"{_nome_curto(resultado):<42} "
            f"{_celula(resultado, 'passos'):>8} "
            f"{_celula(resultado, 'profundidade'):>14} "
            f"{_celula(resultado, 'custo'):>8} "
            f"{resultado['tempo_ms']:>9.2f} ms"
        )
    print()


def _mostrar_menu(problema):
    x, y = problema.initial
    print()
    print(SEPARADOR)
    print("  TRABALHO 1 - INTELIGÊNCIA ARTIFICIAL")
    print(SEPARADOR)
    print()
    print("Problema:")
    print("Recipientes com Água (5L e 3L)")
    print()
    print(f"Estado inicial:\n5L: {x} litros\n3L: {y} litros")
    print()
    print("Objetivo:")
    print("Obter exatamente 7 litros no total.")
    print()
    print(LINHA)
    print()
    print("[1] Busca em Largura")
    print("[2] Busca em Profundidade")
    print("[3] Busca em Profundidade Limitada")
    print("[4] Aprofundamento Iterativo")
    print("[5] Comparar estratégias")
    print("[0] Sair")
    print()
    print(LINHA)


def _ler_limite():
    try:
        texto = input("Informe o limite de profundidade: ").strip()
    except EOFError:
        print()
        return None

    if not texto.isdigit():
        print("Informe um inteiro maior ou igual a zero.")
        return None

    limite = int(texto)
    if limite > 12:
        print(
            "Aviso: a busca limitada do AIMA não evita ciclos. "
            "Limites altos podem demorar muito."
        )
    return limite


def _formatar_passo(passo, estado, acao=None):
    linhas = [f"Passo {passo}"]
    if passo == 0:
        linhas.append("Estado inicial")
    else:
        linhas.append(f"Ação: {NOMES_ACOES.get(acao, acao)}")
    linhas.append(_formatar_recipientes(estado))
    return "\n".join(linhas)


def _formatar_recipientes(estado):
    x, y = estado
    return (
        f"Recipiente 5L: {x}L\n"
        f"Recipiente 3L: {y}L\n"
        f"Total: {x + y}L"
    )


def _mostrar_tempo(resultado):
    print(f"Tempo: {resultado['tempo_ms']:.2f} ms")
    print()


def _nome_curto(resultado):
    nome = resultado["nome"]
    if nome.startswith("Busca em Profundidade Limitada"):
        return nome.replace("Busca em Profundidade Limitada", "Prof. Limitada")
    if nome == "Aprofundamento Iterativo":
        return "Aprof. Iterativo"
    return nome


def _celula(resultado, campo):
    if resultado["status"] == "cutoff":
        return "cutoff" if campo == "passos" else "-"
    if resultado["status"] != "solucao":
        return "falha" if campo == "passos" else "-"
    return str(resultado[campo])
