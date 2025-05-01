pago_por_hora = 2.00

horas_usadas = {
    "ANA": 3,
    "LUIS": 5,
    "MARÍA": 2,
    "JUAN": 4,
    "CARLA": 1,
}

costo_por_estudiante = []
for nombre, horas in horas_usadas.items():
    costo = horas * pago_por_hora
    costo_por_estudiante.append((nombre, costo))

print(costo_por_estudiante)
print("--------------------------------------------------------")

gasto_total = 0
for horas in horas_usadas.values():
    gasto_total += horas * pago_por_hora

cantidad_estudiantes = len(horas_usadas)
gasto_promedio = gasto_total / cantidad_estudiantes

print(f"Gasto promedio por estudiante: S/ {gasto_promedio:.2f}")
print("--------------------------------------------------------")
print("Estudiantes que gastaron más de S/ 6.00:")
for nombre, costo in costo_por_estudiante:
    if costo > 6.00:
        print(f"{nombre}: S/ {costo:.2f}")

