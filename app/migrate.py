import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from data_validation import validate_data, log_invalid_records

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

def load_csv_to_table(engine, filepath, table_name):
    """Cargar datos desde un archivo CSV a una tabla de la base de datos."""
    df = pd.read_csv(filepath, header=None)

    # Asignar nombres de columnas según la tabla que se está cargando
    if table_name == 'department':
        df.columns = ['department_id', 'department']
    elif table_name == 'employee':
        df.columns = ['employee_id', 'name', 'datetime', 'department_id', 'job_id']
    elif table_name == 'job':
        df.columns = ['job_id', 'job']

    # Validar los datos y obtener índices de filas vacías
    empty_indices = validate_data(df)

    # Separar filas válidas e inválidas
    if empty_indices:
        # Filtrar los registros vacíos
        invalid_rows = df.iloc[empty_indices]
        valid_rows = df.drop(empty_indices)

        # Registrar los registros inválidos
        log_invalid_records(invalid_rows, filepath)
    else:
        valid_rows = df

    # Insertar los datos válidos en la base de datos
    with engine.connect() as connection:
        valid_rows.to_sql(table_name, con=connection, if_exists='append', index=False)
        print(f"Los datos de '{filepath}' se han cargado correctamente en la tabla '{table_name}'.")

def main():
    """Función principal para ejecutar la carga de datos."""
    # Crear la conexión a la base de datos
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    
    # Definir los archivos CSV y sus respectivas tablas
    files = {
        'C:/Users/danie/OneDrive/Documentos/InteligentHR/assets/data/departments.csv': 'department',
        'C:/Users/danie/OneDrive/Documentos/InteligentHR/assets/data/jobs.csv': 'job',
        'C:/Users/danie/OneDrive/Documentos/InteligentHR/assets/data/hired_employees.csv': 'employee'
    }
    
    for filepath, table_name in files.items():
        load_csv_to_table(engine, filepath, table_name)

if __name__ == '__main__':
    main()