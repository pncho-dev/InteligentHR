from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import os
import json  # Importar el módulo json
from dotenv import load_dotenv
from utils import log_invalid_records, separate_valid_invalid
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
        df.columns = TABLE_CONFIG[table_name]  # Asignar nombres de columnas desde la configuración

        # Separar filas válidas e inválidas
        valid_rows, invalid_rows, invalid_count = separate_valid_invalid(df, 'upload_log.csv')

        # Registrar los registros inválidos si existen
        if invalid_count > 0:
            log_invalid_records(invalid_rows, 'upload_log.csv')

        # Intentar insertar los datos válidos en la base de datos
        try:
            with engine.connect() as connection:
                valid_rows.to_sql(table_name, con=connection, if_exists='append', index=False)
        except IntegrityError as e:
            return jsonify({'error': f'Error al insertar datos en {table_name}: ' + str(e)}), 500

    return jsonify({'message': 'Datos cargados exitosamente.'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
