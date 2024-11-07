import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
queries_path = os.getenv('QUERIES_PATH')

# Crear la conexión a la base de datos
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

def read_sql_file(file_path):
    """Lee el contenido de un archivo SQL y lo retorna como un string."""
    with open(file_path, 'r') as file:
        return file.read()

def execute_sql(query):
    """Ejecuta una consulta SQL y retorna el resultado como un DataFrame."""
    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df.to_dict(orient='records')
    except Exception as e:
        raise Exception(f"Error al ejecutar la consulta: {str(e)}")

def get_employee_counts():
    """Lee y ejecuta la consulta de conteo de empleados por trimestre."""
    query = read_sql_file(queries_path+'employee_counts.sql')  # Ruta al archivo SQL
    return execute_sql(query)

def get_departments_with_most_hired():
    """Lee y ejecuta la consulta de departamentos con más empleados contratados."""
    query = read_sql_file(queries_path+'departments_most_hired.sql')  # Ruta al archivo SQL
    return execute_sql(query)
