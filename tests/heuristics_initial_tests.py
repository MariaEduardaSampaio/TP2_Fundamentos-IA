from heuristics.algoritm_genetic import algoritmo_genetico
from src.utils.count_conflitcts import contar_conflitos
from src.utils.generate_random_color import gerar_coloracao_aleatoria
from src.graph_coloring_instances.example_graph import Example

cores = ["vermelho", "azul", "verde", "amarelo"]

# Gerar uma coloração inicial aleatória
coloracao_inicial = gerar_coloracao_aleatoria(Example, cores)

print("Coloração inicial:")
for vertice, cor in coloracao_inicial.items():
    print(f"{vertice}: {cor}")

conflitos_iniciais = contar_conflitos(Example, coloracao_inicial)
print("\nConflitos iniciais:", conflitos_iniciais)


print("\n--- Aplicando heurísticas ---\n")

# define o número máximo de passos de execução para cada heurística de busca local
max_steps = 1000

# # Random Walk
# coloracao_rw, conflitos_rw = random_walk(Example, coloracao_inicial, cores, max_steps)
# print("Random Walk (RW):")
# print(f"Conflitos finais: {conflitos_rw}")
# print(coloracao_rw)

# # Best Improvement
# coloracao_bi, conflitos_bi = best_improvement(Example, coloracao_inicial, cores, max_steps)
# print("\nBest Improvement (BI):")
# print(f"Conflitos finais: {conflitos_bi}")
# print(coloracao_bi)

# First Improvement - Random Search
#coloracao_firs, conflitos_firs = first_improvement_rs(Example, coloracao_inicial, cores, max_steps)
#print("\nFirst Improvement - Random Search (FI-RS):")
#print(f"Conflitos finais: {conflitos_firs}")
#print(coloracao_firs)

# # First Improvement - Any Conflict
# coloracao_fi_ac, conflitos_fi_ac = first_improvement_ac(Example, coloracao_inicial, cores, max_steps)
# print("\nFirst Improvement - Any Conflict (FI-AC):")
# print(f"Conflitos finais: {conflitos_fi_ac}")
# print(coloracao_fi_ac)

# # Simulated Annealing

# # define parametros do simulated annealing:
# t_0 = 10 # temperatura inicial
# alpha = 0.9 # taxa de resfriamento

# coloracao_sa, conflitos_sa = simulated_annealing(Example, coloracao_inicial, cores, max_steps, temperatura_inicial=t_0, taxa_resfriamento=alpha)
# print("\nSimulated Annealing (SA):")
# print(f"Conflitos finais: {conflitos_sa}")
# print(coloracao_sa)

# Parâmetros
NUM_INDIVIDUOS = 100
NUM_GERACOES = 500
CORES = ["vermelho", "azul", "verde", "amarelo"]
TAXA_MUTACAO = 0.05
TEMPERATURA_INICIAL = 10
TAXA_RESFRIAMENTO = 0.9

# Execução
print("--- Executando o Algoritmo Genético ---")
coloracao_ga, conflitos_ga = algoritmo_genetico(Example, NUM_INDIVIDUOS, NUM_GERACOES, CORES, TAXA_MUTACAO, TEMPERATURA_INICIAL, TAXA_RESFRIAMENTO)

# Impressão do resultado
print("\n Algoritmo Genético (GA):")
print(f"Conflitos finais: {conflitos_ga}")
print(coloracao_ga)