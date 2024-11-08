from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()
# Crear una clase base
Base = declarative_base()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')


# Crea una conexión al servidor PostgreSQL
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/')


# Definir un modelo
class Employee(Base):
    __tablename__ = 'employee'
    
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datetime = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc)  )

    #Llaves foráneas
    job_id = Column(Integer, ForeignKey('job.job_id'))
    department_id = Column(Integer, ForeignKey('department.department_id'))

    job = relationship("Job", back_populates="employees")
    department = relationship("Department", back_populates="employees")

class Job(Base):
    __tablename__ = 'job'
    job_id = Column(Integer, primary_key=True)
    job = Column(String)
    
    employees = relationship("Employee", back_populates="job")

class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    department = Column(String)
    
    employees = relationship("Employee", back_populates="department")

def create_tables(user,password,host,port,db_name):
    engine_db = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Base.metadata.create_all(engine_db)  # Crea todas las tablas definidas en Base

if __name__ == '__main__':
    create_tables(user,password,host,port,db_name)
