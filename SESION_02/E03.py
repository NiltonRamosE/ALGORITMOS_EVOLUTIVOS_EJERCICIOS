# Alumno: RAMOS ENCARNACION NILTON
# Fecha: 05/05/2025


import pandas as pd 

datos = {
    'Estudiante': ['Rosa', 'David', 'Elena', 'Mario', 'Paula'],
    'Dias_prestamo': [7, 10, 5, 12, 3]
}

print("\nCrear un DataFrame con esos datos.")
df = pd.DataFrame(datos)
print(df.head())

print("\nCalcular el promedio y el máximo de días de préstamo.")
print(df['Dias_prestamo'].describe())

print("\nFiltrar quiénes retuvieron el libro más de 8 días.")
retencion_libros = df[df['Dias_prestamo'] > 8.0]
print(retencion_libros)
