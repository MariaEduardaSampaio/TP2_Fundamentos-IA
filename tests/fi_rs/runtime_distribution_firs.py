import os
import numpy as np
import matplotlib.pyplot as plt

from src.utils.count_conflitcts import contar_conflitos
from src.heuristics.first_improvement_rs import first_improvement_rs
from src.utils.converter_col_to_graph import carregar_instancia_col
from src.utils.generate_random_color import gerar_coloracao_aleatoria

# Configuração do experimento
GRAFO = "huck"
CAMINHO_INSTANCIA = f"src/graph_coloring_instances/{GRAFO}.col"
cores = ["vermelho", "azul", "verde", "amarelo"]
max_steps = 1000
num_execucoes = 100

# pasta de saída para figuras
output_dir = "tests/fi_rs/reports/runtime"
os.makedirs(output_dir, exist_ok=True)

# carrega grafo
Graph = carregar_instancia_col(CAMINHO_INSTANCIA)

# métricas coletadas em N execuções independentes
conflitos_iniciais_lista = []
conflitos_finais_lista = []
steps_lista = []
tempos_lista = []

for _ in range(num_execucoes):
    coloracao_inicial = gerar_coloracao_aleatoria(Graph, cores)

    conflitos_iniciais = contar_conflitos(Graph, coloracao_inicial)

    melhor_coloracao, melhor_conflitos, elapsed_time, steps_usados = first_improvement_rs(
        grafo=Graph,
        coloracao_inicial=coloracao_inicial,
        cores=cores,
        max_steps=max_steps
    )

    conflitos_iniciais_lista.append(conflitos_iniciais)
    conflitos_finais_lista.append(melhor_conflitos)
    steps_lista.append(steps_usados)
    tempos_lista.append(elapsed_time)

# Estatísticas resumidas

def resumo_stats(nome, valores):
    arr = np.array(valores)
    stats = {
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "media": float(np.mean(arr)),
        "mediana": float(np.median(arr)),
        "n": len(arr),
    }
    print(f"===== {nome} =====")
    print(f"min     = {stats['min']}")
    print(f"max     = {stats['max']}")
    print(f"media   = {stats['media']}")
    print(f"mediana = {stats['mediana']}")
    print(f"n       = {stats['n']}\n")
    return stats

def anotar_estatisticas_boxplot(stats, x_text=1.2, delta=0.02):
    """
    Escreve min / mediana / média / max ao lado do boxplot,
    evitando sobreposição vertical com deslocamento mínimo 'delta'.
    """
    valores = [stats["min"], stats["mediana"], stats["media"], stats["max"]]
    labels = ["min", "mediana", "media", "max"]

    pares = sorted(zip(valores, labels), key=lambda x: x[0])
    ultima_y = None

    for valor, label in pares:
        y_pos = valor
        if ultima_y is not None and abs(y_pos - ultima_y) < delta:
            y_pos = ultima_y + delta
        plt.text(x_text, y_pos, f"{label} = {stats[label]:.4f}", va="center")
        ultima_y = y_pos

resumo_stats("Conflitos iniciais", conflitos_iniciais_lista)
stats_conflitos = resumo_stats("Conflitos finais", conflitos_finais_lista)
stats_tempo = resumo_stats("Tempo de execução (s)", tempos_lista)

# Função auxiliar: ECDF (distribuição acumulada empírica)

def plot_ecdf(valores, xlabel, ylabel, titulo, output_path):
    """
    Plota a ECDF (função distribuição acumulada empírica).
    x = valores ordenados
    y = proporção de execuções com valor <= x
    """
    arr = np.sort(np.array(valores))
    n = len(arr)
    y = np.arange(1, n + 1) / n

    plt.figure()
    plt.step(arr, y, where="post")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)

# Função auxiliar: scatter tempo x conflito

def plot_scatter_tempo_conflitos(tempos, conflitos, titulo, output_path):
    """
    Cada ponto representa uma execução da heurística.
    Eixo X: tempo (s)
    Eixo Y: conflitos finais
    """
    plt.figure()
    plt.scatter(tempos, conflitos, alpha=0.7)
    plt.xlabel("Tempo de execução (s)")
    plt.ylabel("Conflitos finais")
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)

# Gráfico 1: Distribuição acumulada dos conflitos finais

plot_ecdf(
    conflitos_finais_lista,
    xlabel="Conflitos finais após FI-RS",
    ylabel="Proporção de execuções ≤ x",
    titulo="Distribuição acumulada dos conflitos finais (FI-RS)",
    output_path=os.path.join(output_dir, f"{GRAFO}_firs_ecdf_conflitos.png")
)

# Gráfico 2: Boxplot dos conflitos finais

vals_conflitos = np.array(conflitos_finais_lista)

plt.figure()
plt.boxplot(vals_conflitos, vert=True)
plt.ylabel("Conflitos finais após FI-RS")
plt.title("Boxplot dos conflitos finais (FI-RS)")

anotar_estatisticas_boxplot(stats_conflitos, x_text=1.2, delta=1.0)

plt.xlim(0.5, 1.8)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"{GRAFO}_firs_boxplot_conflitos.png"), dpi=300)

# Gráfico 3: Distribuição acumulada do tempo de execução

plot_ecdf(
    tempos_lista,
    xlabel="Tempo de execução (s)",
    ylabel="Proporção de execuções ≤ t",
    titulo="Distribuição acumulada do tempo de execução (FI-RS)",
    output_path=os.path.join(output_dir, f"{GRAFO}_firs_ecdf_tempo.png")
)

# Gráfico 4: Boxplot do tempo de execução

vals_tempo = np.array(tempos_lista)

plt.figure()
plt.boxplot(vals_tempo, vert=True)
plt.ylabel("Tempo de execução (s)")
plt.title("Boxplot do tempo de execução (FI-RS)")

anotar_estatisticas_boxplot(stats_tempo, x_text=1.2, delta=0.0005)

plt.xlim(0.5, 1.8)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, f"{GRAFO}_firs_boxplot_tempo.png"), dpi=300)

# Gráfico 5: Dispersão tempo x conflitos finais

plot_scatter_tempo_conflitos(
    tempos_lista,
    conflitos_finais_lista,
    titulo="Relação entre tempo de execução e conflitos finais (FI-RS)",
    output_path=os.path.join(output_dir, f"{GRAFO}_firs_scatter_tempo_vs_conflitos.png")
)
