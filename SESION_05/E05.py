import pandas as pd
import random
from collections import defaultdict
import numpy as np

# Leer CSV
df = pd.read_csv("SESION_05/dataset/tesistas.csv")
franjas = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
num_salas = 6
max_continuas = 4

# Representación de solución: diccionario {tesistaID: (sala, franja)}
def solucion_inicial(df):
    asignacion = {}
    idx_franja = 0
    idx_sala = 0
    for i, row in df.iterrows():
        for f in franjas:
            if row[f] == 1:
                asignacion[row['TesistaID']] = (idx_sala, f)
                idx_sala = (idx_sala + 1) % num_salas
                if idx_sala == 0:
                    idx_franja = (idx_franja + 1) % len(franjas)
                break
    return asignacion

# Métrica de huecos y solapamientos
def evaluar(asignacion):
    ocupacion = defaultdict(list)
    solapamientos = 0

    # Recolectar ocupaciones por sala
    for tesista, (sala, franja) in asignacion.items():
        ocupacion[sala].append(franjas.index(franja))

    huecos_total = 0
    exceso = 0

    for sala, franjas_ocupadas in ocupacion.items():
        franjas_ocupadas.sort()
        # Contar huecos
        for i in range(1, len(franjas_ocupadas)):
            gap = franjas_ocupadas[i] - franjas_ocupadas[i - 1]
            if gap > 1:
                huecos_total += gap - 1
        # Verificar franjas continuas
        if len(franjas_ocupadas) > max_continuas:
            exceso += (len(franjas_ocupadas) - max_continuas)

    # Revisar solapamientos
    usados = defaultdict(list)
    for tesista, (sala, franja) in asignacion.items():
        usados[(sala, franja)].append(tesista)

    solapamientos = sum(len(v) - 1 for v in usados.values() if len(v) > 1)

    # Función de costo: penalizamos más los solapamientos
    costo = solapamientos * 10 + huecos_total + exceso * 5
    return costo, huecos_total, solapamientos, exceso

# Vecino: mover 1 tesista a otra sala y franja compatible
def vecino(asignacion, df):
    nuevo = asignacion.copy()
    tesista = random.choice(list(asignacion.keys()))
    opciones = df[df['TesistaID'] == tesista]

    franjas_disponibles = [f for f in franjas if opciones.iloc[0][f] == 1]
    nueva_franja = random.choice(franjas_disponibles)
    nueva_sala = random.randint(0, num_salas - 1)

    nuevo[tesista] = (nueva_sala, nueva_franja)
    return nuevo

# Hill Climbing
def hill_climbing(df, iteraciones=1000):
    actual = solucion_inicial(df)
    mejor_costo, mejor_huecos, mejor_solaps, mejor_exceso = evaluar(actual)

    for _ in range(iteraciones):
        candidato = vecino(actual, df)
        costo, huecos, solaps, exceso = evaluar(candidato)
        if costo < mejor_costo:
            actual = candidato
            mejor_costo = costo
            mejor_huecos = huecos
            mejor_solaps = solaps
            mejor_exceso = exceso

    return actual, mejor_huecos, mejor_solaps, mejor_exceso

# Ejecutar
final, huecos, solaps, exceso = hill_climbing(df)

# Mostrar calendario
print("Calendario final:")
for tesista, (sala, franja) in final.items():
    print(f"{tesista}: Sala {sala+1}, Franja {franja}")

print(f"\nHuecos totales: {huecos}")
print(f"Solapamientos: {solaps}")
print(f"Excesos de uso continuo (>4): {exceso}")
