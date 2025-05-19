import pandas as pd
import random
import numpy as np
from collections import Counter

# Leer datos
df = pd.read_csv("SESION_05/dataset/students.csv")

# Verifica que haya 20 estudiantes
assert len(df) == 20, "Debe haber exactamente 20 estudiantes."

# Agrupar por equipos: 5 equipos de 4
def crear_solucion_inicial():
    indices = list(df.index)
    random.shuffle(indices)
    return [indices[i:i+4] for i in range(0, 20, 4)]

# Función de aptitud
def calcular_aptitud(equipos):
    gpas = []
    habilidades_totales = Counter()
    penalizacion = 0

    for equipo in equipos:
        gpa_equipo = [df.loc[i, "GPA"] for i in equipo]
        gpas.append(np.mean(gpa_equipo))
        
        skills = [df.loc[i, "Skill"] for i in equipo]
        count = Counter(skills)
        habilidades_totales += count

        # Penaliza si un equipo tiene más de 2 alumnos de la misma skill
        for skill, c in count.items():
            if c > 2:
                penalizacion += (c - 2) * 10

    varianza_gpa = np.var(gpas)
    return varianza_gpa + penalizacion

# Vecino: intercambia dos alumnos de equipos distintos
def generar_vecino(equipos):
    nuevo = [list(e) for e in equipos]
    eq1, eq2 = random.sample(range(5), 2)
    i1 = random.randint(0, 3)
    i2 = random.randint(0, 3)
    nuevo[eq1][i1], nuevo[eq2][i2] = nuevo[eq2][i2], nuevo[eq1][i1]
    return nuevo

# Hill Climbing
def hill_climbing(iteraciones=1000):
    actual = crear_solucion_inicial()
    mejor = actual
    mejor_aptitud = calcular_aptitud(actual)

    for _ in range(iteraciones):
        candidato = generar_vecino(actual)
        aptitud = calcular_aptitud(candidato)
        if aptitud < mejor_aptitud:
            mejor = candidato
            mejor_aptitud = aptitud
            actual = candidato

    return mejor, mejor_aptitud

# Ejecutar
equipos_finales, aptitud_final = hill_climbing()

# Mostrar resultados
for i, equipo in enumerate(equipos_finales, 1):
    print(f"\nEquipo {i}:")
    print(df.loc[equipo][["StudentID", "GPA", "Skill"]])

# Métricas
print(f"\nAptitud final: {aptitud_final:.4f}")
