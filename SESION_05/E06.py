"""
Selección de problemas de examen: Hay 30 preguntas con dificultad y 
tiempo estimado (min). El examen dura 90 min y debe tener dificultad 
total entre 180-200.

1) Hill climbing sobre subconjuntos (bitstring).
"""

import pandas as pd
import random
import numpy as np

# Leer datos
df = pd.read_csv("SESION_05/dataset/examquestion.csv")

# Parámetros
tiempo_max = 90
dificultad_min = 180
dificultad_max = 200
num_preguntas = len(df)

# Función de aptitud
def aptitud(bitstring, df):
    tiempo_total = 0
    dificultad_total = 0

    for i, bit in enumerate(bitstring):
        if bit:
            tiempo_total += df.iloc[i]['Time_min']
            dificultad_total += df.iloc[i]['Difficulty']

    if tiempo_total > tiempo_max:
        return float('-inf')
    if not (dificultad_min <= dificultad_total <= dificultad_max):
        return float('-inf')
    return dificultad_total

# Genera vecino: cambia un bit
def vecino(bitstring):
    nuevo = bitstring.copy()
    i = random.randint(0, len(bitstring) - 1)
    nuevo[i] = 1 - nuevo[i]
    return nuevo

# Hill climbing
def hill_climbing(df, iteraciones=1000):
    # Solución inicial aleatoria
    actual = [random.randint(0, 1) for _ in range(len(df))]
    mejor = actual
    mejor_apt = aptitud(actual, df)

    for _ in range(iteraciones):
        candidato = vecino(actual)
        apt = aptitud(candidato, df)
        if apt > mejor_apt:
            mejor = candidato
            mejor_apt = apt
            actual = candidato

    return mejor, mejor_apt

# Ejecutar
solucion, dificultad = hill_climbing(df)

# Mostrar preguntas seleccionadas
preguntas = df[[bool(b) for b in solucion]]
tiempo_total = preguntas['Time_min'].sum()

print("Preguntas seleccionadas:")
print(preguntas[['QuestionID', 'Difficulty', 'Time_min']])
print(f"\nDificultad total: {dificultad}")
print(f"Tiempo total: {tiempo_total} min")
