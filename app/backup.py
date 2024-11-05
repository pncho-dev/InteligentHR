import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import fastavro

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

def get_avro_type(data_type):
    """Devuelve el tipo de Avro basado en el tipo de dato de la columna, usando un diccionario de mapeo."""
    avro_type_map = {
        'int64': 'int',
        'float64': 'float',
        'bool': 'boolean',
        'datetime64[ns]': 'string',  
        'object': 'string',  
    }

    return avro_type_map.get(str(data_type), 'string')

def backup_table(table_name, backup_path):
    """Realiza un backup de la tabla especificada en formato Avro y guarda el archivo en la ruta indicada."""
    # Crear la conexión a la base de datos
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    
    try:
        # Leer la tabla especificada en un DataFrame
        df = pd.read_sql_table(table_name, con=engine)

        # Convertir todas las columnas datetime a formato string
        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Formato de fecha iso

        # Generar el nombre del archivo de backup
        backup_file = os.path.join(backup_path, f"backup_{table_name}.avro")

        # Definir el esquema de Avro
        schema = {
            "type": "record",
            "name": table_name,
            "fields": []
        }

        # Generar el esquema de Avro
        for col in df.columns:
            avro_type = get_avro_type(df[col].dtype)
            schema["fields"].append({
                "name": col,
                "type": avro_type
            })

        # Convertir el DataFrame a una lista de diccionarios
        records = df.to_dict(orient='records')

        # Guardar los datos en formato Avro
        with open(backup_file, 'wb') as out:
            fastavro.writer(out, schema, records)

        print(f"Backup de la tabla '{table_name}' guardado en '{backup_file}'.")
        return backup_file

    except Exception as e:
        print( f"Error al realizar el backup de la tabla '{table_name}': {e}")
        
