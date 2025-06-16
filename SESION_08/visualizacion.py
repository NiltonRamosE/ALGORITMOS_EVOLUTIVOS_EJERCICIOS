import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12

# Cargar los datos de los JSON
def cargar_datos():
    datos = {}
    
    # Representación binaria
    with open('SESION_08/results-json/resultados_binaria.json') as f:
        datos['binaria'] = json.load(f)
    
    # Representación permutacional
    with open('SESION_08/results-json/resultados_permutacional.json') as f:
        datos['permutacional'] = json.load(f)
    
    # Representaciones reales (probamos con sigma=0.1 como ejemplo)
    with open('SESION_08/results-json/resultados_real_sigma_0.1.json') as f:
        datos['real'] = json.load(f)
    
    return datos

# Función para graficar la evolución del fitness
def plot_evolucion_fitness(datos):
    plt.figure(figsize=(14, 7))
    
    # Representación binaria
    plt.plot(datos['binaria']['historial_fitness'], 
             label='Binaria', linewidth=2, color='royalblue')
    
    # Representación permutacional
    plt.plot(datos['permutacional']['historial_fitness'], 
             label='Permutacional', linewidth=2, color='forestgreen')
    
    # Representación real
    plt.plot(datos['real']['historial_fitness'], 
             label='Real (σ=0.1)', linewidth=2, color='crimson')
    
    plt.title('Evolución del Fitness por Generación', fontsize=16, pad=20)
    plt.xlabel('Generación', fontsize=14)
    plt.ylabel('Fitness', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Guardar la figura
    if not os.path.exists('SESION_08/visualizaciones'):
        os.makedirs('SESION_08/visualizaciones')
    plt.savefig('SESION_08/visualizaciones/evolucion_fitness.png', bbox_inches='tight', dpi=300)
    
    # Mostrar la figura
    plt.show()
    plt.close()

# Función para graficar histogramas de notas por examen
def plot_histogramas_notas(datos, representacion):
    # Cargar datos de notas
    df = pd.read_csv('SESION_08/algoritmos_evolutivos-s8_lab/notas_1u.csv')
    notas = df['Nota'].tolist()
    
    asignaciones = datos[representacion]['asignaciones_finales']
    
    plt.figure(figsize=(14, 8))
    
    for i, examen in enumerate(['A', 'B', 'C']):
        plt.subplot(1, 3, i+1)
        notas_examen = [notas[idx] for idx in asignaciones[examen]]
        sns.histplot(notas_examen, bins=10, kde=True, color=f'C{i}')
        
        promedio = np.mean(notas_examen)
        plt.axvline(promedio, color='red', linestyle='--', linewidth=1.5)
        plt.text(promedio+0.5, plt.ylim()[1]*0.9, f'Prom: {promedio:.2f}', color='red')
        
        plt.title(f'Examen {examen}\n({len(notas_examen)} alumnos)')
        plt.xlabel('Nota')
        plt.ylabel('Frecuencia')
        plt.xlim(0, 20)
    
    plt.suptitle(f'Distribución de Notas - Representación {representacion.capitalize()}', 
                 fontsize=16, y=1.02)
    plt.tight_layout()
    
    # Guardar la figura
    plt.savefig(f'SESION_08/visualizaciones/histogramas_{representacion}.png', bbox_inches='tight', dpi=300)
    
    # Mostrar la figura
    plt.show()
    plt.close()

# Función para comparar las distribuciones de las 3 representaciones
def plot_comparacion_distribuciones(datos):
    # Cargar datos de notas
    df = pd.read_csv('SESION_08/algoritmos_evolutivos-s8_lab/notas_1u.csv')
    notas = df['Nota'].tolist()
    
    plt.figure(figsize=(16, 8))
    
    # Crear un subplot por cada representación
    for rep_idx, representacion in enumerate(['binaria', 'permutacional', 'real']):
        asignaciones = datos[representacion]['asignaciones_finales']
        
        # Crear listas de notas para cada examen
        notas_A = [notas[idx] for idx in asignaciones['A']]
        notas_B = [notas[idx] for idx in asignaciones['B']]
        notas_C = [notas[idx] for idx in asignaciones['C']]
        
        # Crear un DataFrame para seaborn
        data = []
        for nota in notas_A:
            data.append({'Examen': 'A', 'Nota': nota, 'Representacion': representacion})
        for nota in notas_B:
            data.append({'Examen': 'B', 'Nota': nota, 'Representacion': representacion})
        for nota in notas_C:
            data.append({'Examen': 'C', 'Nota': nota, 'Representacion': representacion})
        
        df_plot = pd.DataFrame(data)
        
        # Crear el subplot
        plt.subplot(1, 3, rep_idx+1)
        sns.boxplot(x='Examen', y='Nota', data=df_plot, palette=['skyblue', 'lightgreen', 'salmon'])
        
        # Añadir los promedios como puntos
        promedios = datos[representacion]['promedios']
        for i, examen in enumerate(['A', 'B', 'C']):
            plt.scatter(i, promedios[examen], color='red', zorder=10, label='Promedio' if i==0 else "")
        
        plt.title(f'Representación {representacion.capitalize()}')
        plt.ylim(0, 20)
        if rep_idx == 0:
            plt.ylabel('Nota')
            plt.legend()
        else:
            plt.ylabel('')
    
    plt.suptitle('Comparación de Distribuciones de Notas por Representación', fontsize=16, y=1.02)
    plt.tight_layout()
    
    # Guardar la figura
    plt.savefig('SESION_08/visualizaciones/comparacion_distribuciones.png', bbox_inches='tight', dpi=300)
    
    # Mostrar la figura
    plt.show()
    plt.close()

# Función para mostrar métricas comparativas
def plot_metricas_comparativas(datos):
    metricas = []
    
    for representacion in ['binaria', 'permutacional', 'real']:
        desv = datos[representacion]['desviacion_estandar']
        promedios = datos[representacion]['promedios']
        dif_max = max(promedios.values()) - min(promedios.values())
        
        metricas.append({
            'Representacion': representacion.capitalize(),
            'Desviación Estándar': desv,
            'Diferencia Máxima': dif_max,
            'Promedio A': promedios['A'],
            'Promedio B': promedios['B'],
            'Promedio C': promedios['C']
        })
    
    df_metricas = pd.DataFrame(metricas)
    
    plt.figure(figsize=(12, 6))
    
    # Gráfico de barras para desviación estándar y diferencia máxima
    df_melted = df_metricas.melt(id_vars='Representacion', 
                                value_vars=['Desviación Estándar', 'Diferencia Máxima'],
                                var_name='Métrica', value_name='Valor')
    
    sns.barplot(x='Representacion', y='Valor', hue='Métrica', data=df_melted, 
                palette=['skyblue', 'lightcoral'])
    
    plt.title('Comparación de Equilibrio entre Exámenes', fontsize=16, pad=20)
    plt.xlabel('Representación')
    plt.ylabel('Valor')
    plt.legend(title='Métrica')
    
    # Añadir los valores en las barras
    for p in plt.gca().patches:
        plt.gca().annotate(f"{p.get_height():.3f}", 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='center', 
                          xytext=(0, 10), 
                          textcoords='offset points')
    
    plt.tight_layout()
    
    # Guardar la figura
    plt.savefig('SESION_08/visualizaciones/metricas_comparativas.png', bbox_inches='tight', dpi=300)
    
    # Mostrar la figura
    plt.show()
    plt.close()

if __name__ == "__main__":
    # Cargar los datos
    datos = cargar_datos()
    
    # Generar las visualizaciones
    print("Generando visualizaciones...")
    
    # 1. Evolución del fitness
    plot_evolucion_fitness(datos)
    print("- Gráfico de evolución del fitness generado y mostrado")
    
    # 2. Histogramas de notas por examen para cada representación
    for representacion in ['binaria', 'permutacional', 'real']:
        plot_histogramas_notas(datos, representacion)
        print(f"- Histogramas para representación {representacion} generados y mostrados")
    
    # 3. Comparación de distribuciones
    plot_comparacion_distribuciones(datos)
    print("- Gráfico comparativo de distribuciones generado y mostrado")
    
    # 4. Métricas comparativas
    plot_metricas_comparativas(datos)
    print("- Gráfico de métricas comparativas generado y mostrado")
    
    print("\nVisualizaciones guardadas en: SESION_08/visualizaciones/")