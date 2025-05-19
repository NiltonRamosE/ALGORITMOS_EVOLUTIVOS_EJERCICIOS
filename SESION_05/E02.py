import pandas as pd
import random

# Leer el archivo de disponibilidad
df = pd.read_csv('SESION_05/dataset/mentoravailability.csv', index_col='MentorID')

# Extraer mentores y slots
mentores = df.index.tolist()
slots = df.columns.tolist()

# Generar todos los bloques de 2 horas contiguos válidos
bloques = [(slots[i], slots[i+1]) for i in range(len(slots)-1)]

# Verifica si un mentor está disponible en un bloque
def bloque_disponible(mentor, bloque):
    return df.loc[mentor, bloque[0]] == 1 and df.loc[mentor, bloque[1]] == 1

# Generar una solución aleatoria válida
def generar_solucion():
    asignacion = {}
    for mentor in mentores:
        disponibles = [b for b in bloques if bloque_disponible(mentor, b)]
        if disponibles:
            asignacion[mentor] = random.choice(disponibles)
        else:
            asignacion[mentor] = None  # sin bloque válido
    return asignacion

# Función de costo = número de choques
def calcular_choques(asignacion):
    conteo = {}
    for bloque in asignacion.values():
        if bloque:
            conteo[bloque] = conteo.get(bloque, 0) + 1
    # Choque = si más de un mentor en el mismo bloque
    choques = sum(c - 1 for c in conteo.values() if c > 1)
    return choques

# Búsqueda local para minimizar choques
def hill_climbing(iteraciones=1000):
    solucion = generar_solucion()
    mejor_costo = calcular_choques(solucion)

    for _ in range(iteraciones):
        mentor = random.choice(mentores)
        actuales = [b for b in bloques if bloque_disponible(mentor, b)]
        if not actuales:
            continue
        nuevo_bloque = random.choice(actuales)
        nueva_solucion = solucion.copy()
        nueva_solucion[mentor] = nuevo_bloque

        nuevo_costo = calcular_choques(nueva_solucion)
        if nuevo_costo < mejor_costo:
            solucion = nueva_solucion
            mejor_costo = nuevo_costo
            if mejor_costo == 0:
                break

    return solucion, mejor_costo

# Ejecutar algoritmo
asignacion_final, choques_finales = hill_climbing()

# Mostrar resultados
print("Asignación final:")
for mentor, bloque in asignacion_final.items():
    print(f"{mentor}: {bloque if bloque else 'Sin bloque válido'}")

print(f"\nChoques finales: {choques_finales}")
