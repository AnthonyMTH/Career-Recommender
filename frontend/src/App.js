import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [inputTexto, setInputTexto] = useState('');
  const [resultados, setResultados] = useState([]);

  const manejarSubmit = async (e) => {
    e.preventDefault();

    try {
      const respuesta = await axios.post('http://localhost:5000/recomendar', {
        texto: inputTexto,
      });

      setResultados(respuesta.data);
    } catch (error) {
      console.error("Error al obtener recomendaciones", error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Recomendador de Carreras</h1>
      <form onSubmit={manejarSubmit}>
        <input
          type="text"
          value={inputTexto}
          onChange={(e) => setInputTexto(e.target.value)}
          placeholder="¿Qué te interesa?"
          style={{ width: '300px', marginRight: '10px' }}
        />
        <button type="submit">Buscar</button>
      </form>

      <div style={{ marginTop: '2rem' }}>
        {resultados.length > 0 && (
          <ol>
            {resultados.map((r, index) => (
              <li key={index}>
                <strong>{r.carrera}</strong> — {r.institucion} (Similitud: {r.similitud})
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}

export default App;