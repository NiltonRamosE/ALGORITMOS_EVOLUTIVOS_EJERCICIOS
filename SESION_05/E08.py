"""
Ajuste de hiper-parámetros en regresión sobre dataset HousePricesUNS.csv 
(precio de alquiler universitario). Implementa hill climbing + población usando 
DEAP para optimizar (α,ridge) de un modelo Ridge. Métrica: RMSE.

1) Usa deap (creator, toolbox, algorithms) con población = 20. 
2) Operadores: mutación gaussiana pequeña, sin cruce. 
3) Selección greedily (mejor vecino). 
4) Reporta α óptimo y curva de convergencia.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from deap import base, creator, tools
import random
import matplotlib.pyplot as plt

# Leer y preparar datos
df = pd.read_csv("SESION_05/dataset/houseprices.csv")
X = df[["Rooms", "Area_m2"]].values
y = df["Price_Soles"].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Configuración DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Un solo gen: alpha ∈ [0.01, 100]
toolbox.register("attr_alpha", random.uniform, 0.01, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_alpha, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluación: RMSE (menor es mejor)
def eval_ridge(individual):
    alpha = individual[0]
    model = Ridge(alpha=alpha)
    scores = cross_val_score(model, X, y, scoring='neg_root_mean_squared_error', cv=5)
    return (-scores.mean(),)  # Minimizar RMSE

toolbox.register("evaluate", eval_ridge)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.0, indpb=1.0)
toolbox.register("select", tools.selBest)

# Hill climbing con población
def hill_climbing_deap(generations=50):
    pop = toolbox.population(n=20)
    fits = list(map(toolbox.evaluate, pop))
    best_rmse_per_gen = []

    for g in range(generations):
        new_pop = []
        for ind in pop:
            if not ind.fitness.valid:
                ind.fitness.values = toolbox.evaluate(ind)

            neighbor = toolbox.clone(ind)
            toolbox.mutate(neighbor)
            neighbor[0] = max(0.01, neighbor[0])  # Evitar valores negativos
            del neighbor.fitness.values
            neighbor.fitness.values = toolbox.evaluate(neighbor)


            if neighbor.fitness.values[0] < ind.fitness.values[0]:  # Greedy
                new_pop.append(neighbor)
            else:
                new_pop.append(ind)

    pop = new_pop
    fits = [ind.fitness.values[0] for ind in pop]
    best_rmse_per_gen.append(min(fits))


    best_ind = tools.selBest(pop, 1)[0]
    return best_ind[0], best_rmse_per_gen

# Ejecutar
alpha_optimo, curva_rmse = hill_climbing_deap()

print(f"Alpha óptimo encontrado: {alpha_optimo:.4f}")

# Graficar curva de convergencia
plt.plot(curva_rmse)
plt.xlabel("Generación")
plt.ylabel("RMSE")
plt.title("Curva de convergencia (RMSE)")
plt.grid()
plt.show()
