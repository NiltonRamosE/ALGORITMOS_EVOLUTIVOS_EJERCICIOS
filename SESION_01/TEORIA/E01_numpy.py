import numpy as np
import matplotlib.pyplot as plt
# Es necesario instalar las librerías si no están instaladas:
# pip install numpy
# pip install matplotlib

# Parámetros del problema
max_horas_trabajo = 120
horas_artesania_A = 2
horas_artesania_B = 3
ganancia_artesania_A = 50
ganancia_artesania_B = 80
min_artesania_A = 10
min_artesania_B = 5

# Crear mallas de valores posibles para A y B
A_vals = np.arange(min_artesania_A, max_horas_trabajo // horas_artesania_A + 1)
B_vals = np.arange(min_artesania_B, max_horas_trabajo // horas_artesania_B + 1)

# Variables para almacenar el máximo
max_ganancia = 0
optimo_A = 0
optimo_B = 0

# Explorar todas las combinaciones posibles
for A in A_vals:
    for B in B_vals:
        horas_usadas = horas_artesania_A * A + horas_artesania_B * B
        if horas_usadas <= max_horas_trabajo:
            ganancia = ganancia_artesania_A * A + ganancia_artesania_B * B
            if ganancia > max_ganancia:
                max_ganancia = ganancia
                optimo_A = A
                optimo_B = B

# Mostrar resultados
print(f"Máxima ganancia: S/ {max_ganancia}")
print(f"Cantidad de artesanía A: {optimo_A}")
print(f"Cantidad de artesanía B: {optimo_B}")

# ----------------------
# Graficar la región factible
# ----------------------

# Crear un grid para graficar la región factible
A_grid, B_grid = np.meshgrid(A_vals, B_vals)
horas_grid = horas_artesania_A * A_grid + horas_artesania_B * B_grid
region_factible = (horas_grid <= max_horas_trabajo)

plt.figure(figsize=(10, 6))
plt.title("Región factible y solución óptima")
plt.xlabel("Cantidad de artesanía A")
plt.ylabel("Cantidad de artesanía B")

# Graficar región factible
plt.contourf(A_grid, B_grid, region_factible, levels=[0.5, 1], colors=['lightblue'], alpha=0.5)

# Dibujar líneas de restricción
x_line = np.linspace(min_artesania_A, max(A_vals), 200)
y_line = (max_horas_trabajo - horas_artesania_A * x_line) / horas_artesania_B
plt.plot(x_line, y_line, 'k--', label='2A + 3B = 120')

# Marcar restricciones mínimas
plt.axvline(min_artesania_A, color='orange', linestyle=':', label='Mínimo A = 10')
plt.axhline(min_artesania_B, color='green', linestyle=':', label='Mínimo B = 5')

# Marcar solución óptima
plt.plot(optimo_A, optimo_B, 'ro', label='Solución óptima')
plt.text(optimo_A + 0.5, optimo_B, f"({optimo_A}, {optimo_B})", color='red')

plt.legend()
plt.grid(True)
plt.show()
