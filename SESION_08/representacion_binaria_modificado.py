import random
import numpy as np
import pandas as pd
import json

df = pd.read_csv('SESION_08/algoritmos_evolutivos-s8_lab/notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    # Crear un cromosoma que cumpla con la restricción de tamaño de grupo
    cromosoma = []
    asignaciones = {'A': 0, 'B': 0, 'C': 0}
    for i in range(39):
        # Asegurarse de que no se exceda el límite de 13 alumnos por examen
        if asignaciones['A'] < 13 and (asignaciones['B'] >= 13 or random.random() < 0.333):
            examen = 0
        elif asignaciones['B'] < 13 and (asignaciones['C'] >= 13 or random.random() < 0.5):
            examen = 1
        else:
            examen = 2

        asignaciones['ABC'[examen]] += 1
        genes = [0, 0, 0]
        genes[examen] = 1
        cromosoma.extend(genes)

    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': []}
    examenes = ['A', 'B', 'C']
    
    for i in range(39):
        idx = i * 3
        for j in range(3):
            if cromosoma[idx + j] == 1:
                asignaciones[examenes[j]].append(i)
                break
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)

    # Penalizar si no hay exactamente 13 alumnos en cada examen
    if any(len(asignaciones[ex]) != 13 for ex in ['A', 'B', 'C']):
        return -1000

    promedios = {}
    varianzas = {}
    rangos = {}

    for examen in ['A', 'B', 'C']:
        indices = asignaciones[examen]
        notas_examen = [notas[i] for i in indices]
        promedios[examen] = np.mean(notas_examen)
        varianzas[examen] = np.var(notas_examen)
        rangos[examen] = max(notas_examen) - min(notas_examen)

    # Penalizar alta varianza
    penalizacion_varianza = sum(varianzas.values())

    # Premiar diversidad (rango grande de notas)
    premio_diversidad = sum(rangos.values())

    # Calcular desviación estándar de los promedios
    desviacion = np.std(list(promedios.values()))

    # Fitness final: penalizar desviación y varianza, premiar diversidad
    fitness = -desviacion - 0.1 * penalizacion_varianza + 0.05 * premio_diversidad

    return fitness

def mutacion(cromosoma):
    cromosoma_mutado = cromosoma.copy()
    
    alumno1 = random.randint(0, 38)
    alumno2 = random.randint(0, 38)
    
    idx1 = alumno1 * 3
    idx2 = alumno2 * 3
    
    examen1 = [i for i in range(3) if cromosoma_mutado[idx1 + i] == 1][0]
    examen2 = [i for i in range(3) if cromosoma_mutado[idx2 + i] == 1][0]
    
    if examen1 != examen2:
        cromosoma_mutado[idx1:idx1+3] = [0, 0, 0]
        cromosoma_mutado[idx1 + examen2] = 1
        
        cromosoma_mutado[idx2:idx2+3] = [0, 0, 0]
        cromosoma_mutado[idx2 + examen1] = 1
    
    return cromosoma_mutado

def algoritmo_genetico(generaciones=100, tam_poblacion=50):
    poblacion = [crear_cromosoma() for _ in range(tam_poblacion)]
    historial_fitness = [] # Lista para guardar el historial de fitness
    for gen in range(generaciones):
        fitness_scores = [(crom, calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        historial_fitness.append(fitness_scores[0][1]) # Guardar el mejor fitness de esta generación
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

print("REPRESENTACIÓN BINARIA")
print("Problema: Distribuir 39 alumnos en 3 exámenes (A, B, C) de forma equitativa")
print("Cromosoma: 117 bits (39 alumnos × 3 bits cada uno)")
print("Gen: [0,1,0] significa alumno asignado a examen B\n")

mejor_solucion, historial_fitness = algoritmo_genetico()
asignaciones_finales = decodificar_cromosoma(mejor_solucion)

# Guardar los resultados en un archivo JSON
resultados = {
    'historial_fitness': historial_fitness,
    'asignaciones_finales': asignaciones_finales,
    'promedios': {examen: np.mean([notas[i] for i in asignaciones_finales[examen]]) for examen in ['A', 'B', 'C']},
    'desviacion_estandar': np.std([np.mean([notas[i] for i in asignaciones_finales[examen]]) for examen in ['A', 'B', 'C']])
}

with open('SESION_08/results-json/resultados_binaria.json', 'w') as f:
    json.dump(resultados, f)

print("\nDistribución final:")
for examen in ['A', 'B', 'C']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedio = np.mean(notas_examen)
    print(f"Examen {examen}: {len(indices)} alumnos, promedio = {promedio:.2f}")
    print(f"  Alumnos: {[alumnos[i] for i in indices[:5]]}... (mostrando primeros 5)")

print("\nVerificación de equilibrio:")
promedios = []
for examen in ['A', 'B', 'C']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedios.append(np.mean(notas_examen))
print(f"Desviación estándar entre promedios: {np.std(promedios):.4f}")