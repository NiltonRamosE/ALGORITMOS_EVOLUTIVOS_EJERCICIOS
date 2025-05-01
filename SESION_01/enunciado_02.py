# 1. Importamos la librería Pandas
import pandas as pd 

# 2. Creamos un diccionario
datos = {
    'Estudiante': ['Ana', 'Luis', 'María', 'Juan', 'Carla'],
    'Horas_usadas': [3, 5, 2, 4, 1]
}

# 3. Creamos un DataFrame a partir del diccionario
df = pd.DataFrame(datos)

# 4. Añadimos una nueva columna 'Costo_total' multiplicando las horas usadas por S/ 2.00
df['Costo_total'] = df['Horas_usadas'] * 2.0

# 5. Mostramos el DataFrame completo con .head()
print("Datos del laboratorio:")
print(df.head())

# 6. Calculamos estadísticas descriptivas de la columna 'Costo_total'
print("\nEstadísticas del costo total:")
print(df['Costo_total'].describe())

# 7. Filtramos los estudiantes que gastaron más de S/ 6.00
estudiantes_mayores_6 = df[df['Costo_total'] > 6.0]

# 8. Obtenemos el gasto promedio
gasto_promedio = df['Costo_total'].mean()

# 9. Imprimir resultados
print(f"\nEl gasto promedio fue de S/ {gasto_promedio:.2f}; los estudiantes que gastaron más de S/6.00 son: {list(estudiantes_mayores_6['Estudiante'])}")
