import React, { useState, useEffect } from 'react';
import './App.css';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Conéctate a tu servidor de Flask

function ClimateTech() {
  const [activePanel, setActivePanel] = useState(null);
  const [tempData, setTempData] = useState({});
  const [humData, setHumData] = useState({});
  const [vientoData, setVientoData] = useState({});
  const [lumData, setLumData] = useState({ status: 'Soleado' });
  const [aireData, setAireData] = useState({ quality: 'Buena' });
  const [presData, setPresData] = useState({});

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Conectado a Socket.IO');
    });

    socket.on('luminosidad', (data) => {
      setLumData(data);
    });

    socket.on('calidad_aire', (data) => {
      setAireData(data);
    });

    socket.on('disconnect', () => {
      console.log('Desconectado de Socket.IO');
    });

    return () => {
      socket.off('connect');
      socket.off('luminosidad');
      socket.off('calidad_aire');
      socket.off('disconnect');
    };
  }, []);

  const fetchData = async (panelId) => {
    fetch(`http://localhost:5000/data/${panelId}`, { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        switch (panelId) {
          case 'temp':
            setTempData(data);
            break;
          case 'hum':
            setHumData(data);
            break;
          case 'viento':
            setVientoData(data);
            break;
          case 'lum':
            setLumData(data);
            break;
          case 'aire':
            setAireData(data);
            break;
          case 'pres':
            setPresData(data);
            break;
          default:
            console.error('Unrecognized panel ID');
        }
      })
      .catch(error => console.error('Failed to fetch data:', error));
  };

  const showPanel = (panelId) => {
    setActivePanel(activePanel === panelId ? null : panelId);
    fetchData(panelId);
  };

  return (
    <div className="container">
      <h1>
        <span className="symbol">&lt;</span>
        <span className="climate">climateTech.</span>
        <span className="symbol">/&gt;</span>
      </h1>
      <div className="button-panel">
        <button className="ui-btn" onClick={() => showPanel('temp')}><span>Temperatura</span></button>
        <button className="ui-btn" onClick={() => showPanel('hum')}><span>Humedad</span></button>
        <button className="ui-btn" onClick={() => showPanel('viento')}><span>V. Viento</span></button>
        <button className="ui-btn" onClick={() => showPanel('lum')}><span>Luminosidad</span></button>
        <button className="ui-btn" onClick={() => showPanel('aire')}><span>C. Aire</span></button>
        <button className="ui-btn" onClick={() => showPanel('pres')}><span>P. Barométrica</span></button>
      </div>
      <div id="infoPanel" className="info-panel">
        {Object.entries({ temp: tempData, hum: humData, viento: vientoData, lum: lumData, aire: aireData, pres: presData }).map(([key, data]) => (
          <div key={key} id={key} className="panel-content" style={{ display: activePanel === key ? 'block' : 'none' }}>
            <h2>{key === 'temp' ? 'Temperatura' :
              key === 'hum' ? 'Humedad' :
                key === 'viento' ? 'Velocidad del Viento' :
                  key === 'lum' ? 'Luminosidad' :
                    key === 'aire' ? 'Calidad del Aire' : 'Presión Barométrica'}</h2>
            {key === 'lum' || key === 'aire' ?
              <p>{key === 'lum' ? `Actualmente está: ${data.status || 'Soleado'}` : `La calidad del aire es: ${data.quality || 'Buena'}`}</p> :
              <table>
                <thead>
                  <tr>
                    <th>Contador</th>
                    <th>Promedio</th>
                    <th>Mediana</th>
                    <th>Desviación Estándar</th>
                    <th>Máximo</th>
                    <th>Mínimo</th>
                    <th>Moda</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{data.count || '-'}</td>
                    <td>{data.average || '-'}</td>
                    <td>{data.median || '-'}</td>
                    <td>{data.stdDev || '-'}</td>
                    <td>{data.max || '-'}</td>
                    <td>{data.min || '-'}</td>
                    <td>{data.mode || '-'}</td>
                  </tr>
                </tbody>
              </table>
            }
          </div>
        ))}
      </div>
      <div className="cardContainer">
        <WeatherCard />
      </div>
    </div>
  );
}

