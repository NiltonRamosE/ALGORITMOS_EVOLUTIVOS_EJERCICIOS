"""
Optimización de presupuesto de proyectos: Tienes 8 proyectos estudiantiles con costo S/ 
y beneficio estimado. Con un máximo de S/ 10 000, busca el subconjunto con beneficio 
total máximo.

1) Usa bitstring de longitud 8. 
2) Función de aptitud: beneficio si costo ≤ presupuesto, –∞ si no. 
3) Vecino: voltear 1 bit. 
4) Entrega lista seleccionada y beneficio.
"""

import pandas as pd
import random
import numpy as np

# Leer los proyectos
df = pd.read_csv('SESION_05/dataset/projects.csv')

presupuesto_max = 10000

# Función de aptitud
def fitness(bitstring):
    total_cost = 0
    total_benefit = 0
    for i, bit in enumerate(bitstring):
        if bit == 1:
            total_cost += df.loc[i, 'Cost_Soles']
            total_benefit += df.loc[i, 'Benefit_Soles']
    if total_cost > presupuesto_max:
        return -float('inf')
    return total_benefit

# Generar vecino (voltear 1 bit)
def generar_vecino(bitstring):
    vecino = bitstring.copy()
    i = random.randint(0, len(bitstring) - 1)
    vecino[i] = 1 - vecino[i]
    return vecino

# Algoritmo de Hill Climbing
def hill_climbing(iteraciones=1000):
    actual = [random.randint(0, 1) for _ in range(len(df))]
    mejor_fitness = fitness(actual)

    for _ in range(iteraciones):
        vecino = generar_vecino(actual)
        f_vecino = fitness(vecino)
        if f_vecino > mejor_fitness:
            actual = vecino
            mejor_fitness = f_vecino

    return actual, mejor_fitness

# Ejecutar
mejor_solucion, beneficio_total = hill_climbing()

# Mostrar proyectos seleccionados
seleccionados = df[[bool(b) for b in mejor_solucion]].copy()
print("Proyectos seleccionados:")
print(seleccionados[['ProjectID', 'Cost_Soles', 'Benefit_Soles']])
print(f"\nBeneficio total: S/ {beneficio_total}")
print(f"Costo total: S/ {seleccionados['Cost_Soles'].sum()}")
