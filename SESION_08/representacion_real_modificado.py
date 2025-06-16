import random
import numpy as np
import pandas as pd
import json

df = pd.read_csv('SESION_08/algoritmos_evolutivos-s8_lab/notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    cromosoma = []
    for i in range(39):
        pesos = [random.random() for _ in range(3)]
        suma = sum(pesos)
        pesos_norm = [p/suma for p in pesos]
        cromosoma.extend(pesos_norm)
    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': []}
    examenes = ['A', 'B', 'C']
    
    alumnos_disponibles = list(range(39))
    contadores = {'A': 0, 'B': 0, 'C': 0}
    
    while alumnos_disponibles:
        mejor_alumno = None
        mejor_examen = None
        mejor_valor = -1
        
        for alumno in alumnos_disponibles:
            idx = alumno * 3
            for i, examen in enumerate(examenes):
                if contadores[examen] < 13:
                    valor = cromosoma[idx + i]
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_alumno = alumno
                        mejor_examen = examen
        
        if mejor_alumno is not None:
            asignaciones[mejor_examen].append(mejor_alumno)
            contadores[mejor_examen] += 1
            alumnos_disponibles.remove(mejor_alumno)
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)
    
    promedios = {}
    varianzas = {}
    
    for examen in ['A', 'B', 'C']:
        indices = asignaciones[examen]
        notas_examen = [notas[i] for i in indices]
        promedios[examen] = np.mean(notas_examen)
        varianzas[examen] = np.var(notas_examen)
    
    desv_promedios = np.std(list(promedios.values()))
    promedio_varianzas = np.mean(list(varianzas.values()))
    
    fitness = -desv_promedios - 0.1 * promedio_varianzas
    return fitness

def cruce(padre1, padre2):
    hijo = []
    for i in range(39):
        idx = i * 3
        if random.random() < 0.5:
            genes = padre1[idx:idx+3]
        else:
            genes = padre2[idx:idx+3]
        
        genes = [g + random.gauss(0, 0.1) for g in genes]
        genes = [max(0, g) for g in genes]
        suma = sum(genes)
        if suma > 0:
            genes = [g/suma for g in genes]
        else:
            genes = [1/3, 1/3, 1/3]
        
        hijo.extend(genes)
    
    return hijo

def mutacion_gaussiana(cromosoma, sigma=0.1):
    cromosoma_mutado = cromosoma.copy()

    for i in range(39):
        idx = i * 3
        # Aplicar mutación gaussiana a cada peso
        pesos_mutados = [cromosoma_mutado[idx + j] + random.gauss(0, sigma) for j in range(3)]
        # Asegurarse de que los pesos no sean negativos
        pesos_mutados = [max(0, peso) for peso in pesos_mutados]
        # Normalizar los pesos
        suma = sum(pesos_mutados)
        if suma > 0:
            pesos_mutados = [peso / suma for peso in pesos_mutados]
        else:
            # Si todos los pesos son cero, asignar pesos uniformes
            pesos_mutados = [1/3, 1/3, 1/3]

        cromosoma_mutado[idx:idx+3] = pesos_mutados

    return cromosoma_mutado


def algoritmo_genetico(generaciones=150, tam_poblacion=100, sigma=0.1):
    poblacion = [crear_cromosoma() for _ in range(tam_poblacion)]
    historial_fitness = []  # Lista para guardar el historial de fitness

    mejor_global_fitness = float('-inf')
    mejor_global_cromosoma = None

    for gen in range(generaciones):
        fitness_scores = [(crom, calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        historial_fitness.append(fitness_scores[0][1])  # Guardar el mejor fitness de esta generación

        if fitness_scores[0][1] > mejor_global_fitness:
            mejor_global_fitness = fitness_scores[0][1]
            mejor_global_cromosoma = fitness_scores[0][0].copy()

        nueva_poblacion = []

        elite = int(tam_poblacion * 0.1)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])

        while len(nueva_poblacion) < tam_poblacion:
            padre1 = random.choice(poblacion[:tam_poblacion//4])
            padre2 = random.choice(poblacion[:tam_poblacion//4])

            hijo = cruce(padre1, padre2)
            hijo = mutacion_gaussiana(hijo, sigma)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        if gen % 30 == 0:
            print(f"Generación {gen}: Mejor fitness = {fitness_scores[0][1]:.4f}")

    return mejor_global_cromosoma, historial_fitness

# Probar con diferentes valores de sigma
sigmas = [0.05, 0.1, 0.2]

for sigma in sigmas:
    print(f"\nREPRESENTACIÓN REAL con sigma={sigma}")
    print("Problema: Optimizar distribución de alumnos usando pesos probabilísticos")
    print("Cromosoma: 117 valores reales (39 alumnos × 3 pesos normalizados)")
    print("Gen: [0.2, 0.5, 0.3] representa probabilidades para exámenes A, B, C\n")

    mejor_solucion, historial_fitness = algoritmo_genetico(sigma=sigma)
    asignaciones_finales = decodificar_cromosoma(mejor_solucion)

    # Guardar los resultados en un archivo JSON
    resultados = {
        'sigma': sigma,
        'historial_fitness': historial_fitness,
        'asignaciones_finales': asignaciones_finales,
        'promedios': {examen: np.mean([notas[i] for i in asignaciones_finales[examen]]) for examen in ['A', 'B', 'C']},
        'desviacion_estandar': np.std([np.mean([notas[i] for i in asignaciones_finales[examen]]) for examen in ['A', 'B', 'C']])
    }

    with open(f'SESION_08/results-json/resultados_real_sigma_{sigma}.json', 'w') as f:
        json.dump(resultados, f)
    
    print("\nDistribución optimizada:")
    for examen in ['A', 'B', 'C']:
        indices = asignaciones_finales[examen]
        notas_examen = [notas[i] for i in indices]
        promedio = np.mean(notas_examen)
        varianza = np.var(notas_examen)
        print(f"Examen {examen}: {len(indices)} alumnos")
        print(f"  Promedio: {promedio:.2f}, Varianza: {varianza:.2f}")
        print(f"  Rango de notas: [{min(notas_examen):.0f} - {max(notas_examen):.0f}]")

    print("\nAnálisis de equilibrio:")
    promedios = []
    for examen in ['A', 'B', 'C']:
        indices = asignaciones_finales[examen]
        notas_examen = [notas[i] for i in indices]
        promedios.append(np.mean(notas_examen))

    print(f"Promedios por examen: A={promedios[0]:.2f}, B={promedios[1]:.2f}, C={promedios[2]:.2f}")
    print(f"Desviación estándar entre promedios: {np.std(promedios):.4f}")
    print(f"Diferencia máxima entre promedios: {max(promedios) - min(promedios):.2f}")