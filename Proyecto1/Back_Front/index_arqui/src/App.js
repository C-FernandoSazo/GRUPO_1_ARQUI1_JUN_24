import React, { useState, useEffect } from 'react';
import './App.css';
import socketIOClient from "socket.io-client";

function IconLightbulb(props) {
  return (
    <svg
      viewBox="0 0 384 512"
      fill="currentColor"
      height="1.5em"
      width="1.5em"
      {...props}
    >
      <path d="M112.1 454.3c0 6.297 1.816 12.44 5.284 17.69l17.14 25.69c5.25 7.875 17.17 14.28 26.64 14.28h61.67c9.438 0 21.36-6.401 26.61-14.28l17.08-25.68c2.938-4.438 5.348-12.37 5.348-17.7l.128-39.2H112l.1 39.2zM192 0C90.02.32 16 82.97 16 175.1c0 44.38 16.44 84.84 43.56 115.8 16.53 18.84 42.34 58.23 52.22 91.45.031.25.094.517.125.782h160.2c.031-.265.094-.516.125-.782 9.875-33.22 35.69-72.61 52.22-91.45C351.6 260.8 368 220.4 368 175.1 368 78.8 289.2.004 192 0zm96.4 260.1c-15.66 17.85-35.04 46.3-49.05 75.89h-94.61c-14.01-29.59-33.39-58.04-49.04-75.88C75.24 236.8 64 206.1 64 175.1 64 113.3 112.1 48.25 191.1 48 262.6 48 320 105.4 320 175.1c0 31-11.2 61.7-31.6 85zM176 80c-44.1 0-80 35.9-80 80 0 8.844 7.156 16 16 16s16-7.2 16-16c0-26.47 21.53-48 48-48 8.844 0 16-7.148 16-15.99S184.8 80 176 80z" />
    </svg>
  );
}

function IconReceotion(props) {
  return (
    <svg
      fill="currentColor"
      viewBox="0 0 16 16"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path d="M8 16A8 8 0 108 0a8 8 0 000 16zm.93-9.412l-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 110-2 1 1 0 010 2z" />
    </svg>
  );
}

function IconAdminLine(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path fill="none" d="M0 0h24v24H0z" />
      <path d="M12 14v2a6 6 0 00-6 6H4a8 8 0 018-8zm0-1c-3.315 0-6-2.685-6-6s2.685-6 6-6 6 2.685 6 6-2.685 6-6 6zm0-2c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm9 6h1v5h-8v-5h1v-1a3 3 0 016 0v1zm-2 0v-1a1 1 0 00-2 0v1h2z" />
    </svg>
  );
}

function IconPhoneInTalk(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path d="M15 12h2a5 5 0 00-5-5v2a3 3 0 013 3m4 0h2c0-5-4.03-9-9-9v2c3.86 0 7 3.13 7 7m1 3.5c-1.25 0-2.45-.2-3.57-.57-.35-.11-.74-.03-1.02.25l-2.2 2.2a15.097 15.097 0 01-6.59-6.59l2.2-2.2c.28-.28.36-.67.25-1.02A11.36 11.36 0 018.5 4a1 1 0 00-1-1H4a1 1 0 00-1 1 17 17 0 0017 17 1 1 0 001-1v-3.5a1 1 0 00-1-1z" />
    </svg>
  );
}

