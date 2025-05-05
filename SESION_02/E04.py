# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 05/05/2025


import pandas as pd 

datos = {
    'Dias': ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'],
    'Gasto': [4.0, 3.5, 5.0, 4.2, 3.8]
}

print("\n1. Pasar esa lista a un DataFrame con columna Gasto.")
df = pd.DataFrame(datos)
print(df.head())

print("\n2. Calcular el gasto total y el gasto medio de la semana.")
print(df['Gasto'].describe())
print(f"Gasto total: {df['Gasto'].sum()}")
print(f"Gasto Medio: {df['Gasto'].mean()}")

print("\n3. Identificar los días en que gastó más que el promedio.")
gasto_mayor_promedio = df[df['Gasto'] > df['Gasto'].mean()]
print(gasto_mayor_promedio)
