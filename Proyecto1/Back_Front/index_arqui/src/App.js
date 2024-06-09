import React, { useState, useEffect } from 'react';
import './App.css';

function IconLightbulb(props) {
  return (
    <svg
      viewBox="0 0 384 512"
      fill="currentColor"
      height="2em"
      width="2em"
      {...props}
    >
      <path d="M112.1 454.3c0 6.297 1.816 12.44 5.284 17.69l17.14 25.69c5.25 7.875 17.17 14.28 26.64 14.28h61.67c9.438 0 21.36-6.401 26.61-14.28l17.08-25.68c2.938-4.438 5.348-12.37 5.348-17.7l.128-39.2H112l.1 39.2zM192 0C90.02.32 16 82.97 16 175.1c0 44.38 16.44 84.84 43.56 115.8 16.53 18.84 42.34 58.23 52.22 91.45.031.25.094.517.125.782h160.2c.031-.265.094-.516.125-.782 9.875-33.22 35.69-72.61 52.22-91.45C351.6 260.8 368 220.4 368 175.1 368 78.8 289.2.004 192 0zm96.4 260.1c-15.66 17.85-35.04 46.3-49.05 75.89h-94.61c-14.01-29.59-33.39-58.04-49.04-75.88C75.24 236.8 64 206.1 64 175.1 64 113.3 112.1 48.25 191.1 48 262.6 48 320 105.4 320 175.1c0 31-11.2 61.7-31.6 85zM176 80c-44.1 0-80 35.9-80 80 0 8.844 7.156 16 16 16s16-7.2 16-16c0-26.47 21.53-48 48-48 8.844 0 16-7.148 16-15.99S184.8 80 176 80z" />
    </svg>
  );
}

function IconPeopleTwentyFour(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="2em"
      width="2em"
      {...props}
    >
      <path
        fillRule="evenodd"
        d="M3.5 8a5.5 5.5 0 118.596 4.547 9.005 9.005 0 015.9 8.18.75.75 0 01-1.5.045 7.5 7.5 0 00-14.993 0 .75.75 0 01-1.499-.044 9.005 9.005 0 015.9-8.181A5.494 5.494 0 013.5 8zM9 4a4 4 0 100 8 4 4 0 000-8z"
      />
      <path d="M17.29 8c-.148 0-.292.01-.434.03a.75.75 0 11-.212-1.484 4.53 4.53 0 013.38 8.097 6.69 6.69 0 013.956 6.107.75.75 0 01-1.5 0 5.193 5.193 0 00-3.696-4.972l-.534-.16v-1.676l.41-.209A3.03 3.03 0 0017.29 8z" />
    </svg>
  );
}

function IconAlert(props) {
  return (
    <svg
      viewBox="0 0 1024 1024"
      fill="currentColor"
      height="3em"
      width="3em"
      {...props}
    >
      <path d="M193 796c0 17.7 14.3 32 32 32h574c17.7 0 32-14.3 32-32V563c0-176.2-142.8-319-319-319S193 386.8 193 563v233zm72-233c0-136.4 110.6-247 247-247s247 110.6 247 247v193H404V585c0-5.5-4.5-10-10-10h-44c-5.5 0-10 4.5-10 10v171h-75V563zm-48.1-252.5l39.6-39.6c3.1-3.1 3.1-8.2 0-11.3l-67.9-67.9a8.03 8.03 0 00-11.3 0l-39.6 39.6a8.03 8.03 0 000 11.3l67.9 67.9c3.1 3.1 8.1 3.1 11.3 0zm669.6-79.2l-39.6-39.6a8.03 8.03 0 00-11.3 0l-67.9 67.9a8.03 8.03 0 000 11.3l39.6 39.6c3.1 3.1 8.2 3.1 11.3 0l67.9-67.9c3.1-3.2 3.1-8.2 0-11.3zM832 892H192c-17.7 0-32 14.3-32 32v24c0 4.4 3.6 8 8 8h688c4.4 0 8-3.6 8-8v-24c0-17.7-14.3-32-32-32zM484 180h56c4.4 0 8-3.6 8-8V76c0-4.4-3.6-8-8-8h-56c-4.4 0-8 3.6-8 8v96c0 4.4 3.6 8 8 8z" />
    </svg>
  );
}

function IconDoorOpenLine(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="3em"
      width="3em"
      {...props}
    >
      <path fill="none" d="M0 0h24v24H0z" />
      <path d="M2 21v-2h2V4.835a1 1 0 01.821-.984l9.472-1.722a.599.599 0 01.707.59v1.28L19 4a1 1 0 011 1v14h2v2h-4V6h-3v15H2zM13 4.396L6 5.67V19h7V4.396zM12 11v2h-2v-2h2z" />
    </svg>
  );
}

