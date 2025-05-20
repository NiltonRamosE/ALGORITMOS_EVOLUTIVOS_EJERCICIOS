"""
Sintonización de reglas en un spam filter para correos institucionales (dataset tokenizado). 
Evoluciona umbrales de puntaje y pesos de 5 características con DEAP y operador de hill 
climbing por individuo.

1) Genotipo: 6 floats. 
2) Cada individuo aplica hill climbing local tras mutar. 
3) Fitness = F1-score sobre conjunto validación. 
4) Entrega mejores pesos y gráfica de F1 vs generación.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt

# Leer datos
df = pd.read_csv("SESION_05/dataset/emails.csv")
X = df.iloc[:, :-1].values  # 5 características
y = df["Spam"].values

# Separar en entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# Configuración DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # F1-score se maximiza
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Genotipo: 5 pesos [0,1] + 1 umbral [0,5]
toolbox.register("attr_weight", random.uniform, 0, 1)
toolbox.register("attr_threshold", random.uniform, 0, 5)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_weight,)*5 + (toolbox.attr_threshold,), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Función de predicción binaria basada en pesos y umbral
def predict(X, weights, threshold):
    scores = np.dot(X, weights)
    return (scores >= threshold).astype(int)

# Fitness: F1-score en validación
def evaluate(ind):
    weights = ind[:5]
    threshold = ind[5]
    preds = predict(X_val, weights, threshold)
    score = f1_score(y_val, preds)
    return (score,)

toolbox.register("evaluate", evaluate)

# Mutación gaussiana + hill climbing local (1 paso)
def hill_climb_mutation(ind, sigma=0.1):
    neighbor = toolbox.clone(ind)
    for i in range(len(neighbor)):
        neighbor[i] += random.gauss(0, sigma)
    neighbor = [max(0, gene) for gene in neighbor]  # evitar negativos
    neighbor[5] = min(neighbor[5], 5.0)  # limitar umbral
    fit_orig = toolbox.evaluate(ind)[0]
    fit_new = toolbox.evaluate(neighbor)[0]
    return neighbor if fit_new > fit_orig else ind

# Algoritmo principal
def run_evolution(generations=50, pop_size=20):
    pop = toolbox.population(n=pop_size)
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    best_scores = []

    for gen in range(generations):
        new_pop = []
        for ind in pop:
            mutated = hill_climb_mutation(ind)
            mutated = creator.Individual(mutated)
            mutated.fitness.values = toolbox.evaluate(mutated)
            new_pop.append(mutated)

        pop = tools.selBest(new_pop, pop_size)
        top = tools.selBest(pop, 1)[0]
        best_scores.append(top.fitness.values[0])

    best_ind = tools.selBest(pop, 1)[0]
    return best_ind, best_scores

# Ejecutar
best_ind, f1_curve = run_evolution()

print("\n🔧 Mejores pesos encontrados:")
print(f"Pesos: {best_ind[:5]}")
print(f"Umbral: {best_ind[5]:.4f}")
print(f"F1-score validación: {f1_curve[-1]:.4f}")

# Graficar curva de convergencia
plt.plot(f1_curve)
plt.xlabel("Generación")
plt.ylabel("F1-score")
plt.title("Convergencia F1-score por generación")
plt.grid()
plt.show()
