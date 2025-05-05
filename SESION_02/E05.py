# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 05/05/2025

import numpy as np  


paquete_gb = np.array([1, 2, 5, 10])

precios_paquete = np.array([5, 9, 20, 35])

print("1. Con un array de NumPy, calcular el costo por GB para cada paquete.")

costo_por_gb = precios_paquete / paquete_gb

for i in range(len(paquete_gb)):
    print(f"Paquete de {paquete_gb[i]} GB: S/ {costo_por_gb[i]:.2f} por GB")

print("2. Encontrar el paquete más económico en precio por GB.")

indice_mas_economico = costo_por_gb.argmin()
paquete_mas_economico = paquete_gb[indice_mas_economico]
precio_mas_economico = precios_paquete[indice_mas_economico]

print(f"\nEl paquete más económico por GB es el de {paquete_mas_economico} GB a S/ {precio_mas_economico} (S/ {costo_por_gb[indice_mas_economico]:.2f} por GB)")