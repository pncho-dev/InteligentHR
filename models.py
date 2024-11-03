from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

# Definir la base de datos
DATABASE_URL = "sqlite:///local_database.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase base
Base = declarative_base()

# Definir un modelo
class Employee(Base):
    __tablename__ = 'employee'
    
    employee_id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc)  )
    job_id = Column(Integer, ForeignKey('job.job_id'))

    job = relationship("Job", back_populates="employees")

class Job(Base):
    __tablename__ = 'job'
    job_id = Column(Integer, primary_key=True)
    job = Column(String)
    
    employees = relationship("Employee", back_populates="job")

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear una nueva instancia de employee
new_employee = Employee(employee_id=3, name='Pepito',job_id=1)
new_job = Job(job_id=1,job="Contador")
# Agregar a la sesión
session.add(new_employee)

# Confirmar los cambios
session.commit()

# Consultar todos los usuarios
employees = session.query(Employee).all()
for employee in employees:
    print(employee.employee_id, employee.name,employee.datetime, employee.job_id)

session.close()