function WeatherCard() {
  return (
    <div className="card">
      <p className="city">GUATEMALA CITY</p>
      <p className="weather">PARTLY CLOUDY</p>
      <svg
        className="weather-icon"
        viewBox="0 0 100 100"
      >
        <image
          width="100"
          height="100"
          href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAMg0lEQVR42u2de5AcVb3HP7/unZ19Tt4vQsgGwpIABoREEVJqlFyLwgclEsmliFZULIWgqFHxlZKioBRKIVzBRwEmKUFQsQollhCzAW9xrzxKi/IiybVAgVjktdlkd3Z3errPzz+6Z3d2d2a3Z7bnsaF/VVvdc/qc032+nz3nd87p7tMQW2yxxRZbbLHFFltsscVWXZNaX0Ap1ruLeQ1ZlqN0CsxXQ6vCdFHaMKBCnxp6BNKqvCHKXs/mpfYPcaDW1x7W6haIdtGQdVlllDUoa1RZJTANBRQ02A79ZuTvEXEMPcBzCrvF0NUyj+dkDW6ty1jI6gqIbsEafBdrxLAB5TJRUqq5g1AWjLz0eWHH1fBrhO1te9kj38bUuuw5qwsg+hRzHJdNKB9HWTRCVIgaxoi0anhNlPvV5q7UVRyutRY1BaK7mOfYfEaVG0RJjREVKgpjRJghrXCv7XBb6zW8XitNagJEn6bZyfB14EsoyYKiQvVg5MVTwyDCbak2bpV1DFRbm6oDyXbxflW2IiwpKFYNYeTSql9jXka4ftoneaya+lQNiHbRloUfAlcNFbpeYYw8vj2T5dp519F3wgAZfIozLcPDKGdNJRh+HEGVvWp03cxreaHSWlmVPkHmSa4Sw/NTFQYKAmdYIv/bcxdXTmkgThebMGwXpWmqwsi7tmaDPHB0K1+cckBUkcwebkHYKsE5pjgM1K8pAnL70Tvk5ikFxHmKmwVuHL/QUwvGiHjC1498X26qhHaRO3VnD58FfnDCwhiRVj8/8wvcWbdAMk9xJR4/O5GaKcZJq4pRox+dvZlf1h2QzB85C5dnBFreDDCG4hnSanTV7K/ytyh0jMSH6NM0i8sDbzoY/rFWRB7ev8Uve10AyTr8AFjxpoMRHBc4O9kkd0Sh5aSbrGwXFys88WaFkR+m6Hvn3Mjuyeg5qRqif6VRlbtiGP5WPLln350kawYke4gvIyyLYQyFd844xucno2nZTZZ2MduBf6C0xjCGf6vS2+hpx/Rv012OrmXXEEf5XAxjbLkF2rOWXF+urmXVEN1JKpPkHwIzYhhjy61Kt6S1Y85t9JaqbVk1JJPk0zGM4uVGmUkz15SjbVlARNkYwxi/3MbIxqoAcXbxNmBZDGP8cotw5sFv8NaKA1Hl6hjGBOXOlcnI1RUHAnw4hhG6TB+pKJDBx1mOclIMI2SZYNHBzZxeMSCW/9BzDKOEMhnhPRUD4ilrYhillQmVygEROD+GUUKZ/HKdV6LG4Ux3khy0SItixzDCwQjO7fUOamvnXWTC6NwQFoijdJ5oMFTBM+B54Hr+vprhtLZAgwV2sF8qDBREsdsaOQ14MVIgatOJOTFgeB44LgxmIeP6+9qQwmqbj900C+Nm8PqP4Pa8RkIMjTYkbWiyIWEFzUoIGENhhjOiB2KYV46g9QTDMzDoQH8W0hlILnonqbM/QvuSd5Gc2xlclw5tvUya/tefp+eF39L9wsMkeg/RloTWhF9jQsFQEJgbVudSgLTn/jOmIgzH9SEcH4TGJZfQsXYLLQvOGboW1WEQGgRKooXWJatp6VjN/Eu+xZFntnP4iVsY6DvK9GZIWhPDCPbbw+ocupclSttUhZFx4Wg/HDMzmHfZTzltwyM0LzgHo4qqjtkW+qOhiVnvuIZTv/Ac5tRLOdzn5xvG+YuR6IEQAJlqMJwARjpxMh0bdzFjxUd94U0g9qitMeNDsltnccqGHTRd9CUO94HjjQ8jKHcqrMyhmywUo8XazTqF4XpwbADS9nw6P9VFYtpCX9g8PzHcPdWiWw1OkL+d+76vcUDh2P/czsym4XMKY8utSg5bdEAM9MkUgqEK/Rk47jSyeMMOEqkARnAxhbfFAYzdwpz/+Ar/OriPA3sfxQQ90ITl+5akBQnbb4JENfSdw9BARINXuqYIjKwLvRmYtfortC6+EBNELARiuMYUBzC25vjnn3flPWj2+9CQxO09QLb7ddL7nuT4iztpOPQSqSQ0SfjX4cL3spTjBfvfdQgDhX4HnOYOFl/0uTE1I7/JogiQ8Zqw3LkVBSsByQZQsKctxE4tJNnxNli7md4Xf8/h391KqvulwciBAP+aKjA84481Zq3ehDQ0YcxE4g43QwVhjYgzftx88K3L19J8+rsZ+NvO5dz/mVAih+5l2creeobhGb+ZGggGfY7XxLS3rCvajQ3T1R2KU6RHpkaHemzFem5YDTSd+YFrX3719W+G0Tn85GIXDekjpEVprCcYWdcfffdmICPttHZ+kOZFF9A0/2yaTjo/lH8Y20wN/5cX9zfF8y1YA1XVGF1/+qmLH4oECED6F7wILK8HGCaYBunphwHTzIwLb2D2hdcjiZZI/MPE/mY434nzGwLWi5ddunTp0oPFNC7Fh4DyDLC8HmCkB/0xRiYxn1PWP0zTgnP9eKaYGCP9QRHBxvclBfxEuPyG8m1Xy/4msKmYxCXdoFKlq55g9GuKxR97jKYF54b3D6NH5CX4hxF+okyfZIxufG7//qIv95R2T92wu9Y+IxM47X4HTvrAVhpnLi3NQU8yzlDcMoCqGlBa2vozayMB0rKe1zDsqxUMx4WBjD+pl1ywkvbll1UIgCkap5S4RWuJmtWRAAn0e6hWXdusO3xDacbKT6CEEWxYuErVpJLzM7owMiCey3YTzM9VE4bjQtYDT8E1QvOpF088YztRsxJhU1YKJA9mRQZk+gb+LvCnasJQHb7vbTywk9OxW2aV1/bnb0MCndA/lArJmIi6vYEZ5SeWckG1YKgJaobn97KslplDhR5KN6o7Ot64YXR3tJrjkSDf/ZHVEIBUPzvU8M9qwEDB5Hd7Fbz+7iq1/aaE/Ezoc2JMV6RA5NNkVfleNWDkH/cMiII32EO2vyevWQknhhYQbtIOutQ4xhxvSdp7IgUCkGrlJ2p4o9IwCJosVR+GJYBR0v//xKiCTjzRN65/qBIko/xXZ2dn0YfmygYi6xhAubHSMPLDBB+IKvT+5YFoBZsAZGiHP845jZpD6iS/O56uk3pPPfUJtqHsqTSM3I2x3LNQtgX9r/yR/r//oTLNymRqSXGQrmKuWrnytGMVAyKCWobrVMlWtGYEWyuYm24Mnoc69OgNOMf2V6ftDw3JjG2mjDGq3qZVK1Y8MZGmk158pv0a/g/DTZV88NkK0iVsH07C8muL23uQAw9ciXPkleC/0JQgrikBgJkEJHNc4EOrzl3xwzB62pMFAnDr+fz3YJu8Q+C0qGHkjuWe6jDG723ZEozc092k//oIVnIaibnLQCw/fRnjkqFxwiTHGsFpXcXca3uJK1aed9bzYbWMbAGz3ruZ6yF/JvfKW0QwgnKSzT0UrdA76IMxxp/1NUG8humLaV52KY0dF2G3z8NumY0R8L99MFbkXN6BhAXEHT2QDOKavHwEYxpbe0VIo7IfNa8qPK6O9ejb3372G6XqGOkSf8fu5gJjZBf5S25EACP3e8AZfn0g7QSCBeFZb1Ra8tJSJH/GuYa8sBH7eWGiDExP6sXnPcTTUWkY+SKYPVu52CCP5e69RwUDBTe4bZsbJKYdv5YQNGWu58PyCog5ZmxDuOsqBEMBC7JtSb38/Af5TZT6VWSp8e47uRqVbYBEBSMXJzfri/pN1WBQO3Iv2pRUM8qEgcEkbd14zs/ZFrV2FVv7vfsO/lON/FQgERWMXNqs5985zD/uun4NMqPOUS6MgmH+L8dCP3Xug2yvhG4VXYz/6O28V0V+jdIeFYxcmAmew3K9AmmjgjEqrUAadN0ZO9hZKc0q/nWEQ7exSlR+JbAoKhij47jesIMvmv8kYajymuvp5ct+xrOV1Ksqn6s4dguzsrZsE7g0Shih0kYBw/Bby9OPn7yDI5XWqnofdFGk+ztsViM3wfBnjuocxqCqfmPR/Xwvbx7ixACSswO3sNRS2SrKJfUMw8BuT/S6JfdGs2J1WKvZV9oO3swVovJdlI56gqGGVxDdvOg+flULXWr72bwfkThygPXGyI3o8KJoOcGqDONlNfqdAwnuX/ljsrXSpD4+LLkF65ByOSobFdaKYlcDhiqeGB5X0ftOXsgj9fDFz7oAkm8Hv8YCI6wXI1eoslKgIUoYanBVeRb0F67Dg0u2UfIEYCWt7oDk2+EtpLL9vBOR9+B/nHgZyuxSYKjhELBX4FlFdycdnpxzX+nLt1bL6hpIIXv1BmY2QqdRTgZaBdpM8PluC/rU0Af0eR77Ncu+U+4tb4Xp2GKLLbbYYosttthiiy222GKLLbbYYottfPs3GPtpnh9ZV0oAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMDItMTdUMDg6MDM6MDcrMDA6MDBPnKiVAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTAyLTE3VDA4OjAzOjA3KzAwOjAwPsEQKQAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0wMi0xN1QwODowMzowNyswMDowMGnUMfYAAAAASUVORK5CYII="
        />
      </svg>
      <p className="temp">32°</p>
      <div className="minmaxContainer">
        <div className="min">
          <p className="minHeading">Min</p>
          <p className="minTemp">30°</p>
        </div>
        <div className="max">
          <p className="maxHeading">Max</p>
          <p className="maxTemp">32°</p>
        </div>
      </div>
    </div>
  );
}

export default ClimateTech;
