import pandas as pd
import random

# Paso 1: Leer el archivo
df = pd.read_csv('SESION_05/dataset/grades.csv')

parciales = ['Parcial1', 'Parcial2', 'Parcial3']

# Paso 2: Función de aptitud
def fitness(offset):
    df_offset = df.copy()
    df_offset[parciales] = df_offset[parciales] + offset

    # Limita las notas entre 0 y 20
    df_offset[parciales] = df_offset[parciales].clip(0, 20)

    # Calcula promedio final por alumno
    df_offset['Promedio'] = df_offset[parciales].mean(axis=1)

    # % de aprobados (nota >= 11)
    aprobados = (df_offset['Promedio'] >= 11).mean()

    # Penalización si el promedio general excede 14
    promedio_general = df_offset['Promedio'].mean()
    if promedio_general > 14:
        return aprobados - (promedio_general - 14) * 0.1  # penaliza suavemente
    return aprobados

# Paso 3: Hill Climbing
current_offset = 0.0
best_fitness = fitness(current_offset)

for _ in range(100):  # número de iteraciones
    step = random.choice([-0.5, 0.5])
    new_offset = current_offset + step

    if -5 <= new_offset <= 5:
        new_fitness = fitness(new_offset)

        if new_fitness > best_fitness:
            current_offset = new_offset
            best_fitness = new_fitness

# Paso 4: Resultado
df_final = df.copy()
df_final[parciales] = df_final[parciales] + current_offset
df_final[parciales] = df_final[parciales].clip(0, 20)
df_final['Promedio'] = df_final[parciales].mean(axis=1)

print(f"Mejor offset encontrado: {current_offset:.1f}")
print(f"Porcentaje de aprobados: {(df_final['Promedio'] >= 11).mean() * 100:.2f}%")
print(f"Promedio general: {df_final['Promedio'].mean():.2f}")
