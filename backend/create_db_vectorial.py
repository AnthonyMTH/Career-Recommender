# crear_base_vectorial.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Leer el Excel
df = pd.read_excel("DondeEstudio_completo_v2_final.xlsx")
df = df[['Carrera', 'Descripcion_Carrera', 'Habilidades_Necesarias', 'Institución']].dropna()
df['texto_vector'] = df.apply(
    lambda row: f"{row['Carrera']}. {row['Descripcion_Carrera']} Habilidades necesarias: {row['Habilidades_Necesarias']}",
    axis=1
)

# 2. Generar embeddings
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
# model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['texto_vector'].tolist())

# 3. Crear colección en ChromaDB con embedding function personalizado
client = chromadb.PersistentClient(path=".chromadb")
collection_name = "recomendador_carreras"
if collection_name in [c.name for c in client.list_collections()]:
    client.delete_collection(name=collection_name)

# Crear colección sin embedding function automático
collection = client.create_collection(
    name=collection_name,
    embedding_function=None  # Desactivar el embedding function por defecto
)

# 4. Insertar documentos con embeddings pre-calculados
collection.add(
    documents=df['texto_vector'].tolist(),
    embeddings=embeddings.tolist(),  # Usar embeddings pre-calculados
    metadatas=[
        {'carrera': row['Carrera'], 'institucion': row['Institución']}
        for _, row in df.iterrows()
    ],
    ids=[str(i) for i in df.index]
)

print("✅ Base vectorial creada con éxito.")
print("🔍 Ejemplo de embedding:", embeddings[0][:5])  # Solo 5 valores para resumir
print("🧮 Dimensión del embedding:", len(embeddings[0]))
print("🔍 Carreras insertadas:", collection.count())