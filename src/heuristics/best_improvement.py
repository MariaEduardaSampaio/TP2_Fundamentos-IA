import time
from src.utils.count_conflitcts import contar_conflitos


def best_improvement(grafo, coloracao_inicial, cores, max_iter=1000):

    coloracao = coloracao_inicial.copy()
    conflitos = contar_conflitos(grafo, coloracao)

    # Seleciona um vizinho iterativamente

    g = list(grafo.graph.keys())

    start_time = time.time()
    
    for i in range(max_iter):

        # criar variáveis para identificar o melhor movimento global

        melhor_vertice = None
        melhor_cor = None
        melhor_conflitos = conflitos

        # Seleciona todos os estados possíveis que a variável v pode assumir
        # e guarda o valor que traz a melhor melhoria

        for v in g:

          for cor in cores:
            coloracao_teste = coloracao.copy()
            coloracao_teste[v] = cor
            novos_conflitos = contar_conflitos(grafo, coloracao_teste)

            if novos_conflitos < conflitos:
              melhor_conflitos = novos_conflitos
              melhor_vertice = v
              melhor_cor = cor

        # Aplica mudança no grafo, em caso de melhoria

        if melhor_vertice is not None and melhor_conflitos < conflitos:
          coloracao[melhor_vertice] = melhor_cor
          conflitos = melhor_conflitos

          if conflitos == 0:
            elapsed_time = time.time() - start_time
            return coloracao, conflitos, elapsed_time, i+1

        else:
          # Mínimo local
          print("Preso em um mínimo local. Número de iterações: ", i+1)

          break

    elapsed_time = time.time() - start_time

    return coloracao, conflitos, elapsed_time, i+1