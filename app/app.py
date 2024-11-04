from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import os
import json  # Importar el módulo json
from dotenv import load_dotenv
from data_validation import validate_data, log_invalid_records
import pandas as pd

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Cargar la configuración desde el archivo config.json
with open('../assets/db_config.json') as config_file:
    config = json.load(config_file)
    TABLE_CONFIG = config['tables']  # Extraer la sección de tablas

# Inicializar la aplicación Flask
app = Flask(__name__)

# Crear la conexión a la base de datos
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

@app.route('/upload', methods=['POST'])
def upload_data():
    """Endpoint para recibir nuevos datos en formato JSON y cargarlos en la base de datos."""
    data = request.json
    table_name = data.get('table_name')
    records = data.get('records')

    if not table_name or not records:
        return jsonify({'error': 'Faltan datos necesarios.'}), 400

    # Verificar si la tabla existe en la configuración
    if table_name not in TABLE_CONFIG:
        return jsonify({'error': 'Nombre de tabla no válido.'}), 400

    # Crear DataFrame desde los registros recibidos
    df = pd.DataFrame(records)

    # Asignar nombres de columnas desde la configuración
    df.columns = TABLE_CONFIG[table_name]

    # Validar los datos y obtener índices de filas vacías
    empty_indices = validate_data(df)

    # Separar filas válidas e inválidas
    if empty_indices:
        invalid_rows = df.iloc[empty_indices]
        valid_rows = df.drop(empty_indices)

        # Registrar los registros inválidos
        log_invalid_records(invalid_rows, 'upload_log.csv')
        return jsonify({'message': 'Algunos registros son inválidos y han sido registrados.', 'invalid_count': len(invalid_rows)}), 400
    else:
        valid_rows = df

    # Intentar insertar los datos válidos en la base de datos
    try:
        with engine.connect() as connection:
            valid_rows.to_sql(table_name, con=connection, if_exists='append', index=False)
        return jsonify({'message': 'Datos cargados exitosamente.'}), 200
    except IntegrityError as e:
        return jsonify({'error': 'Error al insertar datos: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
