import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  const [inputTexto, setInputTexto] = useState('');
  
  // 1. AÑADIMOS ESTADOS PARA LAS 4 CARACTERÍSTICAS PRINCIPALES
  const [habilidadLogica, setHabilidadLogica] = useState(5);
  const [vocacionServicio, setVocacionServicio] = useState(5);
  const [interesTecnologico, setInteresTecnologico] = useState(5);
  const [creatividad, setCreatividad] = useState(5);

  const [resultados, setResultados] = useState([]);
  const [cargando, setCargando] = useState(false);

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setCargando(true);

    try {
      // 2. ENVIAMOS EL PERFIL COMPLETO EN LA PETICIÓN
      const respuesta = await axios.post('http://localhost:5000/recomendar', {
        texto: inputTexto,
        perfil: {
          habilidad_logica_matematica: parseInt(habilidadLogica),
          vocacion_servicio_cuidado: parseInt(vocacionServicio),
          interes_tecnologico_digital: parseInt(interesTecnologico),
          creatividad_innovacion: parseInt(creatividad),
        }
      });

      setResultados(respuesta.data);
    } catch (error) {
      console.error("Error al obtener recomendaciones", error);
      alert("Hubo un error al obtener las recomendaciones. Por favor, intenta de nuevo.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="container">
      <h1>Recomendador de Carreras</h1>
      <p>Describe tus intereses y luego ajusta tus habilidades para obtener una recomendación más precisa.</p>
      
      <form onSubmit={manejarSubmit}>
        <textarea
          value={inputTexto}
          onChange={(e) => setInputTexto(e.target.value)}
          placeholder="Ej: Me gusta crear cosas, la tecnología y ayudar a la gente..."
          rows="3"
        />

        {/* 3. AÑADIMOS LOS SLIDERS A LA INTERFAZ */}
        <div className="sliders-container">
          <div className="slider-item">
            <label>Habilidad Lógica / Matemática: {habilidadLogica}</label>
            <input type="range" min="1" max="10" value={habilidadLogica} onChange={(e) => setHabilidadLogica(e.target.value)} />
          </div>
          <div className="slider-item">
            <label>Vocación de Servicio / Cuidado: {vocacionServicio}</label>
            <input type="range" min="1" max="10" value={vocacionServicio} onChange={(e) => setVocacionServicio(e.target.value)} />
          </div>
          <div className="slider-item">
            <label>Interés Tecnológico / Digital: {interesTecnologico}</label>
            <input type="range" min="1" max="10" value={interesTecnologico} onChange={(e) => setInteresTecnologico(e.target.value)} />
          </div>
          <div className="slider-item">
            <label>Creatividad / Innovación: {creatividad}</label>
            <input type="range" min="1" max="10" value={creatividad} onChange={(e) => setCreatividad(e.target.value)} />
          </div>
        </div>
        
        <button type="submit" disabled={cargando}>
          {cargando ? 'Buscando...' : 'Obtener Recomendación'}
        </button>
      </form>

      <div className="resultados-container">
        {resultados.length > 0 && (
          <>
            <h2>Resultados Sugeridos:</h2>
            <ol>
              {resultados.map((r, index) => (
                <li key={index}>
                  <strong>{r.carrera}</strong> — {r.institucion} (Similitud: {r.similitud})
                </li>
              ))}
            </ol>
          </>
        )}
      </div>
    </div>
  );
}

export default App;