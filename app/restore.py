import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import fastavro
from sqlalchemy import text

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

def restore_table_from_avro(table_name,backup_path):
    """Restaura la tabla especificada desde un archivo Avro, eliminando primero los datos existentes."""
    avro_file = os.path.join(backup_path, f"backup_{table_name}.avro")  # Define el nombre del archivo Avro
    
    # Crear la conexión a la base de datos
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    try:
        with engine.connect() as connection:
            # Iniciar una transacción
            with connection.begin():
                # Eliminar la tabla si existe
                connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

                # Leer el archivo Avro
                with open(avro_file, 'rb') as f:
                    reader = fastavro.reader(f)
                    records = [record for record in reader]

                # Convertir los registros a un DataFrame
                df = pd.DataFrame(records)

                # Convertir columnas de tipo string que representan fechas a datetime
                for col in df.columns:
                    if df[col].dtype == 'object':
                        try:
                            df[col] = pd.to_datetime(df[col])
                        except Exception:
                            pass  # Si no se puede convertir, se deja como está

                # Insertar los datos en la base de datos
                df.to_sql(table_name, con=connection, if_exists='replace', index=False)

        print(f"Datos restaurados en la tabla '{table_name}' desde el archivo '{avro_file}'.")
    except Exception as e:
        print(f"Error al restaurar la tabla '{table_name}' desde '{avro_file}': {e}")
        raise
