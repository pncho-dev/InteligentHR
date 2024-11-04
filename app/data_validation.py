# data_validation.py

import pandas as pd

def validate_data(df):
    
    empty_indices = df.index[df.isnull().any(axis=1)].tolist()
    return empty_indices

def log_invalid_records(invalid_rows, filepath):
    
    log_filepath = f"{filepath}_log.csv"
    invalid_rows.to_csv(log_filepath, index=False, header=False)
    print(f"Campos vacíos encontrados, las filas con campos vacíos fueron guardadas en: {log_filepath}")