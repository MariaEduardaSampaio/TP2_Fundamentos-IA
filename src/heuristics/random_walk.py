import random
import time
from src.utils.count_conflitcts import contar_conflitos

def random_walk(grafo, coloracao_inicial, cores, max_iter=1000):
    coloracao = coloracao_inicial.copy()
    conflitos = contar_conflitos(grafo, coloracao)

    start_time = time.time()

    for step in range(1, max_iter + 1):
        steps_usados = step

        vizinho = coloracao.copy()

        # Seleciona um vizinho e define aleatoriamente outra cor para ele
        v = random.choice(list(grafo.graph.keys()))
        vizinho[v] = random.choice(cores)

        novos_conflitos = contar_conflitos(grafo, vizinho)

        if novos_conflitos < conflitos:
          conflitos = novos_conflitos
          coloracao = vizinho

    # Se possível, implementar solução que permita pioras (considera minimos locais )
    elapsed_time = time.time() - start_time

    return coloracao, conflitos, elapsed_time, steps_usados