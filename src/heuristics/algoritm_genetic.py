import random
import time
import math
from src.utils.count_conflitcts import contar_conflitos

##### Funções Auxiliares para o GA

# Observação: Um indivíduo na população do GA é representado por uma coloração do grafo.
# dicionario coloracao[vértice] = cor atribuída

# Gera a população inicial de indivíduos com colorações aleatórias.
def criar_populacao_inicial(grafo, num_individuos, cores_disponiveis):
    
    # implemente a função
    populacao = []
    vertices = list(grafo.graph.keys())
    for _ in range(num_individuos):
        coloracao = {v: random.choice(cores_disponiveis) for v in vertices}
        populacao.append(coloracao)
    # a populacao pode ser modelada como uma lista de colorações aleatórias
    return populacao

# Calcula o fitness de um indivíduo usando a função contar_conflitos(grafo, coloracao).  
def calcula_fitness(individuo, grafo):
    # implemente a função
    conflitos = contar_conflitos(grafo, individuo)
    fitness = 1 / (1 + conflitos)  # evitar divisão por zero
    return fitness

#  Seleção com probabilidade proporcional a e^(-h(A)/temperatura).
#  O 'custo' h(A) é o número de conflitos.  
def selecao_com_annealing(populacao, grafo, temperatura):

    # implemente a função
    custos = [contar_conflitos(grafo, ind) for ind in populacao]  # h(A) = conflitos
    # evite under/overflow: se temperatura for 0, tratar como seleção determinística do melhor
    if temperatura <= 0:
        return custos.index(min(custos))
    pesos = [math.exp(-c / temperatura) for c in custos]
    soma = sum(pesos)
    if soma == 0:
        # fallback: seleção uniforme
        return random.randrange(len(populacao))
    probs = [p / soma for p in pesos]
    individuo_selecionado = random.choices(range(len(populacao)), weights=probs, k=1)[0]
    # retorna o indice do individuo selecionado
    return individuo_selecionado


# Faz o cruzamento de um ponto entre dois indivíduos (pai1 e pai2).
def crossover(pai1, pai2):
    
    # Seleciona um ponto de corte aleatório.
    # complete o codigo
    vertices = list(pai1.keys())
    if len(vertices) <= 1:
        return pai1.copy(), pai2.copy()
    ponto_corte = random.randint(1, len(vertices) - 1)
    filho1 = {}
    filho2 = {}
    # Combina as partes dos pais para criar dois filhos.
    # complete o codigo
    for i, v in enumerate(vertices):
        if i < ponto_corte:
            filho1[v] = pai1[v]
            filho2[v] = pai2[v]
        else:
            filho1[v] = pai2[v]
            filho2[v] = pai1[v]
    return filho1, filho2

# Escolhe aleatoriamente um vértice do indivíduo e muda sua cor aleatoriamente com probabilidade = taxa_mutacao.
def mutation(individuo, cores, taxa_mutacao):
    
    # implemente a função 
    novo = individuo.copy()
    for v in list(novo.keys()):
        if random.random() < taxa_mutacao:
            # evitar escolher mesma cor atual (opcional)
            opcoes = [c for c in cores if c != novo[v]]
            if not opcoes:
                opcoes = cores
            novo[v] = random.choice(opcoes)
    return novo

def algoritmo_genetico(grafo, num_individuos, num_geracoes, cores, taxa_mutacao, temperatura_inicial, taxa_resfriamento): 
    populacao = criar_populacao_inicial(grafo, num_individuos, cores)
    temperatura = temperatura_inicial 

    melhor_individuo = None
    melhor_fitness = -float("inf")  # inicializa com o pior valor possível
    start_time = time.time()

    for geracao in range(num_geracoes):
        # Avaliação da população
        fitness_values = [calcula_fitness(ind, grafo) for ind in populacao]

        # Atualiza o melhor indivíduo global
        for i, f in enumerate(fitness_values):
            if f > melhor_fitness:
                melhor_fitness = f
                melhor_individuo = populacao[i]

        print(f"Geração {geracao+1}: Melhor fitness = {melhor_fitness:.4f}")

        # Se não há conflitos, encontrou solução ótima
        if contar_conflitos(grafo, melhor_individuo) == 0:
            print("\n✅ Solução ótima encontrada!")
            elapsed_time = time.time() - start_time
            return melhor_individuo, 0,elapsed_time, geracao

        nova_populacao = []

        for _ in range(num_individuos // 2):
            idx1 = selecao_com_annealing(populacao, grafo, temperatura)
            idx2 = selecao_com_annealing(populacao, grafo, temperatura)
            pai1, pai2 = populacao[idx1], populacao[idx2]

            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutation(filho1, cores, taxa_mutacao)
            filho2 = mutation(filho2, cores, taxa_mutacao)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao
        temperatura *= taxa_resfriamento  # resfriamento gradual
    
    conflitos_final = contar_conflitos(grafo, melhor_individuo)
    elapsed_time = time.time() - start_time
    return melhor_individuo, conflitos_final, elapsed_time ,geracao