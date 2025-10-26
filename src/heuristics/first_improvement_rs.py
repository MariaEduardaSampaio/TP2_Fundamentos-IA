import random
import time
from src.utils.count_conflitcts import contar_conflitos

def first_improvement_rs(grafo, coloracao_inicial, cores, max_steps=1000):

    melhor_coloracao = coloracao_inicial.copy()
    melhor_conflitos = contar_conflitos(grafo, melhor_coloracao)

    vertices = list(grafo.graph.keys())

    start_time = time.time()

    steps_usados = 0

    for step in range(1, max_steps + 1):
        steps_usados = step

        v = random.choice(vertices)

        cor_atual = melhor_coloracao[v]

        nova_cor = random.choice(cores)

        # Se a cor é igual, tenta outra. Se não achar cor diferente, segue mesmo assim
        if nova_cor == cor_atual and len(cores) > 1:
            alternativas = [c for c in cores if c != cor_atual]
            if len(alternativas) > 0:
                nova_cor = random.choice(alternativas)

        # Cria uma cópia da coloração atual e aplica a mudança proposta
        tentativa = melhor_coloracao.copy()
        tentativa[v] = nova_cor

        conflitos_tentativa = contar_conflitos(grafo, tentativa)

        # Se reduziu os conflitos, então aceita a nova coloração
        if conflitos_tentativa < melhor_conflitos:
            melhor_coloracao = tentativa
            melhor_conflitos = conflitos_tentativa

            # Se chegamos a zero conflitos, chegamos no ótimo
            if melhor_conflitos == 0:
                break

    elapsed_time = time.time() - start_time

    return melhor_coloracao, melhor_conflitos, elapsed_time, steps_usados