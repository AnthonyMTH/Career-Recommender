import pandas as pd
import numpy as np

# 1. DEFINIR LAS CARACTERÍSTICAS
caracteristicas = [
    'habilidad_logica_matematica',
    'interes_cientifico_investigativo',
    'habilidad_comunicacion_social',
    'creatividad_innovacion',
    'interes_tecnologico_digital',
    'interes_negocios_gestion',
    'vocacion_servicio_cuidado'
]

# 2. DEFINIR LOS ARQUETIPOS DE ESTUDIANTES
# Cada arquetipo tiene una 'carrera_ideal' y puntuaciones base (de 1 a 10) para cada característica.
arquetipos = [
    {
        'carrera_ideal': 'Ingeniería de Software',
        'puntuaciones': [10, 7, 5, 6, 10, 6, 3] # Las puntuaciones corresponden al orden de la lista 'caracteristicas'
    },
    {
        'carrera_ideal': 'Ingeniería Civil',
        'puntuaciones': [10, 8, 7, 7, 7, 8, 6]
    },
    {
        'carrera_ideal': 'Medicina',
        'puntuaciones': [8, 10, 8, 4, 5, 6, 10]
    },
    {
        'carrera_ideal': 'Derecho',
        'puntuaciones': [7, 8, 10, 5, 4, 8, 8]
    },
    {
        'carrera_ideal': 'Diseño Gráfico Publicitario',
        'puntuaciones': [4, 5, 7, 10, 8, 7, 4]
    },
    {
        'carrera_ideal': 'Administración y Negocios',
        'puntuaciones': [7, 6, 9, 7, 6, 10, 6]
    },
    {
        'carrera_ideal': 'Psicología',
        'puntuaciones': [6, 9, 10, 6, 4, 6, 10]
    },
    {
        'carrera_ideal': 'Arquitectura',
        'puntuaciones': [8, 6, 7, 10, 7, 7, 5]
    },
    {
        'carrera_ideal': 'Biología',
        'puntuaciones': [7, 10, 6, 5, 5, 4, 7]
    },
    {
        'carrera_ideal': 'Economía',
        'puntuaciones': [9, 8, 7, 5, 6, 10, 4]
    },
    {
        'carrera_ideal': 'Educación',
        'puntuaciones': [5, 7, 9, 7, 6, 6, 10]
    },
    {
        'carrera_ideal': 'Comunicación Audiovisual',
        'puntuaciones': [4, 6, 8, 10, 8, 7, 5]
    },
    {
        'carrera_ideal': 'Antropología',
        'puntuaciones': [5, 9, 8, 6, 3, 4, 7]
    }
]

# 3. GENERAR LOS PERFILES SIMULADOS
NUM_PERFILES_A_GENERAR = 1000
perfiles = []

for _ in range(NUM_PERFILES_A_GENERAR):
    # Elegir un arquetipo al azar
    arquetipo = np.random.choice(arquetipos)
    
    # Generar puntuaciones con una pequeña variación (ruido) para que no sean todas iguales
    puntuaciones_base = arquetipo['puntuaciones']
    puntuaciones_ruido = np.random.normal(loc=0, scale=0.5, size=len(caracteristicas))
    puntuaciones_finales = np.clip(np.round(puntuaciones_base + puntuaciones_ruido), 1, 10) # Asegura que las notas estén entre 1 y 10
    
    perfil = dict(zip(caracteristicas, puntuaciones_finales))
    perfil['carrera_ideal'] = arquetipo['carrera_ideal']
    perfiles.append(perfil)

# 4. CREAR Y GUARDAR EL DATAFRAME
df_simulado = pd.DataFrame(perfiles)

# Reordenar columnas para que 'carrera_ideal' esté al final
columnas_ordenadas = caracteristicas + ['carrera_ideal']
df_simulado = df_simulado[columnas_ordenadas]

# Guardar en un archivo CSV
ruta_archivo = 'perfiles_simulados.csv'
df_simulado.to_csv(ruta_archivo, index=False, encoding='utf-8-sig')

print(f"Dataset simulado creado con éxito.")
print(f"Se generaron {len(df_simulado)} perfiles y se guardaron en '{ruta_archivo}'.")
print("\nPrimeras 5 filas del dataset:")
print(df_simulado.head())


# FASE 2: ANÁLISIS CON RANDOM FOREST PARA DESCUBRIR IMPORTANCIA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

print("\n--- Iniciando Fase 2: Análisis de Importancia de Características ---")

# 1. Cargar el dataset que se creo
try:
    df = pd.read_csv('perfiles_simulados.csv', encoding='utf-8-sig')
    print("Dataset 'perfiles_simulados.csv' cargado correctamente.")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'perfiles_simulados.csv'. Asegúrate de ejecutar la primera parte del script.")
    exit()

# 2. Preparar los datos para el modelo
# Separar las características (X) de la etiqueta a predecir (y)
X = df[caracteristicas]
y = df['carrera_ideal']

# Convertir las etiquetas de texto (nombres de carreras) a números, porque el modelo solo entiende números
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 3. Entrenar el modelo de Random Forest
print("Entrenando el modelo de Random Forest para descubrir patrones...")
# No necesitamos dividir en train/test aquí, porque no queremos evaluar la precisión del modelo,
# sino usar todos los datos para obtener la mejor estimación de la importancia de las características.
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X, y_encoded)
print("Modelo entrenado.")

# 4. Obtener y mostrar la importancia de cada característica
importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({
    'Caracteristica': caracteristicas,
    'Importancia': importances
}).sort_values(by='Importancia', ascending=False)

print("\n--- Resultados del Análisis ---")
print("Importancia de cada característica para predecir la carrera ideal:")
print(feature_importance_df)

# 5. Visualizar los resultados
print("\nGenerando gráfico de importancia...")
plt.figure(figsize=(10, 8))
sns.barplot(x='Importancia', y='Caracteristica', data=feature_importance_df, palette='viridis')
plt.title('Importancia de las Características del Perfil del Estudiante', fontsize=16)
plt.xlabel('Puntuación de Importancia', fontsize=12)
plt.ylabel('Característica', fontsize=12)
plt.tight_layout() # Ajusta el layout para que no se corten las etiquetas

# Guardar el gráfico en un archivo
plt.savefig('importancia_caracteristicas.png')
print("Gráfico guardado como 'importancia_caracteristicas.png'")

# Mostrar el gráfico
plt.show()