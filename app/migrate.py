import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from utils import separate_rows_migration
import json  # Importar el módulo json

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Cargar la configuración desde el archivo config.json
with open('../data/config/db_config.json') as config_file:
    config = json.load(config_file)
    TABLE_CONFIG = config['tables']  # Extraer la sección de tablas


def load_csv_to_table(engine, filepath, table_name):
    """Cargar datos desde un archivo CSV a una tabla de la base de datos."""
    df = pd.read_csv(filepath, header=None)

   # Asignar nombres de columnas desde la configuración
    column_names = TABLE_CONFIG[table_name]
    df.columns = column_names

    # Separar filas válidas e inválidas
    valid_rows, invalid_count = separate_rows_migration(df,filepath)

    #eliminar la columna employee_id
    if table_name == 'employee':
        valid_rows = valid_rows.drop(columns=['employee_id'])

    # Insertar los datos válidos en la base de datos
    with engine.connect() as connection:
        valid_rows.to_sql(table_name, con=connection, if_exists='append', index=False)
        print(f"Los datos de '{filepath}' se han cargado correctamente en la tabla '{table_name}'.")
        if invalid_count > 0:
            print(f"Se registraron {invalid_count} registros inválidos")

def main():
    """Función principal para ejecutar la carga de datos."""
    # Crear la conexión a la base de datos
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    
    # Definir los archivos CSV y sus respectivas tablas
    files = {
        '../data/historic_data/departments.csv': 'department',
        '../data/historic_data/jobs.csv': 'job',
        '../data/historic_data/hired_employees.csv': 'employee'
    }
    
    for filepath, table_name in files.items():
        load_csv_to_table(engine, filepath, table_name)

if __name__ == '__main__':
    main()