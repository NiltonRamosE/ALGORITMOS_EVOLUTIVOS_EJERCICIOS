# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 30/04/2025

cafeterias = ['A', 'B', 'C', 'D']
precios = [2.50, 3.00, 1.75, 2.20]
presupuesto = 10.0

cantidad_cafes = []
for precio in precios:
    cantidad = int(presupuesto // precio)
    cantidad_cafes.append(cantidad)

print("Cafés que puede comprar en cada cafetería:")
for i in range(len(cafeterias)):
    print(f"Cafetería {cafeterias[i]}: {cantidad_cafes[i]} cafés")

max_cafes = max(cantidad_cafes)
indice_max = cantidad_cafes.index(max_cafes)
cafeteria_max = cafeterias[indice_max]

print(f"\nPuede comprar más cafés en la cafetería {cafeteria_max} ({max_cafes} cafés)")

precio_min = min(precios)
indice_min = precios.index(precio_min)
cafeteria_min = cafeterias[indice_min]

print(f"\nEl precio más bajo es S/ {precio_min:.2f} en la cafetería {cafeteria_min}")
