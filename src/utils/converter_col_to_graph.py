from src.utils.graph import Graph

def carregar_instancia_col(caminho_arquivo):
    """
    Lê um arquivo .col (formato DIMACS de coloração)
    e retorna um grafo (objeto Graph) com arestas não direcionais e peso 1.

    Regras:
    - Linhas que começam com 'c' são comentários
    - Linha que começa com 'p edge' contém: número_de_vertices número_de_arestas
    - Linhas que começam com 'e u v' descrevem uma aresta entre u e v
      Essas arestas são adicionadas como não-direcionais e com peso 1.
    """

    grafo = Graph()

    with open(caminho_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()

            # ignora linhas vazias
            if not linha:
                continue

            # aresta
            if linha.startswith("e"):
                partes = linha.split()

                u = "V" + partes[1]
                v = "V" + partes[2]

                # adiciona aresta não direcional com peso 1
                grafo.add_undirected_edge(u, v, 1)

    return grafo