function IconBoxesPacking(props) {
  return (
    <svg
      viewBox="0 0 640 512"
      fill="currentColor"
      height="3em"
      width="3em"
      {...props}
    >
      <path d="M256 48c0-26.5 21.5-48 48-48h288c26.5 0 48 21.5 48 48v416c0 26.5-21.5 48-48 48H381.3c1.8-5 2.7-10.4 2.7-16V253.3c18.6-6.6 32-24.4 32-45.3v-32c0-26.5-21.5-48-48-48H256V48zm315.3 299.3c6.2-6.2 6.2-16.4 0-22.6l-64-64c-6.2-6.2-16.4-6.2-22.6 0l-64 64c-6.2 6.2-6.2 16.4 0 22.6s16.4 6.2 22.6 0l36.7-36.7V432c0 8.8 7.2 16 16 16s16-7.2 16-16V310.6l36.7 36.7c6.2 6.2 16.4 6.2 22.6 0zM0 176c0-8.8 7.2-16 16-16h352c8.8 0 16 7.2 16 16v32c0 8.8-7.2 16-16 16H16c-8.8 0-16-7.2-16-16v-32zm352 80v224c0 17.7-14.3 32-32 32H64c-17.7 0-32-14.3-32-32V256h320zm-208 64c-8.8 0-16 7.2-16 16s7.2 16 16 16h96c8.8 0 16-7.2 16-16s-7.2-16-16-16h-96z" />
    </svg>
  );
}

function Icon177Truck(props) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path
        fill="currentColor"
        d="M16 9l-2-4h-3V3c0-.55-.45-1-1-1H1c-.55 0-1 .45-1 1v8l1 1h1.268a2 2 0 103.464 0h5.536a2 2 0 103.464 0H16V9zm-5 0V6h2.073l1.5 3H11z"
      />
    </svg>
  );
}

function IconCafe(props) {
  return (
    <svg
      viewBox="0 0 512 512"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path d="M432 64H96a16 16 0 00-16 16v192a96.11 96.11 0 0096 96h112a96.11 96.11 0 0096-96v-80h18a62.07 62.07 0 0062-62V96a32 32 0 00-32-32zm0 66a30 30 0 01-30 30h-18V96h48zM400 400H64a16 16 0 000 32h336a16 16 0 000-32z" />
    </svg>
  );
}

function IconToilet(props) {
  return (
    <svg
      viewBox="0 0 448 512"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path d="M24 0C10.7 0 0 10.7 0 24s10.7 24 24 24h8v148.9c-1.9 1.4-3.8 2.9-5.6 4.4C10.9 214.5 0 232.9 0 256c0 46.9 14.3 84.1 37 112.5 14.2 17.7 31.1 31.3 48.5 41.8l-19.9 59.6c-3.3 9.8-1.6 20.5 4.4 28.8S85.7 512 96 512h256c10.3 0 19.9-4.9 26-13.3s7.7-19.1 4.4-28.8l-19.8-59.5c17.4-10.5 34.3-24.1 48.5-41.8 22.7-28.4 37-65.5 37-112.5 0-23.1-10.9-41.5-26.4-54.6-1.8-1.5-3.7-3-5.6-4.4V48h8c13.3 0 24-10.7 24-24s-10.7-24-24-24H24zm360 256.3c0 1-.3 2.6-3.8 5.6-4.8 4.1-14 9-29.3 13.4C320.5 284 276.1 288 224 288s-96.5-4-126.9-12.8c-15.3-4.4-24.5-9.3-29.3-13.4-3.5-3-3.8-4.6-3.8-5.6v-.4c0-1 0-2.5 3.8-5.8 4.8-4.1 14-9 29.3-13.4C127.5 228 171.9 224 224 224s96.5 4 126.9 12.8c15.3 4.4 24.5 9.3 29.3 13.4 3.8 3.2 3.8 4.8 3.8 5.8v.4zM328.2 384l-.2.5v-.5h.2zM112 64h32c8.8 0 16 7.2 16 16s-7.2 16-16 16h-32c-8.8 0-16-7.2-16-16s7.2-16 16-16z" />
    </svg>
  );
}

