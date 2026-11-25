# Algoritmos de busca 
Neste trabalho, usamos dois scripts para resolver os labirintos. O `menor_caminho.py` procura a rota com menos movimentos. Já o `menor_custo.py` leva em conta o terreno de cada célula. Em alguns mapas, vale a pena andar um pouco mais para evitar a água ou a lama.

## Como executar

Os scripts usam Python 3.6 ou superior e só precisam da biblioteca padrão. Depois de extrair o ZIP, coloque o mapa na pasta dos scripts e abra o terminal nessa pasta.

```shell
python menor_caminho.py mapa.json comandos_caminho.json
python menor_custo.py mapa.json comandos_custo.json
```

Em cada comando, o primeiro arquivo JSON é o mapa da fase. O segundo é o arquivo em que o programa salva os movimentos. Para testar outra fase, basta trocar `mapa.json` pelo nome ou caminho do outro mapa.

## Como funciona a busca

No mapa, `inicio` e `objetivo` têm o formato `[x, y]`, com a coluna primeiro e a linha depois. A contagem começa em zero. Para consultar o terreno, usamos `custos[y][x]`, porque a matriz está organizada por linhas. Entrar no piso custa 1, na lama custa 5 e na água custa 9. O valor `null` representa uma parede. Os dois scripts verificam os limites do mapa e só consideram os vizinhos de cima, de baixo, da esquerda e da direita que estão livres para passagem.

Para encontrar o caminho com menos movimentos, usamos a busca em largura (BFS). Ela usa uma fila para visitar primeiro as posições que ficam a um passo do início, depois as que ficam a dois passos e assim por diante. Como cada movimento conta como um passo em qualquer terreno, a primeira rota que chega ao objetivo já tem o menor número de movimentos.

Para encontrar o caminho de menor custo, usamos Dijkstra. A busca começa com custo zero e dá prioridade à posição com o menor custo acumulado. Ao avaliar um vizinho, o programa soma o custo de entrar nele ao total percorrido. Se for a primeira rota conhecida até ali ou se ela melhorar o custo anterior, o programa registra essa rota. Como cada passo aumenta o custo, quando o objetivo sai da fila de prioridade, o valor encontrado é o menor possível.

Nos dois scripts, o dicionário `anteriores` guarda de onde viemos e qual movimento usamos. Ao chegar ao objetivo, seguimos esses registros até o início e invertemos a lista para obter os comandos na ordem em que devem ser executados. Antes de gravar o arquivo, o programa verifica o limite de 20.000 movimentos do TRILHA.

## Exemplo

Para testar, salve este mapa como `mapa.json` e rode os comandos acima.

```json
{
  "custos": [
    [1, 9, 1],
    [1, 1, 1]
  ],
  "inicio": [0, 0],
  "objetivo": [2, 0]
}
```

O início e a saída ficam na primeira linha, com água entre eles. A BFS atravessa a água e grava `["direita", "direita"]` em `comandos_caminho.json`. São dois movimentos, com custo total de 10.

Dijkstra desce para a linha de piso e volta a subir na última coluna. O arquivo `comandos_custo.json` contém `["baixo", "direita", "direita", "cima"]`. O trajeto tem quatro movimentos e custa 4.

Se o início já for o objetivo, o resultado é uma lista vazia (`[]`). Se as paredes bloquearem todas as rotas, o programa informa o erro. Em caso de empate, qualquer rota que alcance o melhor resultado para o critério escolhido é válida.
