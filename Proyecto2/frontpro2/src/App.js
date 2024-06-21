import React, { useState } from 'react';
import './App.css';

import temperaturaImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-temperatura-50.png';
import humedadImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-humedad-50.png';
import vientoImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-viento-50.png';
import aireImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-aire-50.png';
import presionImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-barómetro-50.png';
import luminosidadImg from 'C:/Users/PERSONAL/frontpro2/src/icons8-luz-50.png';


function App() {
  const [selectedOption, setSelectedOption] = useState('');

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const imageMap = {
    'Temperatura': temperaturaImg,
    'Humedad': humedadImg,
    'Velocidad del Viento': vientoImg,
    'Presión Barométrica': presionImg,
    'airQuality': aireImg,
    'luminosity': luminosidadImg,
  };

  const renderContent = () => {
    switch(selectedOption) {
      case 'Temperatura':
      case 'Humedad':
      case 'Velocidad del Viento':
      case 'Presión Barométrica':
        return (
          <>
            <div className="selectedOptionContainer">
              
            <table className="infoTable">
  <caption>
    <div className="captionContent">
      <span className="captionText">{selectedOption}</span>
      <img src={imageMap[selectedOption]} alt={selectedOption} className="optionImage" />
    </div>
  </caption>
  <tbody>
    <tr>
      <th>Promedio</th><th>Mediana</th><th>Desviación Estándar</th>
      <th>Máximo</th><th>Mínimo</th><th>Moda</th>
    </tr>
    <tr>
      <td>-</td><td>-</td><td>-</td>
      <td>-</td><td>-</td><td>-</td>
    </tr>
  </tbody>
</table>
            </div>
          </>
        );
      case 'luminosity':
        // Aqui va la integración conectado al backend
        
        return (
          <div className="airQualityContainer">
            <img src={luminosidadImg} alt="Calidad del aire" className="optionImage" />
            <p>Condición Actual: {/* Aquí iría el estado del backend */}</p>
          </div>
        );
        case 'airQuality':
          // Aqui va la integración conectado al backend
          return (
            <div className="airQualityContainer">
              <img src={aireImg} alt="Calidad del aire" className="optionImage" />
              <p>La calidad del aire es: {/* Aquí iría el estado del backend */}</p>
            </div>
          );
        
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <header>
      <h1>‎ </h1>
      <h1>‎ </h1>

        <h1>climateTech.</h1>
        <div class="loader">
  <div class="circle">
    <div class="dot"></div>
    <div class="outline"></div>
  </div>
  <div class="circle">
    <div class="dot"></div>
    <div class="outline"></div>
  </div>
  <div class="circle">
    <div class="dot"></div>
    <div class="outline"></div>
  </div>
  <div class="circle">
    <div class="dot"></div>
    <div class="outline"></div>
  </div>
</div>
      </header>
      <main>
        <section>
          <label htmlFor="climateOption">Elige un sensor:</label>
          <select id="climateOption" onChange={handleSelectChange} value={selectedOption}>
            <option value="">--Selecciona una opción--</option>
            <option value="Temperatura">Temperatura</option>
            <option value="Humedad">Humedad</option>
            <option value="Velocidad del Viento">Velocidad del Viento</option>
            <option value="airQuality">Calidad de Aire</option>
            <option value="Presión Barométrica">Presión Barométrica</option>
            <option value="luminosity">Luminosidad</option>
          </select>
        </section>
        <section id="displayArea">
          {renderContent()}
        </section>
      </main>

      
    </div>

    
  );
}

export default App;
