from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import chromadb

app = Flask(__name__)
CORS(app)

# Cargar modelo y base ya existente
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768 dimensiones
print(f"🧠 Modelo cargado: sentence-transformers/all-mpnet-base-v2")

# model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensiones - más rápido
client = chromadb.PersistentClient(path=".chromadb")
#collection = client.get_or_create_collection("recomendador_carreras")

collection_name = "recomendador_carreras"

try:
    collection = client.get_collection(name="recomendador_carreras")
    print("✅ Colección cargada exitosamente")
except Exception as e:
    print("❌ Error al cargar colección:", e)
    collection = None
#collection = client.get_collection(name=collection_name)


#collection_name = "recomendador_carreras"
#if collection_name in [c.name for c in client.list_collections()]:
#    client.delete_collection(name=collection_name)

#collection = client.create_collection(name=collection_name)


@app.route("/recomendar", methods=["POST"])
def recomendar():
    if collection is None:
        return jsonify({"error": "Base de datos no disponible. Ejecuta recrear_bd_mejorada.py"}), 500
    
    data = request.get_json()
    entrada = data.get("texto", "")

    print(f"🔎 Entrada recibida: {entrada}")
    embedding = model.encode([entrada])
    print("➡️ Dimensión de embedding del usuario:", len(embedding[0]))

    try:
        resultados = collection.query(
            query_embeddings=embedding,
            n_results=5,
            include=["metadatas", "distances"]
        )
        print("🧠 Resultados encontrados:", len(resultados['ids'][0]))
    except Exception as e:
        print(f"❌ Error en consulta: {e}")
        return jsonify({"error": f"Error en consulta: {str(e)}"}), 500


    respuesta = [
        {
            "carrera": m["carrera"],
            "institucion": m["institucion"],
            "similitud": round(d, 3)
        }
        for m, d in zip(resultados['metadatas'][0], resultados['distances'][0])
    ]

    return jsonify(respuesta)

if __name__ == "__main__":
    app.run(debug=True)