function IconShield(props) {
  return (
    <svg
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      viewBox="0 0 24 24"
      height="3em"
      width="3em"
      {...props}
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function App() {
  const [lights, setLights] = useState({
    lobby: false,
    warehouse: false,
    exterior: false,
    offices: false
  });
  const [peopleCount, setPeopleCount] = useState(0);
  const [isConveyorMoving, setConveyorMoving] = useState(false);
  const [isGateOpen, setGateOpen] = useState(false);
  const [isAlarmActive, setAlarmActive] = useState(false);

  useEffect(() => {
    toggleGate();
  }, []);

  const toggleLight = (area) => {
    fetch(`http://localhost:5000/api/lights/${area}`, { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setLights(data.lights);
        }
      });
  };

  const incrementPeopleCount = () => {
    fetch('/api/peopleCount', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setPeopleCount(data.peopleCount);
        }
      });
  };

  const toggleConveyor = () => {
    fetch('/api/conveyor', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setConveyorMoving(data.isConveyorMoving);
        }
      });
  };

  const toggleGate = () => {
    fetch('http://localhost:5000/api/gate', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setGateOpen(data.isGateOpen);
        }
      });
  };

  const toggleAlarm = () => {
    fetch('/api/alarm', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setAlarmActive(data.isAlarmActive);
        }
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Control de Establecimiento</h1>
      </header>
      <div className="container">
        <div className="control-container">
          <h2 className="control-title">Control de Luces</h2>
          <div className="light-controls">
            <div>
              <IconLightbulb />
              <label>Lobby</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="lobby-toggle"
                  type="checkbox"
                  checked={lights.lobby}
                  onChange={() => toggleLight('lobby')}
                />
                <label className="toggle-label" htmlFor="lobby-toggle"></label>
              </div>
            </div>
            <div>
              <IconLightbulb />
              <label>Warehouse</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="warehouse-toggle"
                  type="checkbox"
                  checked={lights.warehouse}
                  onChange={() => toggleLight('warehouse')}
                />
                <label className="toggle-label" htmlFor="warehouse-toggle"></label>
              </div>
            </div>
            <div>
              <IconLightbulb />
              <label>Offices</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="offices-toggle"
                  type="checkbox"
                  checked={lights.offices}
                  onChange={() => toggleLight('offices')}
                />
                <label className="toggle-label" htmlFor="offices-toggle"></label>
              </div>
            </div>
            <div>
              <IconLightbulb />
              <label>Exterior</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="exterior-toggle"
                  type="checkbox"
                  checked={lights.exterior}
                  onChange={() => toggleLight('exterior')}
                />
                <label className="toggle-label" htmlFor="exterior-toggle"></label>
              </div>
            </div>
          </div>
        </div>
        <div className="control-container">
          <h2 className="control-title">Conteo de Personas</h2>
          <IconPeopleTwentyFour />
          <p>Entradas</p>
          <h2>Total: {peopleCount}</h2>
        </div>
        <div className="control-container">
          <h2 className="control-title">Banda Transportadora</h2>
          <IconAlert />
          <p>‎ ‎ ‎ ‎ ‎ </p>
          <div className="toggle-switch">
            <input
              className="toggle-input"
              id="conveyor-toggle"
              type="checkbox"
              checked={isConveyorMoving}
              onChange={() => setConveyorMoving(prevState => !prevState)}
            />
            <label className="toggle-label" htmlFor="conveyor-toggle"></label>
          </div>
          <p>‎ ‎ ‎ ‎ ‎ </p>
          <p>‎ ‎ ‎ ‎ ‎ </p>
          <p>Estado</p>
          <p>{isConveyorMoving ? 'En Movimiento' : 'Detenida'}</p>
        </div>
        <div className="control-container">
          <h2 className="control-title">Control de Puerta</h2>
          <IconDoorOpenLine />
          <div className="door-controls">
            <label className="switch">
              <input type="checkbox" className="chk" checked={isGateOpen} onChange={toggleGate} />
              <span className="slider"></span>
            </label>
          </div>
          <p>‎ ‎ ‎ ‎ ‎ </p>
          <p>Estado</p>
          <p>{isGateOpen ? 'Abierta' : 'Cerrada'}</p>
        </div>
        <div className="control-container">
          <h2 className="control-title">Alarma Perimetral</h2>
          <IconShield />
          <p>‎ ‎ ‎ ‎ ‎ </p>
          <p>Estado: {isAlarmActive ? 'Activada' : 'Desactivada'}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
