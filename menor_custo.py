"""Execute: python menor_custo.py mapa.json comandos_custo.json"""

import json
import sys
from heapq import heappop, heappush
from pathlib import Path


MOVIMENTOS = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}


def buscar(mapa):
    """Encontra uma rota com o menor custo acumulado usando Dijkstra."""
    custos = mapa["custos"]
    inicio = tuple(mapa["inicio"])
    objetivo = tuple(mapa["objetivo"])

    fila = [(0, inicio)]
    melhores_custos = {inicio: 0}
    anteriores = {}

    while fila:
        custo_atual, atual = heappop(fila)
        if custo_atual != melhores_custos[atual]:
            continue

        if atual == objetivo:
            comandos = []
            while atual != inicio:
                atual, direcao = anteriores[atual]
                comandos.append(direcao)
            comandos.reverse()
            return comandos

        x, y = atual
        for direcao, (dx, dy) in MOVIMENTOS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= ny < len(custos) and 0 <= nx < len(custos[ny])):
                continue

            custo_terreno = custos[ny][nx]
            if custo_terreno is None:
                continue

            vizinho = (nx, ny)
            novo_custo = custo_atual + custo_terreno
            if vizinho in melhores_custos and novo_custo >= melhores_custos[vizinho]:
                continue

            melhores_custos[vizinho] = novo_custo
            anteriores[vizinho] = (atual, direcao)
            heappush(fila, (novo_custo, vizinho))

    raise ValueError("Não há caminho entre o início e o objetivo.")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python menor_custo.py mapa.json comandos_custo.json")

    mapa = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    comandos = buscar(mapa)
    if len(comandos) > 20000:
        raise ValueError("A busca deve retornar uma lista de até 20.000 comandos.")

    Path(sys.argv[2]).write_text(json.dumps(comandos, ensure_ascii=False), encoding="utf-8")
    print(f"Arquivo salvo: {sys.argv[2]} ({len(comandos)} comandos).")


if __name__ == "__main__":
    main()
