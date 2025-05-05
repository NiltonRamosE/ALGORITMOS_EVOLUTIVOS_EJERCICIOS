# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 05/05/2025

import numpy as np  

capital = 8.0

# Precio por página en cada copisteria

copisteria_A = 0.10
copisteria_B = 0.12
copisteria_C = 0.08

precios_copisteria = np.array([copisteria_A, copisteria_B, copisteria_C])

max_copias = np.floor(capital/precios_copisteria)

mayor_cantidad = int(max_copias.max())
indice_mayor = max_copias.argmax()

copisterias = ['A', 'B', 'C']

print("- Cantidad de páginas que se imprimen en cada copistería")

for i in range(len(copisterias)):
    print(f"Copisteria {copisterias[i]}: {int(max_copias[i])} páginas")

print(f"- Obtenemos el mayor presupuesto comprando en la Copistería {copisterias[indice_mayor]}")