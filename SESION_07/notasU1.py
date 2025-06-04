import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV con los datos de notas
df = pd.read_csv('SESION_06/notas_1u.csv')

# Mostrar resumen estadístico (count, mean, std, min, max, etc.) por tipo de examen
resumen = df.groupby('Tipo_Examen')['Nota'].describe()
print(resumen)

# Calcular los promedios de nota por tipo de examen
promedios = df.groupby('Tipo_Examen')['Nota'].mean()

# Calcular la desviación estándar por tipo de examen (mide la dispersión)
desviacion = df.groupby('Tipo_Examen')['Nota'].std()
print(desviacion.sort_values(ascending=False))  # Ordenado de mayor a menor

# Crear histogramas para cada tipo de examen para visualizar la distribución de notas
for tipo in df['Tipo_Examen'].unique():
    df[df['Tipo_Examen'] == tipo]['Nota'].hist(
        alpha=0.5,          # Transparencia para superponer gráficos
        label=f'Examen {tipo}'
    )

# Configurar el gráfico del histograma
plt.title('Distribución de notas por tipo de examen')
plt.xlabel('Nota')
plt.ylabel('Frecuencia')
plt.legend()  # Mostrar leyenda con etiquetas de cada examen
plt.show()

# Crear un boxplot para comparar visualmente la distribución de notas por examen
df.boxplot(column='Nota', by='Tipo_Examen', grid=False)

# Configurar el gráfico del boxplot
plt.title('Distribución de notas por tipo de examen')
plt.suptitle('')  # Quitar el subtítulo automático de pandas
plt.xlabel('Tipo de Examen')
plt.ylabel('Nota')
plt.show()
