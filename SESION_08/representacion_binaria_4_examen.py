import random
import numpy as np
import pandas as pd
import json

df = pd.read_csv('SESION_08/algoritmos_evolutivos-s8_lab/notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    cromosoma = []
    asignaciones = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    
    for i in range(39):
        # Solo permitir asignar a A, B o C si el alumno tiene nota en esos exámenes
        # Asumimos que todos tienen nota en alguno de los 3 exámenes originales
        opciones = ['A', 'B', 'C']
        
        # Filtrar exámenes que no excedan el límite de 10 alumnos
        opciones_disponibles = [ex for ex in opciones if asignaciones[ex] < 10]
        
        if not opciones_disponibles:
            # Si todos los exámenes originales están llenos, asignar al nuevo examen D
            examen = 'D'
        else:
            # Asignar con probabilidad proporcional a los espacios disponibles
            pesos = [1/(asignaciones[ex]+1) for ex in opciones_disponibles]
            pesos_norm = [p/sum(pesos) for p in pesos]
            examen = np.random.choice(opciones_disponibles, p=pesos_norm)
        
        asignaciones[examen] += 1
        genes = [0, 0, 0, 0]
        genes['ABCD'.index(examen)] = 1
        cromosoma.extend(genes)

    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': [], 'D': []}
    examenes = ['A', 'B', 'C', 'D']
    
    for i in range(39):
        idx = i * 4
        for j in range(4):
            if cromosoma[idx + j] == 1:
                asignaciones[examenes[j]].append(i)
                break
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)

    # Penalizar si no hay entre 9-10 alumnos en A, B, C (D puede tener más flexibilidad)
    if any(len(asignaciones[ex]) < 9 or len(asignaciones[ex]) > 10 for ex in ['A', 'B', 'C']):
        return -1000

    promedios = {}
    varianzas = {}
    rangos = {}

    # Solo consideramos los 3 exámenes originales para el cálculo de fitness
    for examen in ['A', 'B', 'C']:
        indices = asignaciones[examen]
        notas_examen = [notas[i] for i in indices]
        promedios[examen] = np.mean(notas_examen)
        varianzas[examen] = np.var(notas_examen)
        rangos[examen] = max(notas_examen) - min(notas_examen)

    penalizacion_varianza = sum(varianzas.values())
    premio_diversidad = sum(rangos.values())
    desviacion = np.std(list(promedios.values()))

    fitness = -desviacion - 0.1 * penalizacion_varianza + 0.05 * premio_diversidad
    
    # Penalización adicional si el examen D tiene demasiados alumnos
    if len(asignaciones['D']) > 12:  # Máximo 12 alumnos en D
        fitness -= 100 * (len(asignaciones['D']) - 12)
    
    return fitness

def mutacion(cromosoma):
    cromosoma_mutado = cromosoma.copy()
    
    alumno1 = random.randint(0, 38)
    alumno2 = random.randint(0, 38)
    
    idx1 = alumno1 * 4
    idx2 = alumno2 * 4
    
    examen1 = [i for i in range(4) if cromosoma_mutado[idx1 + i] == 1][0]
    examen2 = [i for i in range(4) if cromosoma_mutado[idx2 + i] == 1][0]
    
    if examen1 != examen2:
        cromosoma_mutado[idx1:idx1+4] = [0, 0, 0, 0]
        cromosoma_mutado[idx1 + examen2] = 1
        
        cromosoma_mutado[idx2:idx2+4] = [0, 0, 0, 0]
        cromosoma_mutado[idx2 + examen1] = 1
    
    return cromosoma_mutado

def algoritmo_genetico(generaciones=200, tam_poblacion=80):
    poblacion = [crear_cromosoma() for _ in range(tam_poblacion)]
    historial_fitness = []
    
    for gen in range(generaciones):
        fitness_scores = [(crom, calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        historial_fitness.append(fitness_scores[0][1])
        
        nueva_poblacion = []
        elite = int(tam_poblacion * 0.2)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])
        
        while len(nueva_poblacion) < tam_poblacion:
            padre = random.choice(poblacion[:tam_poblacion//2])
            hijo = mutacion(padre)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        
        if gen % 20 == 0:
            mejor_fitness = fitness_scores[0][1]
            print(f"Generación {gen}: Mejor fitness = {mejor_fitness:.4f}")
    
    mejor_cromosoma = fitness_scores[0][0]
    return mejor_cromosoma, historial_fitness

print("DISTRIBUCIÓN EN 4 EXÁMENES (USANDO DATOS DE 3 EXÁMENES)")
print("Nota: El examen D es nuevo y no tiene datos históricos de notas\n")

mejor_solucion, historial_fitness = algoritmo_genetico()
asignaciones_finales = decodificar_cromosoma(mejor_solucion)

# Guardar resultados
resultados = {
    'historial_fitness': historial_fitness,
    'asignaciones_finales': asignaciones_finales,
    'promedios': {examen: np.mean([notas[i] for i in asignaciones_finales[examen]]) 
                 for examen in ['A', 'B', 'C']},  # Solo calculamos promedios para A, B, C
    'alumnos_D': [alumnos[i] for i in asignaciones_finales['D']]  # Lista de alumnos en D
}

with open('SESION_08/results-json/resultados_4examenes_binario.json', 'w') as f:
    json.dump(resultados, f)

print("\nDistribución final:")
for examen in ['A', 'B', 'C', 'D']:
    indices = asignaciones_finales[examen]
    if examen == 'D':
        print(f"Examen D (nuevo): {len(indices)} alumnos")
        print(f"  Alumnos asignados: {[alumnos[i] for i in indices[:5]]}...")
    else:
        notas_examen = [notas[i] for i in indices]
        promedio = np.mean(notas_examen)
        print(f"Examen {examen}: {len(indices)} alumnos, promedio = {promedio:.2f}")
        print(f"  Alumnos: {[alumnos[i] for i in indices[:5]]}...")

print("\nVerificación de equilibrio (solo exámenes A, B, C):")
promedios = []
for examen in ['A', 'B', 'C']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedios.append(np.mean(notas_examen))
print(f"Desviación estándar entre promedios: {np.std(promedios):.4f}")