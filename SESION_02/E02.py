# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 05/05/2025

import numpy as np  

capital = 15.0

pasaje_bus = 2.50
pasaje_combi = 3.00
pasaje_tren = 1.80

precios_pasaje = np.array([pasaje_bus, pasaje_combi, pasaje_tren])

max_pasajes = np.floor(capital/precios_pasaje)

mayor_cantidad = int(max_pasajes.max())
indice_mayor = max_pasajes.argmax()

medios_transporte = ['Bus', 'Combi', 'Tren']

print("1. Determinar cuántos viajes puede pagar con cada medio.")

for i in range(len(medios_transporte)):
    print(f"Pasaje en bus {medios_transporte[i]} nos permite {int(max_pasajes[i])} viajes")

print("2. Hallar el medio de transporte que le permite más viajes.")

print(f"El {medios_transporte[indice_mayor]} es el mejor ya que nos permite tener {mayor_cantidad} viajes.")