import pandas as pd
import random

"""
Asignación de tutores-pares: Dispones de una tabla “disponibilidad” 
(filas = estudiantes mentores, columnas = horarios). 
Minimiza el número de choques de horario asignando a cada mentor un bloque de 2 h.

1) Representa cada solución como lista de horarios. 
2) Función de costo = choques. 
3) Vecindad: cambiar 1 horario. 
4) Devuelve horario final y choques = 0 si posible.
"""

# Leer el archivo de disponibilidad
# Definimos la columna que será el ID en el argumento index_col
df = pd.read_csv('SESION_05/dataset/mentoravailability.csv', index_col='MentorID')

# Extraer los índices de los mentores en un array
mentores = df.index.tolist()

# Extraer los nombres de las columnas (ajenas a la del índice) en un array
slots = df.columns.tolist()

# Generar todos los bloques de 2 horas contiguos válidos
bloques = []
for i in range(len(slots) - 1):
    slot_a = slots[i]
    slot_b = slots[i + 1]
    bloques.append((slot_a, slot_b))

# Verifica si un mentor está disponible en un bloque
def bloque_disponible(mentor, bloque):
    # df.loc[fila_etiqueta, columna_etiqueta]
    return df.loc[mentor, bloque[0]] == 1 and df.loc[mentor, bloque[1]] == 1

# Generar una solución aleatoria válida
def generar_solucion():
    # Creamos un diccionario
    asignacion = {}
    for mentor in mentores:
        # Crear una lista de bloques donde el mentor sí está disponible
        bloques_disponibles = []

        for bloque in bloques:
            if bloque_disponible(mentor, bloque):
                bloques_disponibles.append(bloque)

        # Si hay al menos un bloque disponible, asignamos uno al azar
        if len(bloques_disponibles) > 0:
            bloque_elegido = random.choice(bloques_disponibles)
            asignacion[mentor] = bloque_elegido
        else:
            # Si no hay bloques disponibles, le asignamos None
            asignacion[mentor] = None
    return asignacion

# Función de costo = número de choques
def calcular_choques(asignacion):
    conteo = {}
    for bloque in asignacion.values():
        if bloque:
            #Contamos las veces que aparece cada bloque, inicializamos en 0 dentro del get()
            conteo[bloque] = conteo.get(bloque, 0) + 1
    # Choque = si más de un mentor en el mismo bloque
    choques = 0
    for c in conteo.values():
        if c > 1:  # si hay más de un mentor en ese bloque
            choques += (c - 1)  # sumamos los choques (exceso de mentores)

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
