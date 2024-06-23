from flask import Flask, jsonify
import random  # Esto es solo para generar datos aleatorios de ejemplo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_data():
    # Esta función es solo para simular datos, deberías reemplazarla con tu propia lógica de acceso a datos
    return {
        "count": random.randint(50, 150),
        "average": round(random.uniform(10, 30), 2),
        "median": round(random.uniform(10, 30), 2),
        "stdDev": round(random.uniform(0.5, 2.5), 2),
        "max": round(random.uniform(30, 40), 2),
        "min": round(random.uniform(5, 10), 2),
        "mode": round(random.uniform(10, 30), 2)
    }

@app.route('/data/<string:panel_id>')
def get_data(panel_id):
    if panel_id not in ['temp', 'hum', 'viento', 'lum', 'aire', 'pres']:
        return jsonify({"error": "Invalid panel ID"}), 404

    data = generate_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)  # Asegúrate de desactivar el modo debug en producción