import time
from src.utils.count_conflitcts import contar_conflitos

def dsatur(grafo, coloracao_inicial, cores_possiveis, max_steps=1000):
    inicio = time.time()

    vertices = list(grafo.graph.keys())

    coloracao = {v: None for v in vertices}

    grau_vertice = {v: grafo.out_degree(v) for v in vertices}

    steps_usados = 0

    # nº de cores distintas usadas pelos vizinhos já coloridos
    def grau_saturacao(v):
        cores_vizinhos = set()
        for viz in grafo.get_neighbors(v):
            cor_viz = coloracao[viz]
            if cor_viz is not None:
                cores_vizinhos.add(cor_viz)
        return len(cores_vizinhos)

    while any(coloracao[v] is None for v in vertices) and steps_usados < max_steps:

        melhor_vertice = None
        melhor_sat = -1
        melhor_grau = -1

        # escolher o próximo vértice:
        # 1. maior grau de saturação
        # 2. desempate: maior grau (out_degree)
        # 3. desempate final: ordem pelo nome do vértice
        for v in vertices:
            if coloracao[v] is not None:
                continue

            sat_v = grau_saturacao(v)
            grau_v = grau_vertice[v]

            if (
                sat_v > melhor_sat or
                (sat_v == melhor_sat and grau_v > melhor_grau) or
                (sat_v == melhor_sat and grau_v == melhor_grau and (melhor_vertice is None or str(v) < str(melhor_vertice)))
            ):
                melhor_vertice = v
                melhor_sat = sat_v
                melhor_grau = grau_v

        vizinhos = grafo.get_neighbors(melhor_vertice)

        # bloqueia as cores já usadas nos vizinhos
        cores_bloqueadas = set(
            coloracao[vz] for vz in vizinhos if coloracao[vz] is not None
        )

        # escolhe a primeira cor possível que não cause conflito
        cor_escolhida = None
        for c in cores_possiveis:
            if c not in cores_bloqueadas:
                cor_escolhida = c
                break

        # se não tiver cor livre, pega a primeira só pra continuar
        if cor_escolhida is None:
            cor_escolhida = cores_possiveis[0]

        coloracao[melhor_vertice] = cor_escolhida
        steps_usados += 1

    # calcula conflitos finais
    conflitos_finais = contar_conflitos(grafo, coloracao)

    elapsed_time = time.time() - inicio

    return coloracao, conflitos_finais, elapsed_time, steps_usados
