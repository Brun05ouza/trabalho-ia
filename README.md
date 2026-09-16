# Trabalho 1 - AV1
## Inteligência Artificial e Computacional

## Grupo

Grupo 05

## Problema

Problema 03 — Recipientes com Água (5, 3), versão 1.

## Enunciado resumido

Há dois recipientes, de 5 L e de 3 L, e uma torneira. Eles começam vazios.
É possível enchê-los na torneira, esvaziá-los no chão ou passar água de um
para o outro. O objetivo é obter 7 litros de água.

## Definição formal

Estado: `(x, y)`

- `x`: quantidade no recipiente de 5 L, com `0 <= x <= 5`
- `y`: quantidade no recipiente de 3 L, com `0 <= y <= 3`

Estado inicial: `(0, 0)`

Objetivo: `x + y = 7`

O enunciado pede 7 litros, mas não diz que eles devam estar em um recipiente
específico. Como nenhum dos recipientes comporta 7 litros sozinho, o teste de
objetivo aceita qualquer estado válido cuja soma seja 7. Nesse domínio, os
únicos estados assim são `(5, 2)` e `(4, 3)`.

Espaço teórico de estados: `{0, ..., 5} × {0, ..., 3}`, isto é, 24 combinações
matematicamente válidas. Nem todas são alcançáveis a partir de `(0, 0)`.

Espaço alcançável a partir de `(0, 0)`: 16 estados. Os operadores só enchem
por completo, esvaziam por completo ou transferem até esvaziar a origem ou
encher o destino. Um estado em que os dois recipientes ficam parcialmente
cheios — nenhum vazio e nenhum cheio — não aparece nesse percurso. São 8
casos, como `(1, 1)` e `(2, 2)`.

Os testes percorrem as 24 combinações válidas só para verificar que `actions`
e `result` nunca produzem quantidades fora das capacidades. Esse percurso não
significa que a busca visite os 24 estados.

Operadores:

- encher 5 L na torneira;
- encher 3 L na torneira;
- esvaziar 5 L no chão;
- esvaziar 3 L no chão;
- transferir 5 L → 3 L, até esvaziar a origem ou encher o destino;
- transferir 3 L → 5 L, com a mesma regra.

Uma ação só é oferecida se mudar o estado. Isso evita, por exemplo, encher um
recipiente que já está cheio.

Função sucessor: aplica o operador escolhido e devolve uma nova tupla.
Na transferência, a quantidade movida é `min(origem, espaço livre no destino)`.

Custo: 1 por operação. Usa-se o `path_cost` padrão do AIMA (`c + 1`).
A quantidade de água transferida não altera o custo.

Restrições: nenhum recipiente fica negativo nem ultrapassa sua capacidade.
Não há outras restrições no enunciado. Encher pela torneira cria água e
esvaziar no chão descarta água, então o total não se conserva.

## Representação dos estados

Tupla imutável `(x, y)`, hashable, para as buscas em grafo do AIMA poderem
guardar estados explorados em um conjunto.

## Operadores

| Ação interna | Efeito |
| --- | --- |
| `ENCHER_5` | `x = 5` |
| `ENCHER_3` | `y = 3` |
| `ESVAZIAR_5` | `x = 0` |
| `ESVAZIAR_3` | `y = 0` |
| `TRANSFERIR_5_PARA_3` | move `min(x, 3 - y)` litros |
| `TRANSFERIR_3_PARA_5` | move `min(y, 5 - x)` litros |

## Estado inicial

`(0, 0)` — os dois recipientes vazios.

## Estado objetivo

Qualquer estado válido com `x + y == 7`. Não se fixa qual dos dois,
`(5, 2)` ou `(4, 3)`, a busca deve devolver.

## Estratégias utilizadas

Os algoritmos vêm do projeto [aima-python](https://github.com/aimacode/aima-python),
módulo `aima.search`. Este trabalho só modela o problema como subclasse de
`aima.search.Problem`. Nenhuma função de busca foi copiada ou reimplementada.

- **Busca em largura** (`breadth_first_graph_search`): expande o nó mais raso
  primeiro e não revisita estados. Com custo unitário, a primeira solução tem
  profundidade mínima.
- **Busca em profundidade** (`depth_first_graph_search`): segue um ramo até
  o fim antes de voltar e também evita estados já explorados. Pode devolver
  um caminho diferente, e mais longo, que o da largura.
- **Busca em profundidade limitada** (`depth_limited_search`): igual à
  profundidade, mas para no limite informado. No AIMA ela é busca em árvore:
  não descarta ciclos. Se o limite for baixo demais, devolve `'cutoff'`.
- **Aprofundamento iterativo** (`iterative_deepening_search`): repete a busca
  limitada com limite 0, 1, 2, ... até achar solução. Combina o pouco uso de
  memória da profundidade com a solução de menor profundidade da largura.

Na comparação, a busca limitada usa limite 8. O padrão da função no AIMA é 50,
mas, por não evitar ciclos, um limite alto não termina em tempo razoável.
Esse valor não foi colocado dentro do AIMA; só é passado como argumento.

## Estrutura do projeto

```
/
├── .venv/
├── vendor/
│   └── aima-python/       # clone do AIMA; não alterar
├── src/
│   ├── __init__.py
│   ├── problema.py        # definição formal (Problem)
│   ├── buscas.py          # chamadas a aima.search
│   ├── interface.py       # CLI
│   └── main.py
├── tests/
│   └── test_problema.py
├── pytest.ini                 # executa só tests/, não o vendor
├── trabalho_IAC_AV1_2026_2_1.pdf
├── README.md
├── LEIAME.txt
└── requirements.txt
```

## Como instalar

Requisito: Python 3.9 ou superior (este ambiente usa 3.12).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ./vendor/aima-python --no-deps
pip install -r requirements.txt
```

`--no-deps` instala só o pacote local `aima`, sem TensorFlow, Keras, OpenCV
ou Jupyter. A busca precisa de NumPy, exigido por `aima.utils`.

## Como executar

```powershell
python -m src.main
```

## Como executar os testes

```powershell
pytest -v
```
