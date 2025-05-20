"""
Diseño de mini-red neuronal para predicción de matrículas: Maximiza exactitud 
en clasificación (Alta-Media-Baja) evolutivamente variando nº capas (1-3), 
neuronas y tasa de aprendizaje.

1) Genotipo mixto (enteros + float). 
2) Usa mutación e hill climbing local (pequeños ajustes). 
3) Limita epochs = 20. 
4) Muestra arquitectura final y accuracy.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# --- Carga de datos ---
df = pd.read_csv("SESION_05/dataset/enrollments.csv")
X = df.iloc[:, :-1].values
y = LabelEncoder().fit_transform(df["Category"])
X = StandardScaler().fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# --- DEAP setup ---
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

def random_architecture():
    n_layers = random.randint(1, 3)
    neurons = [random.randint(5, 100) for _ in range(n_layers)]
    while len(neurons) < 3:
        neurons.append(0)  # rellenar con ceros
    lr = random.uniform(0.0001, 0.1)
    return [n_layers] + neurons + [lr]

toolbox.register("individual", tools.initIterate, creator.Individual, random_architecture)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# --- Evaluación ---
def evaluate(ind):
    n_layers, n1, n2, n3, lr = ind
    layers = tuple(n for n in [n1, n2, n3][:n_layers] if n > 0)

    if not layers:
        return (0,)

    try:
        clf = MLPClassifier(hidden_layer_sizes=layers, learning_rate_init=lr,
                            max_iter=20, random_state=1, early_stopping=True)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_val)
        acc = accuracy_score(y_val, preds)
        return (acc,)
    except:
        return (0,)

toolbox.register("evaluate", evaluate)

# --- Mutación + Hill Climbing local ---
def mutate_and_climb(ind, sigma=5):
    neighbor = ind[:]
    
    # Mutar estructura
    if random.random() < 0.5:
        neighbor[0] = random.randint(1, 3)  # n_layers
    for i in range(1, 4):
        if random.random() < 0.3:
            neighbor[i] = max(1, min(100, int(neighbor[i] + random.gauss(0, sigma))))
    if random.random() < 0.3:
        neighbor[4] = max(0.0001, min(0.1, neighbor[4] + random.gauss(0, 0.01)))

    fit_orig = evaluate(ind)[0]
    fit_new = evaluate(neighbor)[0]
    return creator.Individual(neighbor) if fit_new > fit_orig else ind

# --- Evolución principal ---
def run_evolution(gens=30, pop_size=10):
    pop = toolbox.population(n=pop_size)
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    best_scores = []

    for gen in range(gens):
        offspring = []
        for ind in pop:
            mutant = mutate_and_climb(ind)
            mutant.fitness.values = toolbox.evaluate(mutant)
            offspring.append(mutant)
        pop = tools.selBest(offspring, pop_size)
        top = tools.selBest(pop, 1)[0]
        best_scores.append(top.fitness.values[0])
        print(f"Gen {gen+1}: {top.fitness.values[0]:.4f}")

    best = tools.selBest(pop, 1)[0]
    return best, best_scores

# --- Ejecutar ---
best, scores = run_evolution()

# --- Mostrar resultados ---
print("\n🧠 Mejor arquitectura encontrada:")
print(f"Nº capas: {best[0]}")
print(f"Neuronas por capa: {[n for n in best[1:4] if n > 0]}")
print(f"Learning rate: {best[4]:.5f}")
print(f"Accuracy final: {scores[-1]:.4f}")

# --- Gráfica ---
plt.plot(scores)
plt.title("Evolución de Accuracy")
plt.xlabel("Generaciones")
plt.ylabel("Accuracy")
plt.grid()
plt.show()
