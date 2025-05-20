import pandas as pd
import random
"""
Curva de notas de Parciales: Dado un CSV con las calificaciones de 120 alumnos 
en tres parciales, usa hill climbing para encontrar el offset (entre –5 y +5 puntos) 
que maximiza el porcentaje de aprobados manteniendo el promedio de la clase ≤ 14.

1) Lee el archivo. 
2) Define función de aptitud (porcentaje de aprobados penalizando si promedio > 14). 
3) Itera intentando offsets aleatorios de 0.5 ptos y conserva el mejor. 
4) Reporta offset óptimo y nueva distribución.

"""
# Paso 1: Leer el archivo
df = pd.read_csv('SESION_05/dataset/grades.csv')

parciales = ['Parcial1', 'Parcial2', 'Parcial3']

# Paso 2: Función de aptitud
def fitness(offset):
    # Saco una copia del dataframe para no modificar valores
    df_offset = df.copy()

    # Sumamos el valor del offset que puede ser -5 o +5
    df_offset[parciales] = df_offset[parciales] + offset

    # Limita las notas entre 0 y 20, si la suma se ve superada o muy reducida entonces toma los valores de su lower y upper
    df_offset[parciales] = df_offset[parciales].clip(lower=0, upper=20)

    # Calcula promedio final por alumno (por fila axis=1)
    df_offset['Promedio'] = df_offset[parciales].mean(axis=1)

    # % de aprobados (nota >= 11)
    aprobados = (df_offset['Promedio'] >= 11).mean()

    # Penalización si el promedio general excede 14
    promedio_general = df_offset['Promedio'].mean()
    if promedio_general > 14:
        return aprobados - (promedio_general - 14) * 0.1  # penaliza suavemente
    return aprobados

# Paso 3: Hill Climbing

def hill_climbing(start_offset, step_size=0.5, max_iterations=100):
    # Inicializamos nuestro offset actual
    current_offset = start_offset

    # Hallamos el fitness del offset actual
    current_fitness = fitness(current_offset)

    for i in range(max_iterations):

        # Calculamos el nuevo offset de acuerdo a si se le suma 0.5 o disminuye 0.5
        new_offset = current_offset + random.choice([-step_size, step_size])

        # Comprobamos que esté dentro del rango de puntos a aumentar o disminuir
        if -5 <= new_offset <= 5:

            # Obtenemos el nuevo fitness del offset obtenido
            new_fitness = fitness(new_offset)

            # Si el nuevo fitness es mayor que el fitness anterior entonces se reemplaza
            # ya que buscamos maximizar las notas
            if new_fitness > current_fitness:
                current_offset = new_offset
                current_fitness = new_fitness
        print(f"Iteración {i+1}: Puntos = {current_offset:.4f}, Aprobados = {current_fitness:.4f}")
    return current_offset, current_fitness

# Iniciamos con un offset sin modificar las notas
current_offset = 0.0

best_offset, best_fitness = hill_climbing(current_offset)

# Paso 4: Resultado
df_final = df.copy()
df_final[parciales] = df_final[parciales] + best_offset
df_final[parciales] = df_final[parciales].clip(0, 20)
df_final['Promedio'] = df_final[parciales].mean(axis=1)
print(f"Mejor offset encontrado: {best_offset:.1f}")
print(f"Mejor aptitud encontrada: {best_fitness*100:.2f}")
print(f"Porcentaje de aprobados: {(df_final['Promedio'] >= 11).mean() * 100:.2f}%")
print(f"Promedio general: {df_final['Promedio'].mean():.2f}")
