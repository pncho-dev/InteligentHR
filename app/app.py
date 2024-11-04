from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import os
import json
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from backup import backup_table

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
    TABLE_CONFIG = config['tables']

# Inicializar la aplicación Flask
app = Flask(__name__)

# Crear la conexión a la base de datos
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')


@app.route('/upload', methods=['POST'])
def upload_data():
    """Endpoint para recibir nuevos datos en formato JSON y cargarlos en la base de datos."""
    data = request.json
    records = data.get('records')

    # Validar que se proporcionaron los datos necesarios
    if not records:
        return jsonify({'error': 'Faltan datos necesarios.'}), 400

    for record in records:
        table_name = record.get('table_name')
        table_data = record.get('data')

        # Verificar que se proporcionaron los datos de la tabla
        if not table_name or not table_data:
            return jsonify({'error': 'Faltan datos necesarios en un registro.'}), 400

        # Verificar que el número de registros no exceda 1000
        if len(table_data) > 1000:
            return jsonify({'error': f'Se permiten un máximo de 1000 registros para la tabla {table_name} por solicitud.'}), 400

        # Crear un DataFrame de los registros
        df = pd.DataFrame(table_data)

        # Asignar nombres de columnas desde la configuración
        expected_columns = TABLE_CONFIG[table_name]
        df.columns = expected_columns

        # Intentar insertar los datos válidos en la base de datos
        try:
            with engine.connect() as connection:
                df.to_sql(table_name, con=connection, if_exists='append', index=False)
        except IntegrityError as e:
            return jsonify({'error': f'Error al insertar datos en {table_name}: ' + str(e)}), 500

    return jsonify({'message': 'Datos cargados exitosamente.'}), 200


@app.route('/backup/<table_name>', methods=['POST'])
def backup_data(table_name):
    """Endpoint para realizar el backup de una tabla específica."""
    try:
        # Validar si la tabla existe en la configuración
        if table_name not in TABLE_CONFIG:
            return jsonify({'error': f'La tabla "{table_name}" no existe en la configuración.'}), 400

        backup_file = backup_table(table_name)  # Llama a la función de backup para la tabla específica
        return jsonify({'message': f'Backup de la tabla "{table_name}" realizado exitosamente.', 'file': backup_file}), 200
    except Exception as e:
        return jsonify({'error': f'Error al realizar el backup: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)