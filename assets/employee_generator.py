import json
import random
from datetime import datetime, timedelta

# Configuración
num_employees = 4000
departments = [1, 2, 3]  # Ejemplo de IDs de departamentos
jobs = [1, 2]  # Ejemplo de IDs de trabajos

# Generar registros de empleados
records = []
for i in range(3000, num_employees + 1):
    record = {
        "employee_id": i,
        "name": f"Employee {i}",
        "datetime": (datetime.now() + timedelta(days=i)).isoformat(),
        "department_id": random.choice(departments),
        "job_id": random.choice(jobs)
    }
    records.append(record)

# Crear la solicitud JSON
request_payload = {
    "table_name": "employee",
    "records": records
}

# Guardar en un archivo JSON
with open('employees.json', 'w') as json_file:
    json.dump(request_payload, json_file, indent=4)

print("Archivo employees.json generado con 1000 empleados.")