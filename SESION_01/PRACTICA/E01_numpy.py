# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 30/04/2025

# 1. Importamos la librería NumPy
# pip install numpy
import numpy as np  

# 2. Definimos nuestro presupuesto disponible
presupuesto = 10.0

# 3. Creamos un array con los precios del café en cada cafetería
precios = np.array([2.50, 3.00, 1.75, 2.20])

# 4. Calculamos cuántos cafés puede comprar en cada cafetería (sin pasarse del presupuesto)
max_cafes = np.floor(presupuesto / precios)

# 5. Obtenemos la mayor cantidad de cafés y la posición
mayor_cantidad = int(max_cafes.max())
indice_mayor = max_cafes.argmax()

# 6. Obtenemos el precio mínimo y su posición
precio_minimo = precios.min()
indice_minimo = precios.argmin()

# 7. Lista con nombres de cafeterías
cafeterias = ['A', 'B', 'C', 'D']

# 8. Imprimir resultados
print(f"Con S/10 puedo comprar como máximo {mayor_cantidad} cafés en la cafetería {cafeterias[indice_mayor]} (precio mínimo S/{precio_minimo:.2f} en la cafetería {cafeterias[indice_minimo]})")
