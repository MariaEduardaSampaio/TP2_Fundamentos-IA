import random

def gerar_coloracao_aleatoria(grafo, cores=["vermelho", "azul", "verde", "amarelo"]):
    coloracao = {}
    for vertice in grafo.graph.keys():
        coloracao[vertice] = random.choice(cores)
    return coloracao