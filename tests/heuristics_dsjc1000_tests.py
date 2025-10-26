from src.utils.count_conflitcts import contar_conflitos
from src.heuristics.first_improvement_rs import first_improvement_rs
from src.utils.converter_col_to_graph import carregar_instancia_col
from src.utils.generate_random_color import gerar_coloracao_aleatoria

# carregar grafo alvo
CAMINHO_INSTANCIA = "src/graph_coloring_instances/DSJC1000.1.col"
Example = carregar_instancia_col(CAMINHO_INSTANCIA)

# definir cenários de teste
lista_de_listas_de_cores = [
    ["vermelho", "azul", "verde", "amarelo"],
    # ["vermelho", "azul", "verde"],
    # ["vermelho", "azul"],
]

lista_de_max_steps = [1000, 2000, 3000, 4000, 5000]

resultados = []

for cores in lista_de_listas_de_cores:
    # gerar uma coloração inicial aleatória compatível com o conjunto de cores
    coloracao_inicial = gerar_coloracao_aleatoria(Example, cores)
    conflitos_iniciais = contar_conflitos(Example, coloracao_inicial)

    for max_steps in lista_de_max_steps:
        # roda FI-RS
        melhor_coloracao, melhor_conflitos, elapsed_time, steps_usados = first_improvement_rs(
            grafo=Example,
            coloracao_inicial=coloracao_inicial,
            cores=cores,
            max_steps=max_steps
        )

        resultados.append({
            "num_cores": len(cores),
            "cores": cores,
            "max_steps_param": max_steps,
            "conflitos_iniciais": conflitos_iniciais,
            "conflitos_finais": melhor_conflitos,
            "tempo_seg": elapsed_time,
            "steps_usados": steps_usados if steps_usados != 0 else max_steps,
        })

print("===== RESULTADOS FI-RS =====\n")
for r in resultados:
    print(f"{r['num_cores']} cores ({r['cores']}), max_steps={r['max_steps_param']}:")
    print(f"    conflitos iniciais = {r['conflitos_iniciais']}")
    print(f"    conflitos finais   = {r['conflitos_finais']}")
    print(f"    tempo (s)          = {r['tempo_seg']:.6f}")
    print(f"    steps usados       = {r['steps_usados']}")
    print("")
