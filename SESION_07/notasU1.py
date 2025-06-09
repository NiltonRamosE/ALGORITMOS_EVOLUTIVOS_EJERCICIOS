import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar el archivo CSV con los datos de notas
df = pd.read_csv('SESION_07/notas_1u.csv')

# Mostrar resumen estadístico (count, mean, std, min, max, etc.) por tipo de examen
resumen = df.groupby('Tipo_Examen')['Nota'].describe()
print(resumen)

# Calcular los promedios de nota por tipo de examen
promedios = df.groupby('Tipo_Examen')['Nota'].mean()

# Calcular la desviación estándar por tipo de examen (mide la dispersión)
desviacion = df.groupby('Tipo_Examen')['Nota'].std()
print(desviacion.sort_values(ascending=False))  # Ordenado de mayor a menor

# Agrupar por tipo de examen y nota, y contar la cantidad de estudiantes
conteo_notas = df.groupby(['Tipo_Examen', 'Nota']).size().reset_index(name='Cantidad')

# Estilo de seaborn
sns.set(style='whitegrid')

# Histograma con seaborn (usando KDE para ver la forma de la distribución)
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Nota', hue='Tipo_Examen', kde=True, bins=10, multiple='stack')
plt.title('Distribución de notas por tipo de examen')
plt.xlabel('Nota')
plt.ylabel('Frecuencia')
plt.show()

# Histograma interactivo
fig1 = px.histogram(df, x='Nota', color='Tipo_Examen', barmode='stack', nbins=10,
                    title='Distribución de notas por tipo de examen')
fig1.update_layout(bargap=0.1)
fig1.show()

# Boxplot interactivo
fig2 = px.box(df, x='Tipo_Examen', y='Nota', color='Tipo_Examen',
              title='Distribución de notas por tipo de examen')
fig2.show()

fig3 = px.violin(df, x='Tipo_Examen', y='Nota', color='Tipo_Examen', box=True, points='all',
                 title='Distribución de notas por tipo de examen (Violin Plot)')
fig3.show()

fig4 = px.bar(conteo_notas, x='Cantidad', y='Nota', color='Tipo_Examen',
              orientation='h', barmode='group',
              title='Cantidad de estudiantes por nota y tipo de examen')
fig4.update_layout(yaxis_title='Nota', xaxis_title='Cantidad de Estudiantes')
fig4.show()

print("Total de filas:", len(df))
print("Estudiantes únicos:", df['Alumno'].nunique())
