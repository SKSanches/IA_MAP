"""Execute: python menor_caminho.py mapa.json comandos_caminho.json"""

import json
import sys
from collections import deque
from pathlib import Path


MOVIMENTOS = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}


def buscar(mapa):
    """Encontra uma rota com o menor número de movimentos usando BFS."""
    custos = mapa["custos"]
    inicio = tuple(mapa["inicio"])
    objetivo = tuple(mapa["objetivo"])

    fila = deque([inicio])
    # Cada célula descoberta guarda a célula anterior e o movimento usado.
    anteriores = {inicio: None}

    while fila:
        atual = fila.popleft()
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

            vizinho = (nx, ny)
            if custos[ny][nx] is None or vizinho in anteriores:
                continue

            anteriores[vizinho] = (atual, direcao)
            fila.append(vizinho)

    raise ValueError("Não há caminho entre o início e o objetivo.")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python menor_caminho.py mapa.json comandos_caminho.json")

    mapa = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    comandos = buscar(mapa)
    if len(comandos) > 20000:
        raise ValueError("A busca deve retornar uma lista de até 20.000 comandos.")

    Path(sys.argv[2]).write_text(json.dumps(comandos, ensure_ascii=False), encoding="utf-8")
    print(f"Arquivo salvo: {sys.argv[2]} ({len(comandos)} comandos).")


if __name__ == "__main__":
    main()
