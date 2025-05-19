import pandas as pd
import random

# Leer matriz de distancias
df = pd.read_csv('SESION_05/dataset/labdistances.csv', index_col=0)

labs = df.index.tolist()

# Función para calcular la distancia total de una ruta
def calcular_distancia(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += df.loc[ruta[i], ruta[i+1]]
    # Regreso al laboratorio inicial (opcional)
    total += df.loc[ruta[-1], ruta[0]]
    return total

# Función para generar una permutación inicial aleatoria
def generar_ruta():
    ruta = labs.copy()
    random.shuffle(ruta)
    return ruta

# Función de vecindad: intercambia dos laboratorios
def generar_vecino(ruta):
    vecino = ruta.copy()
    i, j = random.sample(range(len(ruta)), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

# Algoritmo de Hill Climbing
def hill_climbing(iteraciones=1000):
    ruta_actual = generar_ruta()
    mejor_distancia = calcular_distancia(ruta_actual)

    for _ in range(iteraciones):
        ruta_vecina = generar_vecino(ruta_actual)
        distancia_vecina = calcular_distancia(ruta_vecina)

        if distancia_vecina < mejor_distancia:
            ruta_actual = ruta_vecina
            mejor_distancia = distancia_vecina

    return ruta_actual, mejor_distancia

# Ejecutar
ruta_optima, distancia_total = hill_climbing()

# Mostrar resultados
print("Ruta óptima encontrada:")
print(" → ".join(ruta_optima))
print(f"\nDistancia total: {distancia_total:.2f} metros")
