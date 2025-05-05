"""
    Escenario: Una pequeña empresa produce dos tipos de artesanías: A y B
    - Artesanía A requiere 2 horas de trabajo y da S/ 50 de ganancia.
    - Artesanía B requiere 3 horas de trabajo y da S/ 80 de ganancia.
    - Se dispone de un máximo de 120 horas de trabajo por semana.
    - Se deben producir al menos 10 unidades de A y 5 de B.
    Objetivo: Maximizar la ganancia semanal.
"""
max_horas_trabajo = 120
horas_artesania_A = 2
horas_artesania_B = 3
ganancia_artesania_A = 50
ganancia_artesania_B = 80
min_artesania_A = 10
min_artesania_B = 5

max_ganancia = 0
for i in range(min_artesania_A, max_horas_trabajo // horas_artesania_A + 1):
    for j in range(min_artesania_B, max_horas_trabajo // horas_artesania_B + 1):
        cantidad_horas_trabajo = horas_artesania_A * i + horas_artesania_B * j

        
        if cantidad_horas_trabajo <= max_horas_trabajo:
            print(f"2 * {i} + 3 * {j} = {cantidad_horas_trabajo} horas de trabajo")

            ganancia = ganancia_artesania_A * i + ganancia_artesania_B * j

            if ganancia > max_ganancia:
                max_ganancia = ganancia
                max_cant_artesania_A = i
                max_cant_artesania_B = j

print(f"Cantidad máxima de horas de trabajo: {horas_artesania_A * max_cant_artesania_A + horas_artesania_B * max_cant_artesania_B} horas")
print(f"Máxima ganancia: S/ {max_ganancia}")
print(f"Cantidad máxima de artesanía A: {max_cant_artesania_A}")
print(f"Cantidad máxima de artesanía B: {max_cant_artesania_B}")