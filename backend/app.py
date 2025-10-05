from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import chromadb

app = Flask(__name__)
CORS(app)

# Cargar modelo y base ya existente
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768 dimensiones
print(f"Modelo cargado: sentence-transformers/all-mpnet-base-v2")

# model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensiones - más rápido
client = chromadb.PersistentClient(path=".chromadb")
collection = None

#collection = client.get_or_create_collection("recomendador_carreras")

try:
    collection = client.get_collection(name="recomendador_carreras")
    print("Colección cargada exitosamente")
except Exception as e:
    print("Error al cargar colección:", e)
    collection = None
#collection = client.get_collection(name=collection_name)

# --- LÓGICA DE ENRIQUECIMIENTO DE PROMPT ---
# esta función usa el conocimiento que se obtuvo del análisis de Random Forest
def construir_prompt_enriquecido(descripcion_original, perfil):
    frases_adicionales = []

    # Plantillas para cada una de las características más importantes
    # 1. Habilidad Lógica-Matemática
    p_logica = perfil.get('habilidad_logica_matematica', 5)
    if p_logica >= 8:
        frases_adicionales.append("Tengo una fuerte habilidad para el razonamiento lógico y los números.")
    elif p_logica >= 6:
        frases_adicionales.append("Me siento cómodo con los números.")

    # 2. Vocación de Servicio y Cuidado
    p_servicio = perfil.get('vocacion_servicio_cuidado', 5)
    if p_servicio >= 8:
        frases_adicionales.append("Me motiva profundamente ayudar a los demás y tengo una gran vocación de servicio.")
    elif p_servicio >= 6:
        frases_adicionales.append("Disfruto de actividades que involucren el cuidado y el bienestar de las personas.")

    # 3. Interés Tecnológico y Digital
    p_tecnologia = perfil.get('interes_tecnologico_digital', 5)
    if p_tecnologia >= 8:
        frases_adicionales.append("Me apasiona la tecnología, el software y el mundo digital.")
    elif p_tecnologia >= 6:
        frases_adicionales.append("Tengo un marcado interés por las herramientas tecnológicas.")
    
    # 4. Creatividad e Innovación
    p_creatividad = perfil.get('creatividad_innovacion', 5)
    if p_creatividad >= 8:
        frases_adicionales.append("Soy una persona muy creativa, con facilidad para la innovación y el diseño.")
    elif p_creatividad >= 6:
        frases_adicionales.append("Me considero alguien con buenas ideas y creatividad.")

    # Combinar todo en un solo prompt
    prompt_final = descripcion_original
    if frases_adicionales:
        prompt_final += ". " + " ".join(frases_adicionales)
    
    return prompt_final


@app.route("/recomendar", methods=["POST"])
def recomendar():
    if collection is None:
        return jsonify({"error": "La base de datos vectorial no está disponible."}), 500
    
    data = request.get_json()
    entrada_texto = data.get("texto", "")
    perfil_usuario = data.get("perfil", {})

    # 1. usamos la función para crear el prompt mejorado
    prompt_final = construir_prompt_enriquecido(entrada_texto, perfil_usuario)
    
    print(f"Prompt Enriquecido para la búsqueda: {prompt_final}")

    # 2. el resto del proceso es el mismo, pero con el prompt mejorado
    embedding = model.encode([prompt_final])
    
    try:
        resultados = collection.query(
            query_embeddings=embedding,
            n_results=5,
            include=["metadatas", "distances"]
        )
    except Exception as e:
        return jsonify({"error": f"Error en la consulta a la base de datos: {str(e)}"}), 500

    # Formatear la respuesta
    respuesta = [
        {
            "carrera": m.get("carrera", "N/A"),
            "institucion": m.get("institucion", "N/A"),
            "similitud": round(d, 3) # Convertir distancia a similitud
        }
        for m, d in zip(resultados['metadatas'][0], resultados['distances'][0])
    ]
    
    return jsonify(respuesta)

if __name__ == "__main__":
    app.run(debug=True)