function IconSlide(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="currentColor"
      height="2.5em"
      width="2.5em"
      {...props}
    >
      <path d="M14.83 15.45c-.36-.55-.65-1.06-.92-1.53-1.17-2.01-2.12-3.37-4.91-3.79V5.5C9 3.57 7.43 2 5.5 2S2 3.57 2 5.5V22h2v-2h3v2h2v-9.84c1.76.34 2.29 1.23 3.17 2.76.29.51.61 1.05 1 1.64C15.41 19.92 17.67 22 22 22v-2c-3.47 0-5.2-1.6-7.17-4.55M5.5 4C6.33 4 7 4.67 7 5.5V10H4V5.5C4 4.67 4.67 4 5.5 4M4 18v-2h3v2H4m3-4H4v-2h3v2z" />
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
    const socket = socketIOClient("http://localhost:5000");

    socket.on("update_people_count", data => {
      setPeopleCount(data.peopleCount);
    });

    return () => socket.disconnect();
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
    fetch('http://localhost:5000/api/peopleCount', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setPeopleCount(data.peopleCount);
        }
      });
  };

  const toggleConveyor = () => {
    fetch('http://localhost:5000/api/conveyor', { method: 'POST' })
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
    fetch('http://localhost:5000/api/alarm', { method: 'POST' })
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
          <h2 className="control-title">Control de Luces - Área 1‎ ‎ <IconLightbulb /></h2>
          <div className="light-controls">
            <div>
              <IconReceotion />
              <label>Recepción</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="lobby-toggle"
                  type="checkbox"
                  checked={lights.lobby}
                  onChange={() => toggleLight('Area_Recepcion')}
                />
                <label className="toggle-label" htmlFor="lobby-toggle"></label>
              </div>
            </div>
            <div>
              <IconPhoneInTalk />
              <label>Área Conferencias</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="warehouse-toggle"
                  type="checkbox"
                  checked={lights.warehouse}
                  onChange={() => toggleLight('Area_Conferencia')}
                />
                <label className="toggle-label" htmlFor="warehouse-toggle"></label>
              </div>
            </div>
            <div>
              <IconBoxesPacking />
              <label>Área de Trabajo</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="offices-toggle"
                  type="checkbox"
                  checked={lights.offices}
                  onChange={() => toggleLight('Area_Trabajo')}
                />
                <label className="toggle-label" htmlFor="offices-toggle"></label>
              </div>
            </div>
            <div>
              <IconAdminLine />
              <label>Administración</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="admin-toggle"
                  type="checkbox"
                  checked={lights.admin}
                  onChange={() => toggleLight('Area_Administracion')}
                />
                <label className="toggle-label" htmlFor="admin-toggle"></label>
              </div>
            </div>
          </div>
        </div>

        <div className="control-container">
        <h2 className="control-title">Control de Luces - Área 2‎ ‎ <IconLightbulb /></h2>
          <div className="light-controls">
            <div>
              <Icon177Truck />
              <label>Área de Transporte</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="transporte-toggle"
                  type="checkbox"
                  checked={lights.transporte}
                  onChange={() => toggleLight('Area_Transporte')}
                />
                <label className="toggle-label" htmlFor="transporte-toggle"></label>
              </div>
            </div>
            <div>
              <IconCafe />
              <label>Cafetería</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="cafeteria-toggle"
                  type="checkbox"
                  checked={lights.cafeteria}
                  onChange={() => toggleLight('Cafeteria')}
                />
                <label className="toggle-label" htmlFor="cafeteria-toggle"></label>
              </div>
            </div>
            <div>
              <IconToilet />
              <label>Baño</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="bano-toggle"
                  type="checkbox"
                  checked={lights.bano}
                  onChange={() => toggleLight('Bano')}
                />
                <label className="toggle-label" htmlFor="bano-toggle"></label>
              </div>
            </div>
            <div>
              <IconSlide />
              <label>Exterior</label>
              <div className="toggle-switch">
                <input
                  className="toggle-input"
                  id="exterior-toggle"
                  type="checkbox"
                  checked={lights.exterior}
                  onChange={() => toggleLight('Exterior')}
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
              onChange={() => toggleConveyor(prevState => !prevState)}
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
          <p>Estado: {isAlarmActive ? 'Alarma Activada' : 'Alarma Desactivada'}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
