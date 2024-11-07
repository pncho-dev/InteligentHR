import pandas as pd
from datetime import datetime

def validate_data(df):
    
    empty_indices = df.index[df.isnull().any(axis=1)].tolist()
    return empty_indices

def log_invalid_records_migrate(invalid_rows, filepath):
    
    log_filepath = filepath.replace(".csv", "")
    log_filepath = log_filepath.replace("historic_data", "logs")
    log_filepath = f"{log_filepath}_log.csv"
    invalid_rows.to_csv(log_filepath, index=False, header=False)


def separate_rows_migration(df, filepath):
    """Separar filas válidas e inválidas y registrar las inválidas."""
    empty_indices = validate_data(df)

    # Filtrar los registros vacíos
    if empty_indices:
        invalid_rows = df.iloc[empty_indices]
        valid_rows = df.drop(empty_indices)

        # Registrar los registros inválidos
        log_invalid_records_migrate(invalid_rows, filepath)
        invalid_count = len(invalid_rows)
    else:
        valid_rows = df
        invalid_count = 0

    return valid_rows, invalid_count
