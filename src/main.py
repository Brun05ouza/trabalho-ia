"""Ponto de entrada do trabalho.

Uso: python -m src.main
"""

from src.interface import executar_interface
from src.problema import ProblemaRecipientes


def main():
    executar_interface(ProblemaRecipientes())


if __name__ == "__main__":
    main()
